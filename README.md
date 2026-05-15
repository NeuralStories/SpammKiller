# SCAMEATER – Sistema Honeypot Conversacional Anti‑Spam VoIP

**Objetivo**

Crear un honeypot de llamadas telefónicas orientado al mercado español que:
- Reciba llamadas spam mediante un número SIP de Zadarma.
- Mantenga al spammer en la línea durante 20‑120 min.
- Grabe, transcriba y analice cada conversación con IA (STT, LLM, TTS).
- Detecte patrones, campañas y organizaciones criminales.
- Notifique en tiempo real por Telegram y ofrezca un panel de control web completo.

**Stack tecnológico (según el plan maestro)**

- **Telefonía**: Asterisk 20 LTS + Zadarma (SIP trunk).
- **Orquestación**: Docker Compose (services: PostgreSQL + pgvector, Redis, MinIO/SeaweedFS, Streamlit dashboard, FastAPI, engine Python, Asterisk).
- **Motor de voz**: Pipecat Python 3.11 con Deepgram Flux (STT), Groq Llama‑3.1‑70B (LLM), Cartesia Sonic 3.5 (TTS).
- **Almacenamiento**: MinIO (or SeaweedFS) para audios; PostgreSQL 15 para metadatos.
- **Observabilidad**: Langfuse (LLM tracing), Prometheus + Grafana, structlog.
- **Notificaciones**: Bot de Telegram.

**Componentes principales**

| Componente | Función |
|------------|---------|
| `asterisk/` | Configuración SIP, dialplan, ARI y AudioSocket para bridge directo a engine. |
| `engine/` | Motor Pipecat: STT → LLM → TTS, gestión de tácticas de retención, guardado de audio y transcripciones. |
| `dashboard/` | UI Streamlit con vistas en vivo, histórico, análisis, cumplimiento y métricas de coste. |
| `api/` | FastAPI interno para operaciones CRUD y exportación de datos. |
| `scripts/` | Scripts de despliegue, backup, pruebas de llamada, inicialización de BD. |
| `docs/` | Documentación legal, arquitectura, despliegue y operación. |

**Guía rápida de puesta en marcha (Docker)**

```bash
# 1. Copiar variables de entorno y ajustarlas
cp .env.example .env
# editar .env con claves API (Deepgram, Groq, Cartesia, Zadarma, Telegram, etc.)

# 2. Construir y lanzar los contenedores
docker compose up -d --build

# 3. Inicializar la base de datos
docker exec scameater-engine python scripts/init_db.py

# 4. Acceder al panel
#   Dashboard: http://localhost:8501
#   API: http://localhost:8000
#   Asterisk (hosted on the VM) escuchará en el puerto SIP 5060.
```

**Consideraciones legales y de compliance**

- Sólo llamadas **entrantes**; las salientes están bloqueadas por defecto.
- No se revelan datos reales (DNI, IBAN, etc.) – se sustituyen por marcadores `[REDACTADO]`.
- Retención de datos configurable (por defecto 90 días). Los scripts de limpieza están en `services/worker/jobs/retention_cleanup.py`.
- Cumplimiento de la normativa española 2026 (número 400, Ley SAC, RGPD).

**Roadmap (Fases del plan maestro)**

1️⃣ Infraestructura base (Docker, directorios, variables).
2️⃣ Esquema PostgreSQL y auditoría.
3️⃣ Configuración telefónica (Zadarma, Asterisk, AudioSocket).
4️⃣ Motor de voz (Pipecat, Deepgram Flux, Cartesia, LLM).
5️⃣ Analizador post‑llamada y clustering.
6️⃣ Dashboard y bot de Telegram.
7️⃣ Tests unitarios y simulación de llamadas.

---

*Este README es la base; se ampliará con instrucción de despliegue, ejemplos de llamadas de prueba y guía de contribución.*