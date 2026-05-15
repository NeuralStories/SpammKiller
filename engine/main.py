"""SCAMEATER Engine - Main entry point."""
import asyncio
import structlog
import os
import uuid
from audiosocket_server import AudioSocketServer
from voice_agent import VoiceAgent
from database.connection import init_db, close_db
from persona_manager import PersonaManager

log = structlog.get_logger()
persona_manager = PersonaManager()

async def on_audiosocket_connection(call_id, reader, writer):
    """Callback when Asterisk connects via AudioSocket."""
    log.info(f"New call received via AudioSocket. Call ID: {call_id}")
    
    # Select persona (fallback to unknown caller for now)
    persona = await persona_manager.get_best_persona("unknown")
    
    # Spawn VoiceAgent
    agent = VoiceAgent(
        reader=reader,
        writer=writer,
        call_id=call_id,
        caller_number="unknown",
        persona=persona
    )
    
    # Run agent in background
    asyncio.create_task(agent.start())


async def main():
    log.info("SCAMEATER Engine starting (AudioSocket Mode)...")

    # Initialize database connection
    await init_db()
    log.info("Database connected")

    # Start AudioSocket Server on port 9010
    port = int(os.environ.get('AUDIOSOCKET_PORT', 9010))
    server = AudioSocketServer('0.0.0.0', port, on_audiosocket_connection)
    
    await server.start()

    log.info(f"Engine running. Waiting for Asterisk AudioSocket connections on port {port}...")
    
    # Run forever
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await server.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Shutting down...")
    finally:
        asyncio.run(close_db())