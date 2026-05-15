"""AudioSocket TCP Server for bridging Asterisk to Python."""
import asyncio
import structlog
import uuid
import struct
from typing import Callable, Awaitable

log = structlog.get_logger()

# AudioSocket constants
AUDIOSOCKET_KIND_HANGUP = 0x00
AUDIOSOCKET_KIND_ID = 0x01
AUDIOSOCKET_KIND_SILENCE = 0x02
AUDIOSOCKET_KIND_SLIN = 0x10
AUDIOSOCKET_KIND_ERROR = 0xff

class AudioSocketServer:
    """Async TCP server that implements the Asterisk AudioSocket protocol."""
    
    def __init__(self, host: str, port: int, on_connection: Callable):
        self.host = host
        self.port = port
        self.on_connection = on_connection # Callback: async def on_conn(call_id, reader, writer)
        self.server = None

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        addrs = ', '.join(str(sock.getsockname()) for sock in self.server.sockets)
        log.info(f"AudioSocket server listening on {addrs}")
        
    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            log.info("AudioSocket server stopped")

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_addr = writer.get_extra_info('peername')
        log.info(f"New AudioSocket connection from {client_addr}")
        
        call_id = None
        
        try:
            # Read first payload: ID payload (UUID of the call)
            # AudioSocket header: 3 bytes payload length (little endian), 1 byte kind
            header = await reader.readexactly(3)
            length = int.from_bytes(header, byteorder='little')
            
            kind_byte = await reader.readexactly(1)
            kind = kind_byte[0]
            
            if kind == AUDIOSOCKET_KIND_ID:
                payload = await reader.readexactly(length)
                try:
                    # Payload is the 16 byte UUID
                    call_id = str(uuid.UUID(bytes=payload))
                    log.info(f"AudioSocket Call ID registered: {call_id}")
                except Exception as e:
                    log.error(f"Failed to parse UUID: {e}")
                    call_id = "unknown"
            else:
                log.warning(f"Unexpected initial payload kind: {kind}")
                return

            # Pass the reader, writer and call_id to the handler
            await self.on_connection(call_id, reader, writer)
            
        except asyncio.IncompleteReadError:
            log.info("AudioSocket client disconnected during handshake")
        except Exception as e:
            log.error(f"AudioSocket error handling client: {e}")
        finally:
            log.info(f"Closing AudioSocket connection for call {call_id}")
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
