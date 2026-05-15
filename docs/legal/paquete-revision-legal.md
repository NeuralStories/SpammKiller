# Paquete de Revisión Legal (Versión Consolidada)

**Proyecto:** SCAMEATER
**Fecha:** Mayo 2026

## 1. Alcance Defensivo Estricto
Este sistema se define y limita técnicamente como un *honeypot* pasivo (trampa de miel).
- **Prohibición de llamadas salientes:** El sistema **nunca** originará llamadas telefónicas. El dialplan de Asterisk está bloqueado (fail-closed) para impedir cualquier intento de marcación hacia el exterior.
- **Intercepción consensuada:** Al ser los titulares de la línea, tenemos derecho a grabar la llamada que se nos realiza para documentar abusos, en conformidad con la jurisprudencia española sobre grabaciones propias. No obstante, por máxima garantía, el motor redacta activamente y elimina PII (Datos de Carácter Personal) detectados en tiempo real.

## 2. Retención y Manejo de Datos (AEPD)
- El audio crudo en MinIO (y transcripciones en PostgreSQL) tiene un ciclo de vida configurado a 30 días, transcurridos los cuales se destruye automáticamente.
- **Anonimización:** El analizador PNL destruye patrones como DNI, cuentas bancarias e IBAN explícitos antes del volcado a la tabla de inteligencia (`api_usage` / `conversation_turns`).
- La base de datos no es de acceso público. Está aislada dentro del VPS y solo es accesible por el dashboard autenticado.

## 3. Cumplimiento de Normativa de Numeración 400 (Octubre 2026)
A partir de la Resolución en España, la numeración 400 es mandatoria para ciertos tipos de llamadas comerciales y analíticas empresariales. 
El sistema usará un troncal SIP con numeración validada (Zadarma) para garantizar que las terminaciones y el caller ID entrante sigan las regulaciones vigentes y nuestra respuesta no esté catalogada como comportamiento fraudulento en la red de la operadora.

**Aprobado para Operación por:** Equipo de Operaciones SCAMEATER.