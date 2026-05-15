# Alcance Defensivo - SCAMEATER

## Finalidad del sistema
SCAMEATER es un sistema honeypot conversacional diseñado exclusivamente para:
- Recibir llamadas entrantes no solicitadas (spam telefónico).
- Analizar y registrar patrones de fraude para investigación defensiva.
- Generar inteligencia sobre metodologías de estafa sin almacenar datos personales reales.

## Alcance: Únicamente llamadas entrantes
- El sistema SÓLO recibe llamadas. Las llamadas salientes están bloqueadas por configuración.
- No se realiza ninguna acción automática que afecte a terceros fuera del sistema.

## Prohibiciones absolutas
- NO revelar números de teléfono reales de la base de datos a usuarios no autorizados.
- NO acusar automáticamente a ninguna organización de fraude (toda clasificación requiere revisión manual).
- NO clonar voces de personas reales.
- NO publicar números de spammer en listas públicas.
- NO almacenar datos personales reales (DNI, IBAN, cuentas) más allá de lo necesario para análisis.
- NO realizar devoluciones de llamada automáticas.

## Limitaciones del análisis automático
- El análisis de IA puede cometer errores. Toda clasificación de scam debe poder ser revisada.
- El campo `scam_confidence` indica la confianza del modelo (0.0-1.0).
- Clasificaciones con confianza < 0.65 requieren revisión manual obligatoria.

## Marco legal de referencia
- RGPD (Reglamento General de Protección de Datos)
- Ley Orgánica 3/2018 de Protección de Datos Personales y garantía de los derechos digitales
- Ley 9/2014 General de Telecomunicaciones (modificada)
- Circular 1/2023 de la AEPD sobre spam
- Numeración 400 (obligatoria desde octubre 2026)

## Proprietario
Este documento forma parte del paquete de revisión legal para uso interno.