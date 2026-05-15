"""Tactic Engine - Dynamic retention strategy for spam calls."""
import random
import structlog
from typing import Dict, Any, List, Optional

log = structlog.get_logger()


class TacticEngine:
    """Selects and manages retention tactics to keep spammers on the line."""

    TACTIC_DEFINITIONS = {
        "buscar_papeles": {
            "description": "Buscar documentos/papeles en cajones",
            "delay_seconds": 45,
            "phrases": [
                "Aguarde que tengo que buscar los papeles, están en el cajón de la mesilla...",
                "No sé dónde puse el contrato, déjeme ver en el armario...",
                "Espere que tengo que buscar en el archivador, ahora mismo..."
            ],
            "triggers": ["contrato", "firma", "papeles", "documento", "condiciones"]
        },
        "consulta_hijo": {
            "description": "Consultar con el hijo/familiar",
            "delay_seconds": 30,
            "phrases": [
                "Esto es mejor que lo hable con mi hijo, llame mañana a las 10",
                "Mi hija me ha dicho que nunca decida estas cosas por teléfono",
                "Tengo que consultar con mi familia, no puedo decidir sola"
            ],
            "triggers": ["ahora", "hoy", "urgente", "decidir", "aceptar"]
        },
        "problema_auditivo": {
            "description": "Problemas de audición - pedir que repitan",
            "delay_seconds": 15,
            "phrases": [
                "Hable más alto por favor, que oigo fatal con este teléfono",
                "¿Cómo dice? No le entiendo bien, tenga paciencia conmigo",
                "¿Puede repetir eso? Es que oigo muy mal de un oído"
            ],
            "triggers": []
        },
        "duda_seguridad": {
            "description": "Expresar dudas sobre legitimidad",
            "delay_seconds": 25,
            "phrases": [
                "Antes tengo que preguntar en el banco si es de fiar...",
                "¿Cómo puedo saber que esto es cierto?",
                "Déjeme verificar el número de la empresa, no me fío de llamadas"
            ],
            "triggers": ["empresa", "oficina", "banco", "oficial"]
        },
        "peticion_identificacion": {
            "description": "Pedir datos de identificación del interlocutor",
            "delay_seconds": 20,
            "phrases": [
                "Deme su número de empleado y el nombre de la empresa para llamar yo luego",
                "¿Me puede dar un número de expediente o referencia?",
                "Necesito el nombre completo y el DNI del representante"
            ],
            "triggers": ["empresa", "compañía", "servicio"]
        },
        "burocracia_ligera": {
            "description": "Exigir documentación escrita",
            "delay_seconds": 15,
            "phrases": [
                "Necesito que me mande un escrito certificado, no puedo decidir así por teléfono",
                "Mándelo por correo postal certificado, por favor",
                "Sin un documento oficial no puedo hacer nada"
            ],
            "triggers": ["aceptar", "contratar", "ahora"]
        },
        "cambio_tema_suave": {
            "description": "Cambiar tema para ganar tiempo",
            "delay_seconds": 20,
            "phrases": [
                "Y Dígame, ¿hace mucho que trabaja en eso? Qué interesante...",
                "Antes de nada, ¿qué tiempo hace ahí donde está usted?",
                "¿Usted es de Madrid? Yo estuve una vez de vacaciones..."
            ],
            "triggers": []
        },
        "confusion_tecnologica": {
            "description": "Expresar confusión con tecnología",
            "delay_seconds": 30,
            "phrases": [
                "Pero eso del ordinador... ¿eso qué es? Yo de eso no entiendo nada",
                "Mi nieto me ha dicho que no toque nada de eso, que me confundo",
                "Para mí que estos teléfonos son todos iguales, muy complicados"
            ],
            "triggers": ["internet", "online", "web", "correo", "email", "computadora"]
        }
    }

    def __init__(self, persona: Dict[str, Any]):
        self.persona = persona
        self.tactics: List[str] = persona.get('tactics', [])
        self.last_tactic: Optional[str] = None
        self.tactic_history: List[str] = []
        self.turns_since_tactic = 0
        self.silence_response_ms = persona.get('silence_response_ms', 4000)
        self.max_silence_loops = persona.get('max_silence_loops', 5)
        self.silence_count = 0

        log.info("TacticEngine initialized",
                persona=persona.get('name'),
                available_tactics=self.tactics)

    def select_tactic(self, caller_text: str, turn_number: int,
                     transcript: List[Dict]) -> Optional[str]:
        """Select the best tactic based on caller input and call state."""
        self.turns_since_tactic += 1

        if self.turns_since_tactic >= random.randint(5, 8):
            tactic = self._select_random_tactic()
            self._record_tactic_use(tactic)
            return self._build_tactic_instruction(tactic)

        caller_lower = caller_text.lower()
        triggered_tactic = self._check_triggers(caller_lower)
        if triggered_tactic and triggered_tactic != self.last_tactic:
            self._record_tactic_use(triggered_tactic)
            return self._build_tactic_instruction(triggered_tactic)

        if self._is_pressure_situation(caller_lower):
            defensive = ["consulta_hijo", "problema_auditivo", "burocracia_ligera"]
            available = [t for t in defensive if t in self.tactics]
            if available:
                tactic = random.choice(available)
                self._record_tactic_use(tactic)
                return self._build_tactic_instruction(tactic)

        return None

    def _check_triggers(self, caller_text: str) -> Optional[str]:
        for tactic_name in self.tactics:
            if tactic_name in self.TACTIC_DEFINITIONS:
                triggers = self.TACTIC_DEFINITIONS[tactic_name].get('triggers', [])
                if any(trigger in caller_text for trigger in triggers):
                    return tactic_name
        return None

    def _is_pressure_situation(self, text: str) -> bool:
        pressure_indicators = [
            "ahora mismo", "sin tardar", "no puede esperar", "urgente",
            " tiene que", " inmediatamente", " ya mismo", "rápido"
        ]
        return any(indicator in text for indicator in pressure_indicators)

    def _select_random_tactic(self) -> str:
        available = [t for t in self.tactics if t != self.last_tactic]
        if not available:
            available = self.tactics
        return random.choice(available)

    def _record_tactic_use(self, tactic: str):
        self.last_tactic = tactic
        self.tactic_history.append(tactic)
        self.turns_since_tactic = 0

    def _build_tactic_instruction(self, tactic_name: str) -> str:
        if tactic_name not in self.TACTIC_DEFINITIONS:
            return ""

        tactic_def = self.TACTIC_DEFINITIONS[tactic_name]
        phrase = random.choice(tactic_def['phrases'])

        return (
            f"[APLICAR TÁCTICA: {tactic_name}]\n"
            f"Usa esta frase: \"{phrase}\"\n"
            f"Después de la frase, haz una pausa de {tactic_def['delay_seconds']} segundos."
        )

    def get_silence_response(self) -> str:
        self.silence_count += 1

        if self.silence_count > self.max_silence_loops:
            return "[POSIBLE COLGAR] El spammer lleva mucho en silencio."

        filler_phrases = [
            "¿Sigue ahí usted?",
            "¿Se ha cortado la llamada?",
            "Ay, estos teléfonos modernos...",
            "¿Hola? ¿Me oye?",
            "Perdone, le estaba escuchando..."
        ]

        return random.choice(filler_phrases)

    def reset_silence_count(self):
        self.silence_count = 0

    def get_tactics_summary(self) -> Dict[str, int]:
        summary = {}
        for tactic in self.tactic_history:
            summary[tactic] = summary.get(tactic, 0) + 1
        return summary