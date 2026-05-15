"""Post-call analysis: scam classification, technique detection, fingerprinting."""
import json
import structlog
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

log = structlog.get_logger()


class PostCallAnalyzer:
    """Analyzes completed calls to classify scam type, detect techniques, and generate fingerprint."""

    # 16 scam categories
    SCAM_CATEGORIES = {
        "energia": ["luz", "gas", "factura", "energía", " compañía"],
        "telecomunicaciones": ["teléfono", "internet", "fibra", "móvil", "operador"],
        "banca": ["banco", "cuenta", "transferencia", "bizum", "visa"],
        "inversion": ["invertir", "bolsa", "fondos", "rendimiento", "dinero"],
        "cripto": ["bitcoin", "criptomonedas", "wallet", "blockchain"],
        "seguro": ["seguro", " póliza", "cobertura", "siniestro"],
        "loteria": ["premio", "lotería", "sorteo", "ganador"],
        "herencia": ["herencia", "abogado", "tribunal", "testamento"],
        "tech_support": ["ordenador", "computer", "microsoft", "windows", "apple", "hack"],
        "spam_general": ["oferta", "descuento", "promoción", "gratis"],
        "suplantacion_gobierno": [" Seguridad Social", "ayuntamiento", "policía", "guardia civil", "tax", "hacienda"],
        "vacaciones": ["hotel", "vuelo", "vacaciones", "reserva", "viaje"],
        "empleo": ["trabajo", "empleo", "curriculum", "oferta laboral"],
        " Dating/romance": [" cita", "amor", "relación", "pareja"],
        " Bezos/amazon": ["paquete", "envío", "amazon", "reembolso"],
        "otro": []
    }

    # 14 scam techniques
    SCAM_TECHNIQUES = {
        "authority": ["autoridad", "director", "gerente", "oficina", "oficial"],
        "urgency": ["ahora", "inmediato", "urgente", "hoy", "caduca", "plazo"],
        "fear": [" multar", "denunciar", "guardia civil", "policía", "juicio", "celda"],
        "scarcity": ["quedan", "último", "plazas", "oferta limitada", "ahora o nunca"],
        "social_proof": [" miles de personas", "todos", "muchos", "mejor", "más vendido"],
        "liking": ["amigo", "querido", "apreciado", "familiar"],
        "reciprocity": ["gratis", "regalo", "premio", "obsequio", "sin compromiso"],
        "commitment": ["firme", "acepta", "confirmar", "acepto"],
        "deception": ["suplant", "falso", "mentira", "engañ"],
        "technical_jargon": ["servidor", "ip", "protocolo", "encript"],
        "emotional_manipulation": ["familia", "niños", "abuelo", "hermano"],
        "unverifiable": ["no puedo", "no existe", "no hay registro"],
        "pressure_tactic": ["sin tiempo", "no puedo esperar", "decide ahora"],
        "data_request": ["dni", "cuenta", "iban", "tarjeta", "contraseña"]
    }

    async def analyze(self, call_id: str, transcript: List[Dict],
                      caller_number: str, duration_seconds: int) -> Dict[str, Any]:
        """Run full analysis on a completed call.
        
        Returns a dict with:
        - scam_type, scam_confidence
        - techniques_detected (with evidence)
        - fingerprint (text hash for campaign matching)
        - personal_data_requested
        - caller_emotion_timeline
        """
        log.info("Starting post-call analysis", call_id=call_id)
        
        # Combine all spammer text
        spammer_text = " ".join(
            t['text'] for t in transcript 
            if t.get('speaker') == 'spammer'
        ).lower()
        
        # Classify scam type
        scam_type, scam_confidence = await self._classify_scam(spammer_text)
        
        # Detect techniques
        techniques = self._detect_techniques(spammer_text)
        
        # Generate fingerprint
        fingerprint = self._generate_fingerprint(transcript)
        
        # Check for data requests
        data_requests = self._detect_data_requests(spammer_text)
        
        # Analyze emotion timeline
        emotion_timeline = self._analyze_emotions(transcript)
        
        result = {
            "call_id": call_id,
            "scam_type": scam_type,
            "scam_confidence": scam_confidence,
            "techniques_detected": techniques,
            "fingerprint": fingerprint,
            "personal_data_requested": data_requests,
            "caller_emotion_timeline": emotion_timeline,
            "analysis_completed_at": datetime.now().isoformat()
        }
        
        log.info("Post-call analysis complete",
                 call_id=call_id,
                 scam_type=scam_type,
                 confidence=scam_confidence,
                 techniques=len(techniques))
        
        return result

    async def _classify_scam(self, text: str) -> Tuple[str, float]:
        """Classify the scam type based on keywords."""
        scores = {}
        
        for category, keywords in self.SCAM_CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score
        
        if not scores:
            return "otro", 0.5
        
        # Get best match
        best = max(scores, key=scores.get)
        confidence = min(scores[best] / 3.0, 0.95)  # Cap at 0.95
        
        return best, confidence

    def _detect_techniques(self, text: str) -> List[Dict[str, Any]]:
        """Detect scam techniques with textual evidence."""
        detected = []
        
        for technique, keywords in self.SCAM_TECHNIQUES.items():
            for kw in keywords:
                if kw in text:
                    # Find the sentence containing this keyword
                    sentences = text.split('.')
                    evidence = next(
                        (s.strip() for s in sentences if kw in s),
                        kw
                    )
                    detected.append({
                        "technique": technique,
                        "evidence": evidence[:200],
                        "keyword": kw
                    })
                    break  # Only record once per technique
        
        return detected

    def _generate_fingerprint(self, transcript: List[Dict]) -> str:
        """Generate a hash fingerprint of the call script for campaign detection.
        
        Based on: opening, entity impersonated, reason, data requested, closing.
        """
        spammer_turns = [t['text'] for t in transcript if t.get('speaker') == 'spammer']
        
        if not spammer_turns:
            return ""
        
        # First 3 and last 2 turns define the script pattern
        pattern_text = " ".join(spammer_turns[:3] + spammer_turns[-2:])
        
        # Simple hash for fingerprint (not cryptographic, just for comparison)
        fingerprint = sum(ord(c) for c in pattern_text.lower() if c.isalnum())
        
        return str(fingerprint % (10**9))

    def _detect_data_requests(self, text: str) -> List[str]:
        """Detect what types of personal data were requested."""
        data_patterns = {
            "DNI/NIE": ["dni", "nie", "documento"],
            "IBAN/Cuenta": ["iban", "cuenta", "número de cuenta", "ccc"],
            "Tarjeta": ["tarjeta", "cvv", "cvc", "débito", "crédito"],
            "Contraseña": ["contraseña", "password", "pin", "clave"],
            "Teléfono": ["móvil", "celular", "número"],
            "Dirección": ["dirección", "domicilio", "calle"],
            "Email": ["correo", "email", "mail"]
        }
        
        requested = []
        for data_type, patterns in data_patterns.items():
            if any(p in text for p in patterns):
                requested.append(data_type)
        
        return requested

    def _analyze_emotions(self, transcript: List[Dict]) -> List[Dict]:
        """Analyze the emotional arc of the spammer across the call."""
        # Simple keyword-based emotion detection
        emotion_keywords = {
            "frustrated": ["bueno", "vale", "escucha", "mire", "oye", "pero"],
            "aggressive": ["cabrón", "gilipolla", "coño", "joder", "hostia"],
            "impatient": ["rápido", "ya", "llevo", "tiempo", "esperando"],
            "calm": ["sí", "vale", "correcto", "bueno", "de acuerdo"],
            "nervous": ["eh", "a ver", "bueno", "mire", "verá"]
        }
        
        timeline = []
        for turn in transcript:
            if turn.get('speaker') != 'spammer':
                continue
            
            text = turn['text'].lower()
            detected_emotions = [
                emotion for emotion, kws in emotion_keywords.items()
                if any(kw in text for kw in kws)
            ] or ["neutral"]
            
            timeline.append({
                "turn": turn['turn'],
                "timestamp": turn.get('timestamp', 0),
                "emotions": detected_emotions
            })
        
        return timeline

    def redact_sensitive_data(self, text: str) -> str:
        """Redact personal data from text for safe display."""
        import re
        
        # DNI/NIE pattern
        text = re.sub(
            r'\b\d{8}[A-Z]\b', '[DNI_REDACTADO]', text
        )
        text = re.sub(
            r'\b[XYZ]\d{7}[A-Z]\b', '[NIE_REDACTADO]', text
        )
        
        # IBAN
        text = re.sub(
            r'\bES\d{2}[ ]?\d{4}[ ]?\d{4}[ ]?\d{4}[ ]?\d{4}[ ]?\d{4}\b',
            '[IBAN_REDACTADO]', text
        )
        
        # Credit card
        text = re.sub(
            r'\b\d{4}[ ]?\d{4}[ ]?\d{4}[ ]?\d{4}\b',
            '[TARJETA_REDACTADA]', text
        )
        
        # Phone numbers
        text = re.sub(
            r'\b\+?\d{9,15}\b',
            '[TELÉFONO_REDACTADO]', text
        )
        
        return text