"""Handles incoming calls from Asterisk ARI."""
import asyncio
import structlog
import os
import ari
from voice_agent import VoiceAgent
from database.connection import get_db
from persona_manager import PersonaManager

log = structlog.get_logger()


class CallHandler:
    def __init__(self):
        self.asterisk_host = os.environ.get('ASTERISK_HOST', 'asterisk')
        self.ari_user = os.environ.get('ASTERISK_ARI_USER', 'honeypot-user')
        self.ari_password = os.environ.get('ASTERISK_ARI_PASSWORD', 'password')
        self.active_calls = {}
        self.persona_manager = PersonaManager()

        log.info("CallHandler initialized",
                host=self.asterisk_host,
                user=self.ari_user)

    async def start(self):
        """Connect to Asterisk ARI and listen for calls."""
        client = ari.connect(
            f'http://{self.asterisk_host}:8088',
            self.ari_user,
            self.ari_password
        )

        # Register event handlers
        client.on_channel_event('StasisStart', self.on_call_start)
        client.on_channel_event('StasisEnd', self.on_call_end)
        client.on_channel_event('ChannelEnteredBridge', self.on_bridge_enter)
        client.on_channel_event('ChannelLeftBridge', self.on_bridge_leave)

        log.info("Connected to Asterisk ARI", app="honeypot-app")

        # Keep connection alive - this blocks forever
        await asyncio.get_event_loop().run_in_executor(
            None, client.run, 'honeypot-app'
        )

    async def on_call_start(self, channel, event):
        """Handle new incoming call."""
        caller_number = channel.json.get('caller', {}).get('number', 'unknown')
        channel_id = channel.json.get('id', 'unknown')
        channel_name = channel.json.get('name', 'unknown')

        log.info("New incoming call",
                 caller=caller_number,
                 channel_id=channel_id,
                 channel_name=channel_name)

        # Save call to database
        try:
            async with get_db() as db:
                call_id = await db.fetchval("""
                    INSERT INTO calls (caller_number, started_at, analysis_status)
                    VALUES ($1, NOW(), 'pending')
                    RETURNING id::text
                """, caller_number)
                log.info("Call saved to database", call_id=call_id)
        except Exception as e:
            log.error("Failed to save call to database", error=str(e))

        # Select best persona for this caller
        persona = await self.persona_manager.get_best_persona(caller_number)

        # Create voice agent for this call
        agent = VoiceAgent(
            channel=channel,
            caller_number=caller_number,
            persona=persona
        )

        self.active_calls[channel.id] = agent

        # Start conversation in background
        asyncio.create_task(agent.start())

    async def on_call_end(self, channel, event):
        """Handle call ended."""
        if channel.id in self.active_calls:
            agent = self.active_calls[channel.id]
            await agent.on_hangup()
            del self.active_calls[channel.id]

            log.info("Call ended",
                     channel_id=channel.id,
                     duration=agent.duration_seconds,
                     turns=agent.turn_number)
        else:
            log.info("Call ended but no agent found",
                     channel_id=channel.id)

    async def on_bridge_enter(self, channel, event):
        """Handle channel entering a bridge (for monitoring)."""
        log.debug("Channel entered bridge",
                  channel_id=channel.id,
                  bridge_id=event.get('bridge', {}).get('id'))

    async def on_bridge_leave(self, channel, event):
        """Handle channel leaving a bridge."""
        log.debug("Channel left bridge",
                  channel_id=channel.id)