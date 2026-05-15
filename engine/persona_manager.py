"""Manages personas (AI characters) for call handling."""
import json
import os
import structlog
from typing import Optional, Dict, Any

log = structlog.get_logger()


class PersonaManager:
    def __init__(self):
        self.default_persona = {
            'id': 'default',
            'name': 'carmen',
            'display_name': 'Carmen',
            'system_prompt': self._load_carmen_prompt(),
            'voice_id': 'es_elderly_female_warm',
            'tactics': [
                'buscar_papeles',
                'consulta_hijo',
                'problema_auditivo',
                'duda_seguridad',
                'peticion_identificacion',
                'burocracia_ligera',
                'cambio_tema_suave',
                'confusion_tecnologica'
            ],
            'silence_response_ms': 4000,
            'max_silence_loops': 5
        }

    def _load_carmen_prompt(self) -> str:
        """Load the Carmen persona prompt from file if exists, otherwise use default."""
        prompt_path = '/app/packages/prompts/carmen.md'
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r') as f:
                return f.read()

        # Default prompt if file not found
        return """Eres Carmen, una jubilada española de 78 años. Vives sola en un pueblo de Guadalajara.

REGLAS ABSOLUTAS:
1. NUNCA des tu DNI, número de cuenta, ni ningún dato personal.
2. Si te piden datos, di que los tiene tu hijo y que tienes que consultar con él.
3. Siempre hablas muy despacio y a veces pides que repitan.
4. Si alguien se enfada, dices que mejor llamas a tu hijo.
5. Nunca aceptes enlaces ni instales nada.

TÁCTICAS DE RETENCIÓN:
- buscar_papeles: "Aguarde que tengo que buscar los papeles..."
- consulta_hijo: "Esto es mejor que lo hable con mi hijo..."
- problema_auditivo: "Hable más alto por favor..."
- duda_seguridad: "Antes tengo que preguntar en el banco..."
- peticion_identificacion: "Deme su número de empleado..."
- burocracia_ligera: "Necesito que me mande un escrito..."
- cambio_tema_suave: "Y Dígame, ¿hace mucho que trabaja en eso?"
"""

    async def get_best_persona(self, caller_number: str) -> Dict[str, Any]:
        """Select the best persona for a given caller.

        For MVP, always returns Carmen. In future versions,
        this could select based on caller history, time of day, etc.
        """
        log.info("Selecting persona for call",
                 caller=caller_number,
                 persona=self.default_persona['name'])
        return self.default_persona

    async def get_persona_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific persona by name."""
        if name == 'carmen':
            return self.default_persona
        return None