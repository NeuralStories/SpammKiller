"""Telegram notifications for real-time call alerts."""
import asyncio
import httpx
import structlog
import os
from typing import Optional, Dict, Any
from datetime import datetime

log = structlog.get_logger()


class TelegramNotifier:
    """Sends alerts to Telegram when important events occur.
    
    Alerts are sent for:
    - New call started
    - Call ended (with summary)
    - High-value target detected (bank, gov impersonation)
    - Dangerous data requested (DNI, IBAN, etc.)
    - System errors
    """

    def __init__(self):
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        self.enabled = bool(self.bot_token and self.chat_id)
        
        if not self.enabled:
            log.warning("Telegram notifications disabled: missing bot token or chat_id")
        else:
            log.info("Telegram notifications enabled")

    async def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
        """Send a message to the configured Telegram chat."""
        if not self.enabled:
            return False

        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                response = await client.post(url, json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                }, timeout=10.0)
                
                if response.status_code == 200:
                    log.debug("Telegram message sent", text=text[:50])
                    return True
                else:
                    log.error("Telegram send failed",
                             status=response.status_code,
                             response=response.text)
                    return False
        except Exception as e:
            log.error("Telegram error", error=str(e))
            return False

    async def notify_call_started(self, caller_number: str, persona: str, call_id: str):
        """Alert when a new spam call is detected."""
        display_number = self._redact_number(caller_number)
        
        message = (
            f"🕷️ *Nueva Llamada Detectada*\n\n"
            f"📞 Caller: `{display_number}`\n"
            f"🎭 Persona: {persona}\n"
            f"🆔 ID: `{call_id[:8]}`\n"
            f"⏰ Hora: {datetime.now().strftime('%H:%M:%S')}"
        )
        await self.send_message(message)

    async def notify_call_ended(self, call_id: str, duration_seconds: int,
                                 scam_type: Optional[str], 
                                 tactics_used: list,
                                 hangup_reason: str):
        """Alert when a call ends with summary."""
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        
        tactics_str = ", ".join(tactics_used[:5]) if tactics_used else "Ninguna"
        
        message = (
            f"📴 *Llamada Finalizada*\n\n"
            f"🆔 ID: `{call_id[:8]}`\n"
            f"⏱️ Duración: {minutes}m {seconds}s\n"
            f"🏷️ Tipo scam: {scam_type or 'No clasificado'}\n"
            f"🎯 Tácticas: {tactics_str}\n"
            f"📌 Finalizó por: {hangup_reason}"
        )
        await self.send_message(message)

    async def notify_dangerous_request(self, call_id: str, 
                                        request_type: str,
                                        full_text: str):
        """Alert when spammer asks for sensitive data."""
        message = (
            f"🚨 *Solicitud Peligrosa Detectada*\n\n"
            f"🆔 Llamada: `{call_id[:8]}`\n"
            f"⚠️ Tipo: `{request_type}`\n"
            f"💬 \"{full_text[:200]}...\""
        )
        await self.send_message(message)

    async def notify_high_value_target(self, call_id: str,
                                        impersonated: str,
                                        caller_number: str):
        """Alert when high-value target (bank, government) is impersonated."""
        display_number = self._redact_number(caller_number)
        
        message = (
            f"🏦 *Objetivo de Alto Valor*\n\n"
            f"🆔 Llamada: `{call_id[:8]}`\n"
            f"🏛️ Suplantando: {impersonated}\n"
            f"📞 Caller: `{display_number}`\n"
            f"⚡ Verificar manualmente"
        )
        await self.send_message(message)

    async def notify_system_error(self, error_type: str, details: str):
        """Alert for system errors that need attention."""
        message = (
            f"❌ *Error del Sistema*\n\n"
            f"🔧 Tipo: `{error_type}`\n"
            f"📝 Details: {details[:300]}"
        )
        await self.send_message(message)

    def _redact_number(self, number: str) -> str:
        """Partially redact phone number for privacy."""
        if len(number) <= 4:
            return "****"
        return number[:3] + "****" + number[-2:]
