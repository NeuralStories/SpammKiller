# Mapa de Datos Tratados - SCAMEATER

| Dato | Tipo | Retención | Acceso | Notas |
|------|------|-----------|--------|-------|
| Número llamante (hash) | Personal | 90 días | admin, legal | SHA-256 para búsqueda |
| Número llamante (cifrado) | Personal | 90 días | legal only | AES-256, descifrado restringido |
| Audio de llamada | Voz/Biometría | 30 días | admin only | Cifrado en reposo |
| Transcripción completa | Datos derivados | 90 días | analyst+ | Redacción automática |
| Transcripción redactada | Datos derivados | 2 años | all users | Sin datos personales |
| País/Región/Ciudad | Geolocalización | 2 años | analyst+ | Anonimizable |
| Operador/carrier | Técnico | 2 años | analyst+ | - |
| Tipo de línea (VOIP/Fijo) | Técnico | 2 años | analyst+ | - |
| Embeddings de voz | Biométrico | 1 año | admin only | Vectores 768d |
| Coste de API | Financiero | 5 años | admin only | No personal |
| Marcas de tiempo | Técnico | 2 años | analyst+ | - |

## Datos que NO se almacenan
- Contenido exacto de datos personales mencionados por el spammer (se marcan como [REDACTADO])
- IP del llamante (no disponible vía SIP)
- Grabación sin consentimiento explícito (todas las llamadas son entrantes)

## Métricas de cumplimiento
- Auditoría de accesos: tabla `audit_log` registra cada consulta a datos sensibles.
- Rotación de claves: cada 6 meses.
- Revisión de retención: job automático mensual.