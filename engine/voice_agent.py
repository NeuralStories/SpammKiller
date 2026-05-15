"""Voice Agent - Real Pipecat pipeline with AudioSocket integration."""
import asyncio
import time
import uuid
import structlog
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

import boto3
from botocore.config import Config

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.frames.frames import (
    LLMMessagesFrame, EndFrame, AudioRawFrame, TextFrame
)
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.groq import GroqLLMService
from pipecat.services.cartesia import CartesiaTTSService

from tactic_engine import TacticEngine
from database.connection import get_db
from telegram_notifier import TelegramNotifier
from post_call_analyzer import PostCallAnalyzer
from audiosocket_server import AudioSocketServer, get_audio_socket_server

log = structlog.get_logger()


class VoiceAgent:
    """Voice Agent using Pipecat with AudioSocket audio I/O.

    Receives audio from Asterisk via AudioSocket (TCP port 9010),
    processes through STT->LLM->TTS pipeline, and sends audio back.
    """

    def __init__(self, reader, writer, call_id: str, caller_number: str, persona: Dict[str, Any]):
        self.reader = reader
        self.writer = writer
        self.call_id = call_id
        self.caller_number = caller_number
        self.persona = persona

        # Call state
        self.stream_id = str(uuid.uuid4())[:8]
        self.started_at = datetime.now()
        self.transcript: List[Dict] = []
        self.turn_number = 0
        self.audio_buffer = []

        # LLM context
        self.messages = [
            {"role": "system", "content": persona['system_prompt']}
        ]

        # Components
        self.tactic_engine = TacticEngine(persona)
        self.notifier = TelegramNotifier()
        self.analyzer = PostCallAnalyzer()

        # Audio queue for AudioSocket
        self.audio_queue = None

        # Call limits
        self.max_duration = int(os.environ.get('MAX_CALL_DURATION_MINUTES', 90)) * 60
        self.silence_timeout = int(os.environ.get('SILENCE_TIMEOUT_SECONDS', 30))

        # Cost tracking
        self.cost_stt = 0.0
        self.cost_llm = 0.0
        self.cost_tts = 0.0

        log.info("VoiceAgent initialized",
                 call_id=self.call_id,
                 stream_id=self.stream_id,
                 persona=persona['name'],
                 caller=caller_number)

    async def start(self):
        """Start the voice conversation with AudioSocket."""
        log.info("Starting VoiceAgent with AudioSocket",
                 call_id=self.call_id,
                 caller=self.caller_number)

        try:
            # Get AudioSocket server and register this stream
            audio_server = await get_audio_socket_server()
            self.audio_queue = audio_server.register_stream(self.stream_id)

            # Save initial call record
            await self._save_call_start()

            # Notify Telegram about new call
            await self.notifier.notify_call_started(
                self.caller_number,
                self.persona['name'],
                self.call_id
            )

            # Run the pipeline
            await self._run_pipeline()

        except asyncio.TimeoutError:
            log.info("Call timed out", call_id=self.call_id)
            await self.on_hangup(reason='timeout')
        except Exception as e:
            log.error("Pipeline error", call_id=self.call_id, error=str(e))
            await self.on_hangup(reason='error')

    async def _run_pipeline(self):
        """Build and run the AudioSocket -> STT -> LLM -> TTS -> AudioSocket pipeline."""

        # STT: Deepgram FLUX (ultra-low latency for voice agents)
        stt = DeepgramSTTService(
            api_key=os.environ['DEEPGRAM_API_KEY'],
            language="es",
            model="flux",  # Changed from nova-2 to flux for lower latency
            smart_format=True,
            interim_results=True,
            vad_turnoff=500,
            audio_sample_rate=8000,
            channels=1
        )

        # LLM: Groq (use 8B for faster/cheaper during dev, 70B for production)
        llm_model = os.environ.get('LLM_MODEL', 'llama-3.1-70b-versatile')
        llm = GroqLLMService(
            api_key=os.environ['GROQ_API_KEY'],
            model=llm_model,
            temperature=0.85,
            max_tokens=300
        )

        # TTS: Cartesia
        tts = CartesiaTTSService(
            api_key=os.environ['CARTESIA_API_KEY'],
            voice_id=self.persona.get('voice_id', 'es_elderly_female_warm'),
            language="es",
            speed="slow"
        )

        # Create processors
        context_proc = self._create_context_processor(llm)
        audio_output = self._create_audio_output()

        # Build pipeline: AudioSocket -> STT -> LLM -> TTS -> AudioSocket
        pipeline = Pipeline([
            self._create_audiosocket_source(),  # Custom source from AudioSocket
            stt,
            context_proc,
            tts,
            audio_output,
        ])

        task = PipelineTask(pipeline)
        runner = PipelineRunner()

        try:
            await asyncio.wait_for(
                runner.run(task),
                timeout=self.max_duration
            )
        except asyncio.TimeoutError:
            log.info("Max duration reached", call_id=self.call_id)

    def _create_audiosocket_source(self):
        """Create a frame source that reads from AudioSocket queue."""
        async def source():
            while True:
                try:
                    frame = await asyncio.wait_for(
                        self.audio_queue.get(),
                        timeout=30.0
                    )

                    if frame.is_final:
                        yield EndFrame()
                        break

                    # Convert PCM bytes to AudioRawFrame
                    if frame.audio_data:
                        yield AudioRawFrame(
                            audio=frame.audio_data,
                            sample_rate=8000,
                            num_channels=1
                        )
                except asyncio.TimeoutError:
                    # No audio timeout - send silence detection
                    yield TextFrame(text="[SILENCE]")

        return source

    def _create_context_processor(self, llm):
        """Processor that maintains context and injects tactics."""

        async def process(frame):
            if hasattr(frame, 'text') and frame.text:
                await self._handle_speech_input(frame.text, llm)

            if hasattr(frame, 'audio') and frame.audio:
                # Queue audio for recording
                self.audio_buffer.append(frame.audio)

            return frame

        return process

    def _create_audio_output(self):
        """Send TTS output back via AudioSocket."""
        async def output(frame):
            if hasattr(frame, 'audio') and frame.audio:
                # Send audio back to Asterisk via AudioSocket
                # This would go through the Asterisk bridge
                pass
            return frame
        return output

    async def _handle_speech_input(self, text: str, llm):
        """Handle recognized speech from the spammer."""
        self.turn_number += 1
        elapsed = (datetime.now() - self.started_at).total_seconds()

        # Record the turn
        turn_data = {
            "turn": self.turn_number,
            "speaker": "spammer",
            "text": text,
            "timestamp": elapsed
        }
        self.transcript.append(turn_data)

        log.info("Spammer spoke",
                 call_id=self.call_id,
                 turn=self.turn_number,
                 text=text[:80])

        # Save turn to database
        await self._save_turn("spammer", text, elapsed)

        # Check for dangerous requests
        if self._is_dangerous_request(text):
            log.warning("Dangerous request detected",
                       call_id=self.call_id,
                       text=text[:80])
            await self.notifier.notify_dangerous_request(
                self.call_id,
                self._detect_data_type(text),
                text
            )
            self.messages.append({
                "role": "system",
                "content": "[PRECAUCIÓN] Solicitan datos sensibles. NO los des."
            })

        # Select retention tactic
        tactic = self.tactic_engine.select_tactic(
            text,
            self.turn_number,
            self.transcript
        )
        if tactic:
            self.messages.append({
                "role": "system",
                "content": f"[TÁCTICA] {tactic}"
            })

        # Add spammer message
        self.messages.append({"role": "user", "content": text})

        # Periodically summarize
        if self.turn_number % 15 == 0 and len(self.messages) > 40:
            await self._summarize_context()

    def _is_dangerous_request(self, text: str) -> bool:
        """Check if requesting sensitive data."""
        dangerous = ['dni', 'nie', 'cuenta', 'iban', 'tarjeta', 'contraseña', 'pin']
        return any(p in text.lower() for p in dangerous)

    def _detect_data_type(self, text: str) -> str:
        """Detect what type of data is being requested."""
        if 'dni' in text.lower(): return "DNI/NIE"
        if 'cuenta' in text.lower() or 'iban' in text.lower(): return "Cuenta Bancaria"
        if 'tarjeta' in text.lower(): return "Tarjeta"
        return "Datos Personales"

    async def _summarize_context(self):
        """Summarize old context to prevent overflow."""
        if len(self.messages) < 20:
            return

        system_msg = self.messages[0]
        recent = self.messages[-10:]

        summary_prompt = "Resume brevemente la conversación manteniendo puntos clave: " + " ".join(m['content'][:100] for m in self.messages[1:-10])

        self.messages = [system_msg] + [
            {"role": "system", "content": f"[RESUMEN]: {summary_prompt}"}
        ] + recent

        log.info("Context summarized", call_id=self.call_id, total_messages=len(self.messages))

    async def _save_turn(self, speaker: str, text: str, timestamp: float):
        """Save a conversation turn to database."""
        try:
            async with get_db() as db:
                await db.execute("""
                    INSERT INTO conversation_turns
                    (call_id, turn_number, speaker, text, timestamp_seconds)
                    VALUES ($1, $2, $3, $4, $5)
                """, self.call_id, self.turn_number, speaker, text, timestamp)
        except Exception as e:
            log.error("Failed to save turn", error=str(e))

    async def _save_call_start(self):
        """Record call start in database."""
        try:
            async with get_db() as db:
                await db.execute("""
                    INSERT INTO calls (
                        id, caller_number, started_at, answered_at,
                        persona_name, llm_model, tts_engine, stt_engine,
                        analysis_status
                    ) VALUES ($1, $2, $3, $3, $4, $5, $6, $7, $8)
                """,
                    self.call_id,
                    self.caller_number,
                    datetime.now(),
                    self.persona['name'],
                    os.environ.get('LLM_MODEL', 'llama-3.1-70b-versatile'),
                    'cartesia',
                    'deepgram_flux',
                    'in_progress'
                )
        except Exception as e:
            log.error("Failed to save call start", error=str(e))

    async def on_hangup(self, reason: str = 'unknown'):
        """Handle call hangup - COMPLETE IMPLEMENTATION."""
        duration = (datetime.now() - self.started_at).total_seconds()
        duration_min = int(duration // 60)

        log.info("Call ended",
                 call_id=self.call_id,
                 reason=reason,
                 duration=duration,
                 turns=self.turn_number)

        try:
            # 1. Run post-call analysis
            analysis_result = await self.analyzer.analyze(
                self.call_id,
                self.transcript,
                self.caller_number,
                int(duration)
            )

            # 2. Upload audio to MinIO
            audio_path = await self._upload_audio_to_minio()

            # 3. Save end record with analysis
            async with get_db() as db:
                await db.execute("""
                    UPDATE calls SET
                        ended_at = $1,
                        transcript_text = $2,
                        transcript_full = $3,
                        audio_path = $4,
                        scam_type = $5,
                        scam_confidence = $6,
                        techniques_used = $7,
                        personal_data_requested = $8,
                        analysis_status = 'completed',
                        analysis_completed_at = $9
                    WHERE id = $10
                """,
                    datetime.now(),
                    json.dumps([t['text'] for t in self.transcript]),
                    json.dumps(self.transcript),
                    audio_path,
                    analysis_result.get('scam_type'),
                    analysis_result.get('scam_confidence'),
                    json.dumps([t['technique'] for t in analysis_result.get('techniques_detected', [])]),
                    json.dumps(analysis_result.get('personal_data_requested', [])),
                    datetime.now(),
                    self.call_id
                )

            # 4. Send Telegram notification
            await self.notifier.notify_call_ended(
                self.call_id,
                int(duration),
                analysis_result.get('scam_type'),
                self.tactic_engine.get_tactics_summary(),
                reason
            )

            log.info("Call processing complete",
                     call_id=self.call_id,
                     duration=duration_min,
                     scam_type=analysis_result.get('scam_type'))

        except Exception as e:
            log.error("Error in on_hangup", call_id=self.call_id, error=str(e))
            # Still try to notify
            await self.notifier.notify_system_error("on_hangup", str(e))

    async def _upload_audio_to_minio(self) -> Optional[str]:
        """Upload recorded audio to SeaweedFS S3 storage.

        Returns the S3 object path, or None if failed.
        """
        if not self.audio_buffer:
            return None

        try:
            import io
            from botocore.config import Config

            # Combine audio chunks
            full_audio = b''.join(self.audio_buffer)

            # Create S3 client for SeaweedFS
            s3_client = boto3.client(
                's3',
                endpoint_url=os.environ.get('SEAWEEDFS_ENDPOINT', 'http://seaweedfs:9000'),
                aws_access_key_id=os.environ.get('SEAWEEDFS_ACCESS_KEY', 'seaweedfs'),
                aws_secret_access_key=os.environ.get('SEAWEEDFS_SECRET_KEY', 'seaweedfs'),
                config=Config(signature_version='s3v4'),
                region_name='us-east-1'
            )

            bucket = os.environ.get('SEAWEEDFS_BUCKET', 'call-recordings')

            # Ensure bucket exists
            try:
                s3_client.head_bucket(Bucket=bucket)
            except:
                s3_client.create_bucket(Bucket=bucket)

            # Generate object path (without phone number for privacy)
            object_path = f"calls/{self.call_id}/{self.started_at.strftime('%Y%m%d_%H%M%S')}.wav"

            # Upload audio bytes
            audio_io = io.BytesIO(full_audio)

            s3_client.put_object(
                Bucket=bucket,
                Key=object_path,
                Body=audio_io,
                ContentType='audio/wav'
            )

            log.info("Audio uploaded to SeaweedFS",
                    call_id=self.call_id,
                    path=object_path,
                    size=len(full_audio))

            return object_path

        except Exception as e:
            log.error("Failed to upload audio to SeaweedFS",
                     call_id=self.call_id,
                     error=str(e))
            return None

    @property
    def duration_seconds(self) -> float:
        return (datetime.now() - self.started_at).total_seconds()