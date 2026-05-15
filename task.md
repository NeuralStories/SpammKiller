# SCAMEATER — Task de Fabricación para Modelo Inferior

## Notas de Mejora Detectadas (Investigación Mayo 2026)

> [!IMPORTANT]
> **AudioSocket > ExternalMedia**: La investigación confirma que AudioSocket es ahora el método preferido sobre ExternalMedia para streaming de audio con IA. Más simple, menor latencia, TCP directo.

> [!IMPORTANT]
> **Llama 4 disponible en Groq**: Llama 4 Scout (17B activos/109B total) y Maverick (17B/400B) ya están en Groq. Considerar Scout como upgrade sobre llama-3.3-70b.

> [!IMPORTANT]
> **AssemblyAI Universal-3 Pro**: El fallback STT ha evolucionado a Universal-3 Pro Streaming ($0.45/hr, ~300ms latencia, 6 idiomas con code-switching).

> [!WARNING]
> **MinIO CE**: La Community Edition está efectivamente EOL para nuevos despliegues. Evaluar SeaweedFS o Garage como alternativas si no se usa MinIO Enterprise/AIStor.

> [!TIP]
> **Deepgram Flux**: Confirmar uso de Flux (no Nova-3) para el voice engine en tiempo real. Nova-3 para post-call analytics.

---

## FASE 0 — Preparación legal y alcance

### TASK 0.1 — Documento de alcance defensivo
- [x] **Modelo inferior puede ejecutar**
- Crear `docs/legal/alcance-defensivo.md`
- Contenido: solo llamadas entrantes, prohibiciones explícitas (salientes, publicación números, datos reales, clonación voz, acusaciones automáticas)
- Finalidad: investigación defensiva, clasificación, evidencia interna
- **Verificación**: No aparecen palabras prohibidas ("weaponización", "torturar", "organización criminal" como conclusión automática)

### TASK 0.2 — Mapa de datos tratados
- [x] **Modelo inferior puede ejecutar**
- Crear `docs/legal/mapa-datos.md`
- Tabla con columnas: Dato | Tipo (sensible/personal/técnico/derivado/anonimizable) | Retención | Acceso
- Datos: número llamante, audio, voz, transcripción, timestamp, carrier, país, coste, análisis IA, embeddings

### TASK 0.3 — Política de retención y borrado
- [x] **Modelo inferior puede ejecutar parcialmente**
- Crear `docs/legal/politica-retencion.md` (modelo inferior)
- Crear `services/worker/jobs/retention_cleanup.py` (modelo inferior con supervisión)
- Campo `retention_until` en BD, job diario, borrado MinIO, redacción pre-conservación
- **Nota**: El script Python debe ser revisado por modelo superior para edge cases

### TASK 0.4 — Paquete revisión legal
- [x] **Modelo inferior puede ejecutar**
- Crear `docs/legal/paquete-revision-legal.md` compilando docs anteriores
- Incluir referencia a numeración 400 (obligatoria desde oct 2026) y Circular 1/2023 AEPD

---

## FASE 1 — Infraestructura base

### TASK 1.1 — Crear estructura de repositorio
- [x] **Modelo inferior puede ejecutar**
- Crear árbol de directorios según plan (services/, packages/, infra/, docs/)
- README.md básico con descripción del proyecto

### TASK 1.2 — Docker Compose base
- [x] **Modelo inferior puede ejecutar con template**
- Servicios: postgres, redis, minio (o SeaweedFS), dashboard, voice-engine, analyzer, worker, asterisk
- **Mejora**: Añadir healthchecks a todos los servicios
- **Mejora**: Considerar SeaweedFS como alternativa a MinIO CE (ver nota WARNING arriba)
- Verificación: `docker compose up` levanta todo, PG acepta conexiones, Redis responde

### TASK 1.3 — Variables de entorno
- [x] **Modelo inferior puede ejecutar**
- Crear `.env.example` con todas las variables del plan
- Añadir validación de arranque que falle con error claro si falta variable crítica

---

## FASE 2 — Base de datos

### TASK 2.1 — Esquema PostgreSQL
- [x] **Modelo inferior puede ejecutar con supervisión**
- Tablas: calls, conversation_turns, call_analysis, personas, activity_clusters, blacklist_entries, audit_logs, system_events, api_usage
- Activar pgvector 0.8.x (usar HNSW para índices vectoriales)
- Índices por fecha, hash número, duración, tipo scam, campaña
- **Mejora**: Usar `halfvec` para embeddings si el espacio es limitante

### TASK 2.2 — Almacenamiento seguro de números
- [x] **Requiere supervisión de modelo superior**
- `caller_number_hash` (SHA-256 para búsquedas)
- `caller_number_encrypted` (AES-256 para consulta autorizada)
- Dashboard NO muestra número completo; solo rol legal/admin descifra

### TASK 2.3 — Auditoría de accesos
- [x] **Modelo inferior puede ejecutar**
- Tabla audit_logs: quién, qué llamada, descarga audio, exporta informe, descifra número
- Toda acción sensible genera registro

---

## FASE 3 — Telefonía Zadarma + Asterisk

### TASK 3.1 — Configurar Zadarma SIP
- [x] **Requiere configuración manual + modelo inferior para docs**
- Trunk SIP con IP autorizada, codec alaw/ulaw
- Modelo inferior: documentar proceso en `docs/deployment/zadarma-setup.md`
- Bloquear salientes por defecto

### TASK 3.2 — Configurar Asterisk
- [x] **Modelo inferior puede generar configs base**
- Generar `pjsip.conf`, `extensions.conf`, `ari.conf`
- **Mejora**: Usar Asterisk 20 o 22+ LTS
- **Mejora**: Configurar `external_media_address` y `external_signaling_address` para NAT

### TASK 3.3 — Audio bridge hacia Voice Engine
- [x] **Requiere modelo superior**
- **CAMBIO RECOMENDADO**: Usar AudioSocket en lugar de ExternalMedia
- AudioSocket: TCP directo, PCM 16-bit 8kHz, frames 20ms
- Más simple y menor latencia que ExternalMedia (RTP/UDP)
- Mantener ARI para control de llamada (answer, bridge, hangup, transfer)
- Registrar eventos inicio, silencio, error, fin

---

## FASE 4 — Voice Engine

### TASK 4.1 — Servicio voice-engine con Pipecat
- [x] **Requiere modelo superior para arquitectura**
- Modelo inferior: scaffold del servicio, Dockerfile, requirements.txt
- Modelo superior: pipeline Pipecat (STT→LLM→TTS), manejo interrupciones, VAD
- **Info Pipecat 2026**: Soporta Flows (conversación estructurada), multi-agent, 500-800ms round-trip
- Verificación: conversación de prueba 2 min, turnos guardados en BD

### TASK 4.2 — Persona inicial "Carmen"
- [x] **Modelo inferior puede ejecutar**
- Crear prompt en `packages/prompts/carmen.md`
- Carmen: jubilada 78 años, prudente, no da datos, busca papeles, preguntas lentas
- Reglas duras: no DNI/IBAN/dirección reales, no acepta enlaces, no instala software
- Datos ficticios si el flujo lo exige

### TASK 4.3 — Tácticas de retención
- [x] **Modelo inferior puede ejecutar**
- Implementar: buscar_documento, problema_auditivo_leve, consulta_familiar, duda_seguridad, peticion_identificacion, burocracia_ligera, cambio_tema_suave
- NO implementar: llorar, insultar, amenazar, devolver llamada, simular autoridad
- Cada táctica registrada en turno para métricas

### TASK 4.4 — Control duración máxima
- [x] **Modelo inferior puede ejecutar**
- MAX_CALL_DURATION_MINUTES configurable (MVP: 20min, avanzado: 45min)
- Corte automático por bucle, error o coste anómalo. Motivo registrado.

### TASK 4.5 — Interrupciones y silencios
- [x] **Requiere modelo superior**
- Pipecat VAD avanzado para barge-in
- Pausas 3-8s naturales, no 90s
- Escalar a táctica duda si caller sospecha

---

## FASE 5 — STT, LLM y TTS

### TASK 5.1 — STT primario
- [x] **Modelo inferior puede ejecutar integración**
- **Primario**: Deepgram Flux (NO Nova-3) — optimizado para voice agents, <300ms, turn detection integrado
- **Fallback**: AssemblyAI Universal-3 Pro Streaming ($0.45/hr, 6 idiomas)
- **Post-call**: Deepgram Nova-3 (50+ idiomas, mejor accuracy)
- Guardar confianza por turno. Si STT falla → colgar con seguridad.

### TASK 5.2 — LLM de conversación
- [x] **Modelo inferior puede ejecutar integración básica**
- **MVP**: Groq llama-3.3-70b-versatile (~315 tok/s)
- **Upgrade recomendado**: Evaluar Llama 4 Scout (10M contexto, 17B activos, MoE)
- **Fallback barato**: Groq llama-3.1-8b-instant
- **Post-call**: Modelo superior (Claude/GPT) para análisis profundo
- Respuesta <3s media. Prompt respeta restricciones de seguridad.

### TASK 5.3 — TTS
- [x] **Modelo inferior puede ejecutar integración**
- **Primario**: Cartesia Sonic 3.5 — 90ms first byte, 42 idiomas, español mejorado
- **Nota**: speed/volume controls deshabilitados en 3.5, usar Sonic 3 si se necesitan
- **Producción**: Pinear versión fecha (ej: `sonic-3-2026-05-04`), no usar `latest`
- **Fallback**: ElevenLabs Flash v2.5 (~75ms, 0.5 credits/char)
- No usar voz clonada de persona real

### TASK 5.4 — Medición de coste
- [x] **Modelo inferior puede ejecutar**
- Tabla api_usage: proveedor, modelo, segundos audio, tokens in/out, coste estimado, call_id
- Dashboard: coste diario/semanal/mensual. Alerta si supera presupuesto.

---

## FASE 6 — Grabación y almacenamiento

### TASK 6.1 — Audio en MinIO/SeaweedFS
- [x] **Modelo inferior puede ejecutar**
- WAV/FLAC por llamada. Nombre sin número telefónico.
- Cifrado en reposo. Retención automática. Solo rol autorizado descarga.

### TASK 6.2 — Transcripción
- [x] **Modelo inferior puede ejecutar**
- Turnos en BD, versión completa JSON, datos sensibles marcados
- Versión redactada por defecto en dashboard

---

## FASE 7 — Analyzer post-llamada

### TASK 7.1 — Clasificación básica
- [x] **Modelo inferior puede ejecutar**
- 16 categorías (energia, telecomunicaciones, banca, inversion, cripto, etc.)
- scam_type + confidence por llamada. Si <0.65 → revisión manual.

### TASK 7.2 — Detección de técnicas
- [x] **Modelo inferior puede ejecutar con prompts**
- 14 técnicas (autoridad, urgencia, miedo, etc.)
- JSONB con evidencia textual. No inventar sin fragmento.

### TASK 7.3 — Redacción datos sensibles
- [x] **Modelo inferior puede ejecutar**
- Detectar: DNI/NIE, IBAN, tarjetas, direcciones, nombres, emails, teléfonos
- Sustituir por etiquetas: [DNI_REDACTADO], [IBAN_REDACTADO], etc.

### TASK 7.4 — Fingerprint de guion
- [x] **Requiere modelo superior para diseño de embeddings**
- Extraer: apertura, entidad suplantada, motivo, amenaza/oferta, datos solicitados, cierre
- Fingerprint sin datos personales. Llamadas similares → fingerprints comparables.

---

## FASE 8 — Dashboard MVP

### TASK 8.1 — Página "En vivo"
- [x] **Modelo inferior puede ejecutar con Streamlit**
- Llamadas activas, duración, persona, estado STT/LLM/TTS, coste, botón colgar, transcripción live
- **Streamlit 2026**: Soporta AudioColumn, chat_input mejorado, top navigation

### TASK 8.2 — Página "Histórico"
- [x] **Modelo inferior puede ejecutar**
- Filtros: fecha, tipo, duración, persona, confianza, revisado
- Rendimiento: <2s con 10K registros (usar @st.cache_data)

### TASK 8.3 — Detalle de llamada
- [x] **Modelo inferior puede ejecutar**
- Tabs: Resumen, Transcripción, Audio, Análisis, Técnicas, Coste, Auditoría
- Audio solo roles autorizados. Transcripción redactada por defecto.

### TASK 8.4 — Página "Compliance"
- [x] **Modelo inferior puede ejecutar**
- Audios por vencer, datos sensibles, exportaciones, accesos, errores borrado

---

## FASE 9 — Telegram Bot

### TASK 9.1 — Alertas críticas
- [x] **Modelo inferior puede ejecutar**
- Alertar: llamada larga, fallos STT/TTS/LLM, coste alto, campaña nueva, solicitud datos bancarios
- NO enviar: ranking tortura, número real, org criminal, mensajes burlescos

---

## FASE 10 — Clustering e inteligencia

### TASK 10.1 — Embeddings
- [x] **Modelo inferior puede ejecutar integración**
- Embedding de resumen, fingerprint, apertura, entidad suplantada
- pgvector HNSW para búsqueda de similitud

### TASK 10.2 — Campañas probables
- [x] **Requiere modelo superior**
- Criterios: similitud fingerprint >0.75, misma entidad, mismo tipo, patrón horario, técnicas similares
- activity_cluster con nivel confianza. Sin lenguaje acusatorio.

### TASK 10.3 — Reglas España 2026
- [x] **Modelo inferior puede ejecutar**
- Regla numeración 400 (obligatoria oct 2026, Ley SAC dic 2025)
- Campo numbering_anomaly_detected (NO prueba única de fraude)
- Dashboard diferencia: anomalía normativa / posible scam / fraude confirmado manual

---

## FASE 11 — Seguridad

### TASK 11.1 — Roles y permisos
- [x] **Modelo inferior puede ejecutar**
- Roles: admin, analyst, viewer, legal, operator
- Matriz permisos según plan original

### TASK 11.2 — Gestión de secretos
- [x] **Modelo inferior puede ejecutar**
- .env local, Docker secrets en producción
- Test automático falla si detecta claves en repo

### TASK 11.3 — Fail-safe
- [x] **Requiere modelo superior para edge cases**
- STT falla→colgar. TTS falla→mensaje neutro+colgar. LLM lento→fallback. Coste límite→colgar. BD caída→no grabar.

---

## FASE 12 — Testing

### TASK 12.1 — Tests unitarios
- [x] **Modelo inferior puede ejecutar**
- Cubrir: prompts, tácticas, clasificación, redacción, costes, permisos, retención
- Cobertura mínima: 70%

### TASK 12.2 — Tests llamada simulada
- [x] **Modelo inferior puede ejecutar con escenarios definidos**
- 10 escenarios: corta, larga, agresivo, pide IBAN/DNI, enlace, silencio, fallos STT/TTS/LLM
- Todos terminan con estado controlado

### TASK 12.3 — Prueba piloto
- [x] **Requiere ejecución manual supervisada**
- 10 llamadas, 3 guiones, 2 voces, 1 persona
- 0 caídas, 100% registradas, 100% transcritas, coste medido
