SCAMEATER — Task Maestro de Fabricación
Decisión técnica principal

La arquitectura recomendada es:

Zadarma
  ↓
Asterisk
  ↓
ARI / ExternalMedia
  ↓
Voice Engine Python + Pipecat
  ↓
STT + LLM + TTS
  ↓
Post-Call Analyzer
  ↓
PostgreSQL + pgvector + MinIO + Redis
  ↓
Dashboard + Telegram + Informes

Motivo: Zadarma ya tiene documentación oficial para conectar Asterisk mediante SIP trunk y enrutado de llamadas hacia servidor externo; Asterisk permite sacar audio hacia servicios externos usando ARI ExternalMedia; Pipecat está pensado precisamente para construir agentes de voz y multimodales en tiempo real.

1. Alternativas evaluadas
1.1 Telefonía
Opción	Decisión	Motivo
Zadarma + Asterisk	Recomendada	Máximo control, compatible con tu plan, permite grabación, routing, logs y aislamiento.
OpenAI Realtime SIP directo	Alternativa futura	Más rápido para prototipo, pero menos control sobre PBX, grabación, reglas internas y costes.
Twilio / Telnyx	No prioritaria	Más dependencia externa y menos alineada con la limitación actual de Zadarma + Asterisk.

OpenAI ya permite conectar llamadas entrantes SIP directamente con Realtime API, pero para este caso lo dejaría como opción B, no como base inicial.

1.2 Motor de voz
Opción	Decisión	Motivo
Pipecat	Recomendada	Framework abierto para agentes de voz en tiempo real. Reduce trabajo de orquestación.
Python puro	No recomendado	Mucho más trabajo: turnos, audio, interrupciones, transporte, latencia.
OpenAI Realtime todo-en-uno	Alternativa rápida	Menos piezas, pero más dependencia y menos capacidad de auditoría propia.

Pipecat está diseñado para orquestar servicios de IA, transporte, audio y conversación en aplicaciones de baja latencia.

1.3 STT — voz a texto
Opción	Decisión	Uso recomendado
Deepgram Nova-3 / Flux	Recomendada	Baja latencia, buen enfoque para voz conversacional.
AssemblyAI Universal-Streaming	Alternativa seria	Interesante si Deepgram falla en acentos o coste.
Google Speech-to-Text	Alternativa enterprise	Robusto, pero más pesado de integrar.
Whisper local	Fase avanzada	Barato a escala, pero exige GPU/CPU y puede añadir latencia.

Deepgram posiciona Nova-3 y Flux para speech-to-text conversacional; AssemblyAI Universal-Streaming también está orientado a voice agents con baja latencia; Google Speech-to-Text soporta streaming mediante gRPC.

1.4 LLM
Opción	Decisión	Uso
Groq llama-3.3-70b-versatile	Recomendada para MVP	Rápido, buen coste/rendimiento, válido para conversación.
OpenAI Realtime	Alternativa premium	Menos integración manual, pero más coste y dependencia.
Modelo local vía vLLM	Fase avanzada	Para reducir coste si hay volumen.
Anthropic / OpenAI post-call	Recomendado solo para análisis	Mejor para análisis profundo, no necesariamente para cada turno.

Groq documenta llama-3.3-70b-versatile como modelo de producción y publica velocidad/precio por millón de tokens; OpenAI publica precios de Realtime por modalidad de audio/texto.

1.5 TTS — texto a voz
Opción	Decisión	Uso
Cartesia Sonic 3.5	Recomendada	Baja latencia, voz natural, buena para conversación.
ElevenLabs Flash/Turbo	Alternativa	Buenas voces y baja latencia, revisar coste por volumen.
Piper / Coqui / local	Fase avanzada	Barato, pero menor naturalidad y más trabajo.

Cartesia documenta Sonic 3.5 como modelo de TTS en streaming de baja latencia; ElevenLabs publica opciones Flash/Turbo con baja latencia y precio por caracteres.

1.6 Base de datos e inteligencia
Opción	Decisión
PostgreSQL + pgvector	Recomendada
Qdrant separado	Fase avanzada
Elasticsearch/OpenSearch	Solo si el histórico crece mucho
SQLite/Turso	No recomendado para el núcleo de llamadas

pgvector permite guardar embeddings dentro de PostgreSQL y hacer búsqueda vectorial con distancias como cosine, L2 o inner product.

2. Restricciones obligatorias

Estas restricciones no se negocian:

Solo llamadas entrantes.
No devolver llamadas.
No publicar números.
No almacenar datos bancarios reales.
No usar voces reales clonadas.
No afirmar “organización criminal” sin validación externa.
No usar el sistema para hostigar.
Redacción automática de datos sensibles.
Retención limitada de audio.
Logs de acceso y trazabilidad.

La voz puede ser dato personal cuando permite identificar directa o indirectamente a una persona, y la AEPD ha tratado específicamente la transcripción de voz con IA desde la óptica de protección de datos.

Además, en España el marco de llamadas comerciales no deseadas está regulado por la Circular 1/2023 de la AEPD, y desde octubre de 2026 las llamadas comerciales deberán usar numeración 400 según resolución publicada y notas oficiales. Esto debe entrar en las reglas de clasificación, pero nunca como prueba automática de fraude.

3. Task maestro por fases
FASE 0 — Preparación legal, técnica y de alcance

Objetivo: no escribir código serio hasta tener límites claros.

TASK 0.1 — Definir alcance defensivo

Acciones:

Crear documento docs/legal/alcance-defensivo.md.
Definir que el sistema solo recibe llamadas.
Prohibir llamadas salientes.
Prohibir publicación de números.
Prohibir uso de datos reales.
Definir finalidad: investigación defensiva, clasificación y evidencia interna.

Resultado esperado:

docs/legal/alcance-defensivo.md

Criterio de aceptación:

El documento deja claro qué puede y qué no puede hacer SCAMEATER.
No aparece la palabra “weaponización”.
No aparece “torturar spammers”.
No aparece “organización criminal” como conclusión automática.
TASK 0.2 — Mapa de datos tratados

Acciones:

Listar todos los datos que se tratarán:
número llamante,
audio,
voz,
transcripción,
timestamp,
carrier,
país,
coste,
análisis IA,
embeddings.
Marcar cada dato como:
sensible,
personal,
técnico,
derivado,
anonimizable.
Definir retención:
audio: 30/60/90 días según decisión legal,
transcripción: más tiempo si se anonimiza,
número: hash por defecto, cifrado si hace falta consultar.

Resultado esperado:

docs/legal/mapa-datos.md

Criterio de aceptación:

Se puede explicar qué dato se guarda, por qué, cuánto tiempo y quién lo puede ver.
TASK 0.3 — Política de retención y borrado

Acciones:

Crear política de borrado automático.
Definir retention_until en base de datos.
Crear job diario de limpieza.
Borrar audio vencido de MinIO.
Redactar transcripciones antes de conservación larga.

Resultado esperado:

docs/legal/politica-retencion.md
services/worker/jobs/retention_cleanup.py

Criterio de aceptación:

El sistema puede borrar automáticamente audios antiguos.
El borrado queda registrado en auditoría.
TASK 0.4 — Decisión legal antes de producción

Acciones:

Preparar paquete para abogado/DPO:
alcance defensivo,
mapa de datos,
política de retención,
arquitectura,
seguridad,
flujo de grabación,
medidas de minimización.

Resultado esperado:

docs/legal/paquete-revision-legal.md

Criterio de aceptación:

Nadie puede desplegar producción sin marcar esta tarea como validada.
4. FASE 1 — Infraestructura base
TASK 1.1 — Crear repositorio

Estructura final:

scameater/
├── docker-compose.yml
├── .env.example
├── README.md
├── services/
│   ├── gateway-asterisk/
│   ├── voice-engine/
│   ├── analyzer/
│   ├── dashboard/
│   ├── telegram-bot/
│   └── worker/
├── packages/
│   ├── shared/
│   ├── prompts/
│   └── schemas/
├── infra/
│   ├── postgres/
│   ├── redis/
│   ├── minio/
│   ├── nginx/
│   └── monitoring/
└── docs/
    ├── legal/
    ├── architecture/
    ├── deployment/
    └── operations/

Criterio de aceptación:

docker compose up levanta PostgreSQL, Redis, MinIO y dashboard vacío.
.env real no entra al repositorio.
.env.example sí entra.
TASK 1.2 — Docker Compose base

Servicios obligatorios:

postgres
redis
minio
dashboard
voice-engine
analyzer
worker
asterisk

Criterio de aceptación:

Todos los servicios arrancan.
PostgreSQL acepta conexiones.
MinIO crea bucket call-audio.
Redis responde.
Dashboard muestra healthcheck.
TASK 1.3 — Variables de entorno

Crear:

.env.example

Variables mínimas:

APP_ENV=local
APP_SECRET_KEY=

DATABASE_URL=
REDIS_URL=

MINIO_ENDPOINT=
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_BUCKET_AUDIO=

ZADARMA_SIP_SERVER=
ZADARMA_SIP_USER=
ZADARMA_SIP_PASS=

ASTERISK_ARI_URL=
ASTERISK_ARI_USER=
ASTERISK_ARI_PASS=

STT_PROVIDER=deepgram
DEEPGRAM_API_KEY=

LLM_PROVIDER=groq
GROQ_API_KEY=

TTS_PROVIDER=cartesia
CARTESIA_API_KEY=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

AUDIO_RETENTION_DAYS=60
MAX_CALL_DURATION_MINUTES=45
ENABLE_RECORDING=true
ENABLE_TRANSCRIPTION=true

Criterio de aceptación:

No hay claves reales en el repo.
El sistema falla con error claro si falta una variable crítica.
5. FASE 2 — Base de datos
TASK 2.1 — Crear esquema PostgreSQL

Tablas mínimas:

calls
conversation_turns
call_analysis
personas
activity_clusters
blacklist_entries
audit_logs
system_events
api_usage

Criterio de aceptación:

Migraciones ejecutables.
Índices por fecha, hash de número, duración, tipo de scam y campaña.
pgvector activado para embeddings.
TASK 2.2 — Guardar número de forma segura

Acciones:

Guardar número en claro solo si es necesario.
Crear:
caller_number_hash,
caller_number_encrypted.
Usar hash para búsquedas.
Usar cifrado para consulta autorizada.

Criterio de aceptación:

El dashboard normal no muestra número completo.
Solo rol legal/admin puede ver dato descifrado.
TASK 2.3 — Auditoría de accesos

Acciones:

Registrar:
quién accede,
qué llamada consulta,
si descarga audio,
si exporta informe,
si descifra número.

Criterio de aceptación:

Toda acción sensible genera línea en audit_logs.
6. FASE 3 — Telefonía Zadarma + Asterisk
TASK 3.1 — Configurar Zadarma SIP

Acciones:

Crear trunk SIP.
Asociar IP fija del VPS.
Configurar número entrante hacia Asterisk.
Verificar codec alaw/ulaw.
Bloquear llamadas salientes salvo necesidad técnica expresa.

Zadarma documenta conexión SIP trunk con IP autorizada y configuración Asterisk/PJSIP.

Criterio de aceptación:

Llamada entrante llega a Asterisk.
Se registra caller ID.
No se permite salida por defecto.
TASK 3.2 — Configurar Asterisk

Acciones:

Crear pjsip.conf.
Crear extensions.conf.
Crear ari.conf.
Activar ARI.
Crear contexto de llamadas entrantes.
Crear bridge hacia aplicación Python.

Criterio de aceptación:

Asterisk recibe llamada.
ARI detecta evento.
Se puede colgar llamada desde backend.
TASK 3.3 — ExternalMedia hacia Voice Engine

Acciones:

Usar ARI /channels/externalMedia.
Enviar audio RTP hacia voice-engine.
Recibir audio de vuelta.
Registrar eventos de inicio, silencio, error y fin.

Asterisk documenta que ExternalMedia se crea mediante petición ARI a /channels/externalMedia.

Criterio de aceptación:

El voice engine recibe audio real.
El voice engine puede devolver audio.
La llamada no se corta al activar puente.
7. FASE 4 — Voice Engine
TASK 4.1 — Crear servicio voice-engine

Responsabilidad:

recibir audio,
enviar a STT,
pasar texto al LLM,
generar respuesta,
enviar TTS,
guardar turnos,
aplicar límites de seguridad.

Criterio de aceptación:

Una llamada de prueba mantiene conversación durante 2 minutos.
Se guardan turnos en conversation_turns.
TASK 4.2 — Implementar persona inicial

Persona MVP:

Carmen, jubilada prudente.
78 años.
Vive sola.
No da datos por teléfono.
Necesita tiempo para buscar papeles.
Hace preguntas lentas y naturales.
Nunca entrega datos reales.

Reglas duras del prompt:

- No dar DNI real.
- No dar cuenta bancaria.
- No dar dirección real.
- No aceptar enlaces.
- No instalar software.
- No confirmar datos reales.
- Usar datos ficticios si el flujo lo exige.
- Mantener tono humano, lento y prudente.

Criterio de aceptación:

El bot nunca entrega datos sensibles reales.
El bot puede sostener una conversación básica.
El bot no revela que es IA salvo orden interna de emergencia.
TASK 4.3 — Tácticas de retención

Implementar tácticas moderadas:

buscar_documento
problema_auditivo_leve
consulta_familiar
duda_seguridad
peticion_identificacion_empresa
burocracia_ligera
cambio_tema_suave

No implementar:

llorar
insultar
amenazar
devolver llamada
simular autoridad
usar datos reales
provocar activamente

Criterio de aceptación:

Cada táctica queda registrada en el turno.
El sistema puede medir qué táctica alarga más la llamada.
TASK 4.4 — Control de duración máxima

Acciones:

Configurar MAX_CALL_DURATION_MINUTES.
MVP recomendado: 20 minutos.
Fase avanzada: 45 minutos.
Cortar automáticamente si hay bucle, error o coste anómalo.

Criterio de aceptación:

Ninguna llamada supera el límite configurado.
El motivo de corte queda registrado.
TASK 4.5 — Interrupciones y silencios

Acciones:

Detectar interrupciones.
No pisar al caller.
No dejar silencios irreales.
Usar pausas de 3-8 segundos, no 90 segundos repetidos.
Escalar a táctica de duda si el caller sospecha.

Criterio de aceptación:

Conversación natural en prueba manual.
Latencia media documentada.
8. FASE 5 — STT, LLM y TTS
TASK 5.1 — Integrar STT primario

Proveedor recomendado:

Deepgram Nova-3 / Flux

Fallback:

AssemblyAI Universal-Streaming

Criterio de aceptación:

Transcripción parcial en tiempo real.
Transcripción final por turno.
Confianza guardada.
Si STT falla, la llamada se cierra con seguridad.
TASK 5.2 — Integrar LLM de conversación

Proveedor recomendado MVP:

Groq llama-3.3-70b-versatile

Fallback barato:

Groq llama-3.1-8b-instant

Uso correcto:

modelo rápido para conversación,
modelo más fuerte para análisis post-llamada,
no gastar modelo caro en cada turno si no hace falta.

Criterio de aceptación:

Respuesta en menos de 3 segundos de media.
El modelo respeta restricciones de seguridad.
El prompt no genera datos reales.
TASK 5.3 — Integrar TTS

Proveedor recomendado:

Cartesia Sonic 3.5

Fallback:

ElevenLabs Flash/Turbo

Criterio de aceptación:

Voz española natural.
Latencia aceptable.
No usa voz clonada de persona real.
Se puede cambiar voz desde configuración.
TASK 5.4 — Medición de coste

Acciones:

Crear tabla api_usage.
Guardar:
proveedor,
modelo,
segundos de audio,
tokens input,
tokens output,
coste estimado,
llamada asociada.

Criterio de aceptación:

Cada llamada muestra coste aproximado.
Dashboard tiene coste diario/semanal/mensual.
Alerta si se supera presupuesto diario.
9. FASE 6 — Grabación y almacenamiento
TASK 6.1 — Guardar audio en MinIO

Acciones:

Guardar WAV/FLAC por llamada.
Nombre de objeto sin número telefónico.
Metadata mínima.
Cifrado en reposo.
Retención automática.

Criterio de aceptación:

Audio descargable solo por rol autorizado.
Audio eliminado al vencer retención.
TASK 6.2 — Guardar transcripción

Acciones:

Guardar turnos en base de datos.
Guardar versión completa en JSON.
Marcar datos sensibles.
Crear versión redactada.

Criterio de aceptación:

Dashboard muestra transcripción redactada por defecto.
Exportación completa requiere permiso superior.
10. FASE 7 — Analyzer post-llamada
TASK 7.1 — Clasificación básica

Clasificar:

energia
telecomunicaciones
banca
inversion
cripto
soporte_tecnico
administracion_publica
hacienda
seguridad_social
paqueteria
empleo
seguros
encuestas
donaciones
loterias
otros

Criterio de aceptación:

Cada llamada completada tiene scam_type.
Cada clasificación tiene confidence.
Si confianza < 0.65, queda como “revisión manual”.
TASK 7.2 — Detección de técnicas

Detectar:

autoridad
urgencia
miedo
perdida_economica
falsa_verificacion
familiaridad
transferencia_supervisor
descuento_exclusivo
presion_contractual
solicitud_datos_personales
solicitud_datos_bancarios
instalacion_software
envio_enlace
redireccion_whatsapp

Criterio de aceptación:

Técnicas guardadas en JSONB.
Cada técnica tiene evidencia textual.
El sistema no inventa técnicas sin fragmento asociado.
TASK 7.3 — Redacción de datos sensibles

Acciones:

Detectar:
DNI/NIE,
IBAN,
tarjetas,
direcciones,
nombres completos,
emails,
teléfonos.
Crear transcripción redactada.

Criterio de aceptación:

Datos sensibles se sustituyen por etiquetas:
[DNI_REDACTADO]
[IBAN_REDACTADO]
[TELEFONO_REDACTADO]
TASK 7.4 — Fingerprint de guion

Acciones:

Extraer:
apertura,
entidad suplantada,
motivo,
amenaza/oferta,
datos solicitados,
cierre.
Crear script_fingerprint.

Criterio de aceptación:

Llamadas similares generan fingerprints comparables.
El fingerprint no contiene datos personales en claro.
11. FASE 8 — Dashboard MVP
TASK 8.1 — Página “En vivo”

Debe mostrar:

llamadas activas,
duración,
persona usada,
estado STT/LLM/TTS,
coste estimado,
botón colgar,
transcripción en vivo.

Criterio de aceptación:

Se puede cortar una llamada desde dashboard.
Se ve transcripción parcial.
TASK 8.2 — Página “Histórico”

Debe mostrar:

fecha,
duración,
tipo de llamada,
confianza,
persona,
coste,
estado de análisis.

Filtros:

fecha,
tipo,
duración,
persona,
confianza,
revisado/no revisado.

Criterio de aceptación:

Buscar una llamada tarda menos de 2 segundos con 10.000 registros.
TASK 8.3 — Detalle de llamada

Tabs:

Resumen
Transcripción
Audio
Análisis
Técnicas
Coste
Auditoría

Criterio de aceptación:

Audio solo visible para roles autorizados.
Transcripción redactada por defecto.
Informe exportable.
TASK 8.4 — Página “Compliance”

Debe mostrar:

audios próximos a vencer,
datos sensibles detectados,
exportaciones realizadas,
accesos a llamadas,
llamadas pendientes de redacción,
errores de borrado.

Criterio de aceptación:

Se puede auditar el sistema sin mirar la base de datos directamente.
12. FASE 9 — Telegram Bot
TASK 9.1 — Alertas críticas

Enviar alertas por:

llamada superior a X minutos
fallo STT
fallo TTS
fallo LLM
coste diario alto
nueva campaña probable
solicitud de datos bancarios
fallo de guardado audio
fallo de análisis

No enviar:

ranking de tortura
número real detectado
organización criminal detectada
mensaje burlesco

Criterio de aceptación:

Telegram no filtra datos personales.
Las alertas son útiles y sobrias.
13. FASE 10 — Clustering e inteligencia
TASK 10.1 — Embeddings

Acciones:

Generar embedding de:
resumen,
fingerprint,
apertura del guion,
entidad suplantada.
Guardar en pgvector.

Criterio de aceptación:

Se pueden buscar llamadas similares.
TASK 10.2 — Campañas probables

Criterios:

similitud fingerprint > 0.75
misma entidad suplantada
mismo tipo de scam
patrón horario similar
números relacionados por hash/prefijo
técnicas similares

Criterio de aceptación:

El sistema crea activity_cluster.
El cluster tiene nivel de confianza.
No usa lenguaje acusatorio.
TASK 10.3 — Reglas España 2026

Acciones:

Añadir regla informativa sobre numeración 400.
Añadir regla sobre móviles usados para llamadas comerciales.
Añadir campo:
numbering_anomaly_detected.
No usarlo como prueba única de fraude.

Criterio de aceptación:

El dashboard diferencia:
“anomalía normativa”,
“posible scam”,
“fraude confirmado manualmente”.
14. FASE 11 — Seguridad
TASK 11.1 — Roles

Roles mínimos:

admin
analyst
viewer
legal
operator

Permisos:

Acción	Admin	Legal	Analyst	Operator	Viewer
Ver resumen	Sí	Sí	Sí	Sí	Sí
Ver número completo	Sí	Sí	No	No	No
Descargar audio	Sí	Sí	Opcional	No	No
Exportar informe	Sí	Sí	Sí	No	No
Borrar llamada	Sí	Sí	No	No	No
Colgar llamada	Sí	No	No	Sí	No

Criterio de aceptación:

Ningún usuario sin rol ve datos sensibles.
TASK 11.2 — Gestión de secretos

Acciones:

Usar .env local.
En producción, usar Docker secrets o gestor externo.
Rotación mensual de API keys.
Nunca imprimir claves en logs.

Criterio de aceptación:

Test automático falla si detecta claves en repo.
TASK 11.3 — Fail-safe

Acciones:

Si STT falla: colgar.
Si TTS falla: reproducir mensaje neutro y colgar.
Si LLM tarda demasiado: respuesta fallback.
Si coste supera límite: colgar.
Si base de datos cae: no continuar grabando.

Criterio de aceptación:

Ningún fallo deja llamada abierta sin control.
15. FASE 12 — Testing
TASK 12.1 — Tests unitarios

Cubrir:

prompts,
tácticas,
clasificación,
redacción,
cálculo de coste,
permisos,
retención.

Criterio de aceptación:

Cobertura mínima: 70% en MVP.
TASK 12.2 — Tests de llamada simulada

Escenarios:

llamada corta
llamada larga
caller agresivo
caller pide IBAN
caller pide DNI
caller envía enlace
silencio largo
STT falla
TTS falla
LLM falla

Criterio de aceptación:

Todos los escenarios terminan con estado controlado.
TASK 12.3 — Prueba piloto

Objetivo:

10 llamadas controladas.
3 tipos de guion.
2 voces.
1 persona.

Criterio de aceptación:

0 caídas graves.
100% llamadas registradas.
100% audios asociados.
100% transcripciones generadas.
coste medido por llamada.
16. Orden real de fabricación

No haría todo a la vez. Este es el orden correcto:

1. Legal y límites
2. Docker base
3. PostgreSQL + MinIO + Redis
4. Zadarma + Asterisk
5. ARI detectando llamadas
6. ExternalMedia enviando audio
7. Voice Engine mínimo
8. STT
9. TTS
10. LLM
11. Una persona
12. Guardado de llamada
13. Dashboard en vivo
14. Histórico
15. Analyzer básico
16. Redacción de datos sensibles
17. Telegram
18. Costes
19. Clustering
20. Compliance avanzado
17. MVP cerrado

El MVP correcto no es el sistema completo. Es esto:

SCAMEATER MVP 1.0
- Recibe llamadas desde Zadarma
- Asterisk las entrega al voice-engine
- El bot responde con una persona ficticia
- Se graba audio
- Se transcribe
- Se guarda en PostgreSQL
- Se guarda audio en MinIO
- Se analiza tipo de llamada
- Se redactan datos sensibles
- Se ve en dashboard
- Se puede colgar manualmente
- Se mide coste
- Se aplica retención

Todo lo demás va después.

18. No construir todavía

Estas partes deben esperar:

API pública
reconocimiento individual de voces
organizaciones criminales
mapas complejos
modelo propio
comunidad externa
A/B testing avanzado
predicción de comportamiento
llamadas de más de una hora

Meter eso al principio solo aumenta coste, riesgo legal y probabilidad de bloqueo técnico.

19. Resultado esperado por entregas
Entrega 1 — Semana 1
Repositorio listo
Docker base
PostgreSQL
Redis
MinIO
Dashboard vacío
Documentos legales base
Entrega 2 — Semana 2
Zadarma conectado
Asterisk funcionando
ARI detectando llamadas
Grabación básica
Registro de llamadas
Entrega 3 — Semana 3
Voice Engine básico
STT funcionando
TTS funcionando
LLM respondiendo
Persona Carmen activa
Entrega 4 — Semana 4
Dashboard En Vivo
Histórico
Detalle de llamada
Coste por llamada
Colgar desde dashboard
Entrega 5 — Semana 5
Analyzer post-llamada
Clasificación
Técnicas detectadas
Redacción de datos sensibles
Informe básico
Entrega 6 — Semana 6
Telegram
Retención automática
Auditoría
Primer clustering simple
Piloto controlado
20. Definition of Done global

SCAMEATER estará fabricado correctamente cuando cumpla esto:

- Recibe llamadas reales.
- Conversa sin bloquearse.
- No entrega datos reales.
- Guarda audio y transcripción.
- Redacta datos sensibles.
- Clasifica la llamada.
- Calcula coste.
- Permite revisión humana.
- Permite borrar datos.
- Tiene auditoría.
- Tiene límites de duración.
- Tiene roles.
- Tiene documentación.
- Tiene despliegue reproducible.
21. Decisión final recomendada

La mejor combinación para fabricar el sistema ahora mismo es:

Telefonía: Zadarma + Asterisk
Audio bridge: Asterisk ARI ExternalMedia
Voice Engine: Python + Pipecat
STT: Deepgram Nova-3 / Flux
LLM realtime: Groq llama-3.3-70b-versatile
TTS: Cartesia Sonic 3.5
DB: PostgreSQL + pgvector
Storage: MinIO
Cache: Redis
Dashboard MVP: Streamlit
Dashboard futuro: Next.js + FastAPI
Alertas: Telegram
Compliance: desde fase 0