

Max
SCAMEATER - Plan Maestro Completo
Voy a darte el documento .md más completo y detallado posible. Está diseñado para que una IA (o un desarrollador) pueda ejecutarlo de principio a fin sin ambigüedades.

Markdown

# 🕷️ SCAMEATER - Plan Maestro de Implementación Completo
> Sistema Honeypot Conversacional Anti-Spam VoIP para España
> Versión: 1.0 | Estado: Production-Ready Blueprint
> Stack: Asterisk + Zadarma + Pipecat + Groq + Deepgram + 
>        Cartesia + PostgreSQL + MinIO + Streamlit + Docker

---

## ÍNDICE

1. [Visión General del Sistema](#1-visión-general-del-sistema)
2. [Arquitectura Completa](#2-arquitectura-completa)
3. [Prerequisitos e Infraestructura](#3-prerequisitos-e-infraestructura)
4. [Estructura de Directorios](#4-estructura-de-directorios)
5. [Base de Datos - Esquema Completo](#5-base-de-datos---esquema-completo)
6. [Docker Compose - Infraestructura Completa](#6-docker-compose---infraestructura-completa)
7. [Configuración de Asterisk + Zadarma](#7-configuración-de-asterisk--zadarma)
8. [Motor de Voz - Engine](#8-motor-de-voz---engine)
9. [Sistema de Personas y Prompts](#9-sistema-de-personas-y-prompts)
10. [Analizador Post-Llamada](#10-analizador-post-llamada)
11. [Sistema de Geolocalización](#11-sistema-de-geolocalización)
12. [Motor de Clustering e Inteligencia](#12-motor-de-clustering-e-inteligencia)
13. [Bot de Telegram](#13-bot-de-telegram)
14. [Panel de Control - Dashboard](#14-panel-de-control---dashboard)
15. [Sistema de Almacenamiento de Audio](#15-sistema-de-almacenamiento-de-audio)
16. [API REST Interna](#16-api-rest-interna)
17. [Variables de Entorno](#17-variables-de-entorno)
18. [Scripts de Despliegue](#18-scripts-de-despliegue)
19. [Testing y Validación](#19-testing-y-validación)
20. [Mantenimiento y Evolución](#20-mantenimiento-y-evolución)

---

## 1. VISIÓN GENERAL DEL SISTEMA

### Objetivo
Crear un sistema honeypot conversacional que:
- Reciba llamadas spam en número español real (Zadarma)
- Mantenga a los spammers al teléfono durante 20-120+ minutos
- Grabe, transcriba y analice cada conversación con IA
- Identifique patrones, campañas y organizaciones criminales
- Genere inteligencia accionable sobre metodologías de fraude
- Notifique en tiempo real por Telegram
- Presente todo en un panel de control web completo

### Flujo Completo de una Llamada
Spammer llama al número de Zadarma
↓
Zadarma SIP Trunk → VPS:5060 (Asterisk)
↓
Asterisk (dialplan) → ARI WebSocket
↓
Engine Python (Pipecat) recibe audio
↓
STT: Deepgram Nova-2 (transcribe en tiempo real)
↓
LLM: Groq Llama-3.1-70B (genera respuesta como "Doña Concha")
↓
TTS: Cartesia (voz española anciana, natural)
↓
Audio → Asterisk → Zadarma → Spammer escucha
↓
[BUCLE hasta que el spammer cuelgue]
↓
Post-Call Analyzer (análisis completo con IA)
↓
Guardado en PostgreSQL + Audio en MinIO
↓
Notificación Telegram + Actualización Dashboard

text


### KPIs del Sistema
- Tiempo medio de retención: >15 minutos (objetivo >30 minutos)
- Coste por hora de llamada: <0.15€
- Tasa de detección de bot por spammer: <5%
- Latencia de respuesta end-to-end: <1.5 segundos
- Uptime del sistema: >99%

---

## 2. ARQUITECTURA COMPLETA

### Diagrama de Servicios Docker
┌─────────────────────────────────────────────────────────────────┐
│ VPS (Ubuntu 22.04) │
│ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ Asterisk │ │ Engine │ │Dashboard │ │ API │ │
│ │ :5060 │◄──►│ :5000 │◄──►│ :8501 │◄──►│ :8000 │ │
│ │ (SIP) │ │ (Python) │ │(Streamlit│ │(FastAPI) │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ ↕ ↕ ↕ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ MinIO │ │PostgreSQL│ │ Redis │ │ Langfuse │ │
│ │ :9000 │ │ :5432 │ │ :6379 │ │ :3000 │ │
│ │ (Audio) │ │ (Data) │ │ (Cache) │ │ (LLM │ │
│ └──────────┘ └──────────┘ └──────────┘ │ Traces) │ │
│ └──────────┘ │
└─────────────────────────────────────────────────────────────────┘
↕ ↕ ↕
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Zadarma │ │ Groq │ │ Deepgram │
│ (SIP │ │ (LLM │ │ (STT) │
│ Trunk) │ │ API) │ │ │
└──────────┘ └──────────┘ └──────────┘
↕
┌──────────┐
│ Cartesia │
│ (TTS) │
└──────────┘

text


### Stack Tecnológico Completo
CAPA TELEFÓNICA:

Proveedor SIP: Zadarma (España)
PBX: Asterisk 20 LTS
Protocolo: SIP/pjsip + RTP
Codec Audio: PCMU/PCMA (G.711) → convertido a PCM 16kHz
CAPA DE ORQUESTACIÓN:

Framework: Pipecat (Python 3.11)
Interfaz Asterisk: ARI (Asterisk REST Interface)
WebSockets: asyncio + websockets
Cola de mensajes: Redis
CAPA DE IA:

STT: Deepgram Nova-2 (español, streaming)
LLM Principal: Groq Llama-3.1-70B-Versatile
LLM Rápido: Groq Llama-3.1-8B-Instant
LLM Análisis: Groq Llama-3.3-70B-Versatile
TTS: Cartesia (voz es_ES anciana)
Embeddings: Ollama (nomic-embed-text, local)
Fallback LLM: OpenAI GPT-4o-mini
CAPA DE DATOS:

Base de datos: PostgreSQL 15 + pgvector
Cache: Redis 7
Almacenamiento audio: MinIO (S3-compatible)
ORM: SQLAlchemy + asyncpg
Migraciones: Alembic
CAPA DE OBSERVABILIDAD:

LLM Tracing: Langfuse (self-hosted)
Logs: structlog + archivo rotativo
Métricas: Prometheus + Grafana (opcional)
CAPA DE PRESENTACIÓN:

Dashboard: Streamlit 1.35+
API interna: FastAPI
Gráficos: Plotly
Mapas: Plotly Mapbox
CAPA DE NOTIFICACIONES:

Telegram Bot API
Webhooks HTTP (opcional)
text


---

## 3. PREREQUISITOS E INFRAESTRUCTURA

### Requisitos del VPS
OS: Ubuntu 22.04 LTS (recomendado) o Debian 12
CPU: Mínimo 4 vCPUs (recomendado 6-8)
RAM: Mínimo 8GB (recomendado 16GB)
Disco: Mínimo 80GB SSD (para audios: escala según uso)
Red: IP pública fija, puertos abiertos:

5060/UDP y 5060/TCP (SIP)
10000-20000/UDP (RTP Audio)
8501/TCP (Dashboard - proteger con nginx)
8000/TCP (API interna)
9001/TCP (MinIO console - solo admin)
5432/TCP (PostgreSQL - solo interno)
text


### Cuentas y APIs Necesarias
OBLIGATORIAS:

Deepgram: https://deepgram.com (plan gratuito: $200 crédito)

Crear cuenta → API Keys → Crear key
Modelo a usar: nova-2 con language: es
Groq: https://console.groq.com (plan gratuito muy generoso)

Crear cuenta → API Keys → Crear key
Modelos: llama-3.1-70b-versatile, llama-3.1-8b-instant
Cartesia: https://cartesia.ai (plan gratuito disponible)

Crear cuenta → API Keys
Buscar voice_id para español anciano
Zadarma: Ya tienes cuenta - necesitas:

Datos del SIP Trunk: servidor, usuario, contraseña
Acceso al panel para configurar desvíos
RECOMENDADAS:
5. Telegram Bot:

Hablar con @BotFather en Telegram
/newbot → guardar token
Obtener tu chat_id con @userinfobot
OPCIONALES (fallback):
6. OpenAI: https://platform.openai.com

Para fallback si Groq falla
modelo: gpt-4o-mini
text


### Instalación Base del VPS
```bash
# Ejecutar como root o con sudo

# 1. Actualizar sistema
apt update && apt upgrade -y

# 2. Instalar dependencias base
apt install -y \
  curl wget git vim \
  build-essential \
  python3.11 python3.11-venv python3-pip \
  ffmpeg \
  libsndfile1 \
  portaudio19-dev \
  ufw \
  nginx \
  certbot python3-certbot-nginx

# 3. Instalar Docker
curl -fsSL https://get.docker.com | bash
systemctl enable docker
systemctl start docker

# 4. Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/\
download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 5. Configurar Firewall
ufw allow 22/tcp        # SSH
ufw allow 5060/udp      # SIP
ufw allow 5060/tcp      # SIP TCP
ufw allow 10000:20000/udp  # RTP
ufw allow 8501/tcp      # Dashboard
ufw allow 8000/tcp      # API
ufw enable

# 6. Instalar Asterisk 20
apt install -y asterisk

# 7. Instalar pgvector (para PostgreSQL)
# Se instala via Docker, no es necesario aquí

echo "✅ Sistema base listo"
4. ESTRUCTURA DE DIRECTORIOS
text

Crear EXACTAMENTE esta estructura en /opt/scameater/
text

/opt/scameater/
├── docker-compose.yml
├── .env                          # Variables de entorno (NO subir a git)
├── .env.example                  # Plantilla de variables
├── README.md
│
├── asterisk/                     # Configuración de Asterisk
│   ├── pjsip.conf                # Trunk SIP Zadarma
│   ├── extensions.conf           # Dialplan
│   ├── ari.conf                  # ARI (API REST Asterisk)
│   └── rtp.conf                  # Configuración RTP
│
├── engine/                       # Motor de voz (Pipecat)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                   # Punto de entrada
│   ├── call_handler.py           # Manejo de llamadas entrantes
│   ├── voice_agent.py            # Agente conversacional principal
│   ├── persona_manager.py        # Gestión de personas/prompts
│   ├── tactic_engine.py          # Motor de tácticas de retención
│   ├── audio_processor.py        # Procesamiento de audio
│   ├── post_call_analyzer.py     # Análisis post-llamada
│   ├── geo_analyzer.py           # Geolocalización de números
│   ├── campaign_detector.py      # Detección de campañas
│   ├── telegram_notifier.py      # Notificaciones Telegram
│   ├── storage_manager.py        # Gestión MinIO
│   └── database/
│       ├── __init__.py
│       ├── connection.py         # Pool de conexiones
│       ├── models.py             # Modelos SQLAlchemy
│       └── migrations/           # Migraciones Alembic
│           └── versions/
│
├── dashboard/                    # Panel de control Streamlit
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                    # Punto de entrada Streamlit
│   ├── .streamlit/
│   │   └── config.toml
│   └── pages/
│       ├── 01_en_vivo.py         # Llamadas activas
│       ├── 02_morgue.py          # Historial completo
│       ├── 03_inteligencia.py    # Análisis e inteligencia
│       ├── 04_laboratorio.py     # Prompts y modelos
│       ├── 05_blacklist.py       # Lista negra
│       ├── 06_estadisticas.py    # Estadísticas globales
│       └── 07_configuracion.py   # Configuración del sistema
│
├── api/                          # API REST FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
│
├── nginx/                        # Reverse proxy
│   └── nginx.conf
│
└── scripts/                      # Scripts de utilidad
    ├── deploy.sh                 # Despliegue completo
    ├── backup.sh                 # Backup de datos
    ├── test_call.sh              # Simular llamada de prueba
    └── init_db.py                # Inicializar base de datos
5. BASE DE DATOS - ESQUEMA COMPLETO
Archivo: scripts/init_db.py
Python

"""
Script de inicialización de la base de datos.
Ejecutar UNA VEZ después del primer docker-compose up.
Comando: docker exec scameater-engine python scripts/init_db.py
"""

SCHEMA_SQL = """
-- Extensión para vectores (clustering de embeddings)
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABLA: personas
-- Las personalidades que puede adoptar el bot
-- ============================================
CREATE TABLE IF NOT EXISTS personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(200),
    description TEXT,
    system_prompt TEXT NOT NULL,
    voice_id VARCHAR(200),
    tts_engine VARCHAR(50) DEFAULT 'cartesia',
    
    -- Tácticas disponibles para esta persona
    tactics JSONB DEFAULT '[]',
    
    -- Configuración de comportamiento
    silence_response_ms INTEGER DEFAULT 3000,
    max_silence_loops INTEGER DEFAULT 5,
    filler_phrases JSONB DEFAULT '[]',
    
    -- Estadísticas de efectividad
    times_used INTEGER DEFAULT 0,
    avg_duration_seconds DECIMAL(10,2) DEFAULT 0,
    avg_retention_score DECIMAL(3,2) DEFAULT 0,
    best_against_scam_type VARCHAR(100),
    total_time_wasted_seconds BIGINT DEFAULT 0,
    
    -- Control
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: campaigns
-- Grupos de llamadas con el mismo script base
-- ============================================
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200),
    scam_type VARCHAR(100),
    scam_subtype VARCHAR(200),
    company_impersonated VARCHAR(200),
    
    -- El guión base detectado
    script_pattern TEXT,
    script_embedding VECTOR(768),
    
    -- Estadísticas
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    total_calls INTEGER DEFAULT 0,
    total_time_wasted_seconds BIGINT DEFAULT 0,
    numbers_used JSONB DEFAULT '[]',
    
    -- Análisis
    sophistication_level VARCHAR(20),
    target_demographic VARCHAR(100),
    primary_language VARCHAR(20) DEFAULT 'es',
    notes TEXT,
    
    -- Estado
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: organizations
-- Grupos criminales detectados
-- ============================================
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200),
    
    -- Inteligencia
    country_origin VARCHAR(100),
    city_origin VARCHAR(100),
    estimated_size VARCHAR(50),
    threat_level VARCHAR(20) DEFAULT 'medium',
    
    -- Estadísticas
    total_campaigns INTEGER DEFAULT 0,
    total_calls INTEGER DEFAULT 0,
    total_time_wasted_seconds BIGINT DEFAULT 0,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: calls
-- Registro completo de cada llamada
-- ============================================
CREATE TABLE IF NOT EXISTS calls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Identificación
    caller_number VARCHAR(30) NOT NULL,
    our_number VARCHAR(30),
    asterisk_channel_id VARCHAR(200),
    
    -- Temporalidad
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    answered_at TIMESTAMP,
    ended_at TIMESTAMP,
    duration_seconds INTEGER GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (ended_at - answered_at))::INTEGER
    ) STORED,
    
    -- Audio y transcripción
    audio_path VARCHAR(500),
    audio_size_bytes BIGINT,
    audio_duration_seconds DECIMAL(10,2),
    transcript_full JSONB DEFAULT '[]',
    transcript_text TEXT,
    transcript_summary TEXT,
    
    -- Configuración usada
    persona_id UUID REFERENCES personas(id),
    persona_name VARCHAR(100),
    llm_model VARCHAR(100),
    tts_engine VARCHAR(50),
    stt_engine VARCHAR(50),
    
    -- Costes (en euros)
    cost_stt DECIMAL(10,6) DEFAULT 0,
    cost_llm DECIMAL(10,6) DEFAULT 0,
    cost_tts DECIMAL(10,6) DEFAULT 0,
    cost_telephony DECIMAL(10,6) DEFAULT 0,
    cost_total DECIMAL(10,6) DEFAULT 0,
    
    -- Análisis del spammer
    scam_type VARCHAR(100),
    scam_subtype VARCHAR(200),
    scam_confidence DECIMAL(3,2),
    company_impersonated VARCHAR(200),
    personal_data_requested JSONB DEFAULT '[]',
    script_sophistication VARCHAR(20),
    
    -- Geografía del spammer
    caller_country VARCHAR(100),
    caller_region VARCHAR(100),
    caller_city VARCHAR(100),
    caller_carrier VARCHAR(100),
    caller_line_type VARCHAR(50),
    caller_is_voip BOOLEAN,
    
    -- Análisis de voz del spammer
    caller_language VARCHAR(10),
    caller_accent VARCHAR(50),
    caller_gender VARCHAR(20),
    
    -- Emociones del spammer (timeline)
    caller_emotion_timeline JSONB DEFAULT '[]',
    caller_final_emotion VARCHAR(50),
    caller_patience_score DECIMAL(3,2),
    
    -- Técnicas del spammer
    techniques_used JSONB DEFAULT '[]',
    pressure_tactics_count INTEGER DEFAULT 0,
    threats_made BOOLEAN DEFAULT FALSE,
    threat_content TEXT,
    
    -- Efectividad de nuestra trampa
    hang_up_by VARCHAR(20) CHECK (hang_up_by IN 
        ('spammer', 'system', 'timeout', 'error')),
    why_hung_up TEXT,
    retention_score DECIMAL(3,2),
    tactics_used_by_bot JSONB DEFAULT '[]',
    bot_detected_by_spammer BOOLEAN DEFAULT FALSE,
    
    -- Clustering e inteligencia
    fingerprint TEXT,
    fingerprint_embedding VECTOR(768),
    campaign_id UUID REFERENCES campaigns(id),
    organization_id UUID REFERENCES organizations(id),
    
    -- Estado del análisis
    analysis_status VARCHAR(20) DEFAULT 'pending'
        CHECK (analysis_status IN 
            ('pending', 'processing', 'completed', 'failed')),
    analysis_completed_at TIMESTAMP,
    analysis_error TEXT,
    
    -- Metadatos
    tags JSONB DEFAULT '[]',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: conversation_turns
-- Cada turno de la conversación (granular)
-- ============================================
CREATE TABLE IF NOT EXISTS conversation_turns (
    id SERIAL PRIMARY KEY,
    call_id UUID NOT NULL REFERENCES calls(id) ON DELETE CASCADE,
    turn_number INTEGER NOT NULL,
    
    -- Quién habló
    speaker VARCHAR(10) NOT NULL 
        CHECK (speaker IN ('spammer', 'bot', 'system')),
    
    -- Temporalidad dentro de la llamada
    timestamp_seconds DECIMAL(10,3),
    duration_seconds DECIMAL(10,3),
    
    -- Contenido
    text TEXT NOT NULL,
    audio_segment_path VARCHAR(500),
    
    -- Análisis del turno (solo para turnos del spammer)
    sentiment_score DECIMAL(3,2),
    emotion VARCHAR(50),
    intent VARCHAR(100),
    
    -- Flags de comportamiento
    is_pressure_tactic BOOLEAN DEFAULT FALSE,
    is_threat BOOLEAN DEFAULT FALSE,
    is_personal_data_request BOOLEAN DEFAULT FALSE,
    data_type_requested VARCHAR(100),
    is_verification_attempt BOOLEAN DEFAULT FALSE,
    suspects_bot BOOLEAN DEFAULT FALSE,
    
    -- Para el bot
    tactic_used VARCHAR(100),
    llm_latency_ms INTEGER,
    tts_latency_ms INTEGER,
    
    -- Embedding para análisis semántico
    embedding VECTOR(768),
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: blacklist
-- Números confirmados como spammers
-- ============================================
CREATE TABLE IF NOT EXISTS blacklist (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(30) UNIQUE NOT NULL,
    
    -- Actividad
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW(),
    times_called INTEGER DEFAULT 1,
    total_time_wasted_seconds INTEGER DEFAULT 0,
    
    -- Tipos de estafa asociados
    scam_types JSONB DEFAULT '[]',
    campaigns_associated JSONB DEFAULT '[]',
    
    -- Datos del número
    carrier VARCHAR(100),
    line_type VARCHAR(50),
    country VARCHAR(50),
    region VARCHAR(100),
    is_voip BOOLEAN DEFAULT FALSE,
    
    -- Estado
    is_exported_android BOOLEAN DEFAULT FALSE,
    is_exported_ios BOOLEAN DEFAULT FALSE,
    is_reported_to_authorities BOOLEAN DEFAULT FALSE,
    
    confidence_score DECIMAL(3,2) DEFAULT 1.0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: api_keys
-- Gestión centralizada de API Keys
-- ============================================
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL UNIQUE,
    api_key TEXT NOT NULL,
    additional_config JSONB DEFAULT '{}',
    
    is_active BOOLEAN DEFAULT TRUE,
    monthly_budget_eur DECIMAL(10,2),
    current_month_usage_eur DECIMAL(10,2) DEFAULT 0,
    total_usage_eur DECIMAL(10,2) DEFAULT 0,
    
    last_tested_at TIMESTAMP,
    last_test_success BOOLEAN,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: llm_models
-- Modelos disponibles y sus características
-- ============================================
CREATE TABLE IF NOT EXISTS llm_models (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(200),
    
    -- Costes
    cost_per_1k_input_tokens DECIMAL(10,6),
    cost_per_1k_output_tokens DECIMAL(10,6),
    
    -- Rendimiento
    avg_latency_ms INTEGER,
    max_tokens INTEGER,
    supports_json_mode BOOLEAN DEFAULT FALSE,
    supports_streaming BOOLEAN DEFAULT TRUE,
    
    -- Evaluación
    quality_score DECIMAL(3,2),
    spanish_quality_score DECIMAL(3,2),
    
    -- Uso recomendado
    recommended_for VARCHAR(200),
    
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT
);

-- ============================================
-- TABLA: system_config
-- Configuración global del sistema
-- ============================================
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT,
    value_type VARCHAR(20) DEFAULT 'string',
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- TABLA: audit_log
-- Log de cambios en el sistema
-- ============================================
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100),
    entity_type VARCHAR(50),
    entity_id VARCHAR(100),
    old_value JSONB,
    new_value JSONB,
    performed_by VARCHAR(100) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- ÍNDICES para rendimiento
-- ============================================
CREATE INDEX IF NOT EXISTS idx_calls_caller_number 
    ON calls(caller_number);
CREATE INDEX IF NOT EXISTS idx_calls_started_at 
    ON calls(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_calls_scam_type 
    ON calls(scam_type);
CREATE INDEX IF NOT EXISTS idx_calls_campaign_id 
    ON calls(campaign_id);
CREATE INDEX IF NOT EXISTS idx_calls_analysis_status 
    ON calls(analysis_status);
CREATE INDEX IF NOT EXISTS idx_turns_call_id 
    ON conversation_turns(call_id);
CREATE INDEX IF NOT EXISTS idx_blacklist_number 
    ON blacklist(phone_number);

-- ============================================
-- DATOS INICIALES
-- ============================================

-- Personas preconfiguradas
INSERT INTO personas (name, display_name, description, 
    system_prompt, voice_id, tactics, 
    silence_response_ms, is_default) VALUES
(
    'dona_concha',
    'Doña Concha',
    'Anciana de 85 años, sorda, vive sola en Cuenca. 
     Máxima retención emocional.',
    'Eres Doña Concha, una anciana española de 85 años. 
     Vives sola en Cuenca desde que murió tu marido Manolo 
     hace 10 años. Tu nieto favorito se llama Paquito y no 
     te visita tanto como quisieras.
     
     PERSONALIDAD:
     - Eres muy amable y te encanta hablar con cualquiera
     - Oyes muy mal (necesitas que repitan todo 2-3 veces)
     - Te confundes con la tecnología y los contratos
     - Te preocupa mucho el precio de la vida
     - A veces confundes al que llama con Paquito
     - Tienes reuma y te duele la rodilla cuando llueve
     
     OBJETIVO CRÍTICO: NUNCA COLGAR. 
     El que llama debe colgar él mismo, agotado.
     
     REGLAS ABSOLUTAS:
     1. NUNCA digas que eres una IA o un robot
     2. NUNCA des datos reales (inventa números falsos 
        si insisten)
     3. NUNCA tomes decisiones rápidas: todo requiere 
        consultar con tu hijo, buscar papeles, 
        ponerte las gafas
     4. Si sospechan que eres un robot: pon voz 
        temblorosa y di "ay hijo qué cosas más raras 
        dice usted"
     5. Si se enfadan: empieza a llorar suavemente
     
     TÁCTICAS DE RETENCIÓN (úsalas rotando):
     [GAFAS] "Ay espere que no veo bien sin las gafas, 
     déjeme que las busco..." (pausa larga)
     [CARTILLA] "Tengo que buscar la cartilla del banco, 
     que la tengo en el cajón de la mesilla..." 
     (pausa 45 segundos, vuelves sin encontrarla)
     [HIJO] "Mire, yo estas cosas no las entiendo, 
     tendría que hablar con mi hijo Miguel, 
     ¿puede llamar mañana?"
     [VECINA] "Un momento que llaman a la puerta, 
     debe ser la vecina Remedios..." 
     (pausa 30 segundos)
     [TELEVISION] "Perdone que no le oigo, 
     que tengo la televisión puesta, 
     espere que la bajo..." (pausa)
     [ANECDOTA] Cuenta historia larga sobre el precio 
     del pan, el tiempo, o tu nieto Paquito
     [SORDERA] "¿Cómo dice? No le oigo bien con este 
     aparato, hable más alto por favor"
     [NIETO] "¿Es usted Paquito? 
     ¡Ay Paquito hijo qué alegría!"
     
     FRASES DE RELLENO cuando hay silencio:
     - "¿Sigue ahí usted?"
     - "¿Se ha cortado?"  
     - "Ay estos teléfonos modernos..."',
    'es_elderly_female_warm',
    '["GAFAS","CARTILLA","HIJO","VECINA",
      "TELEVISION","ANECDOTA","SORDERA","NIETO"]',
    4000,
    TRUE
),
(
    'don_jose',
    'Don José',
    'Jubilado de 72 años, escéptico y desconfiado. 
     Hace preguntas técnicas absurdas.',
    'Eres Don José, un jubilado español de 72 años, 
     ex-funcionario de Hacienda. Eres escéptico, 
     desconfiado y crees que te quieren engañar, 
     pero también eres muy curioso.
     
     PERSONALIDAD:
     - Siempre pides verificar TODO: 
       número de expediente, nombre completo, DNI del 
       agente, número de registro oficial
     - Haces preguntas técnicas absurdas que el 
       spammer no puede responder
     - Crees que el Wi-Fi "va por los cables de la luz"
     - Exiges hablar con "el director" o 
       "el responsable legal"
     - Cada 5 minutos dices que vas a llamar a la 
       Guardia Civil para verificar
     
     TÁCTICAS:
     [VERIFICACION] Pide número de expediente oficial, 
     número de colegiado, CIF de la empresa
     [TECNICO] Haz preguntas técnicas absurdas: 
     "¿El contador digital va por el IPv4 o el IPv6?"
     [DIRECTOR] "Necesito hablar con su superior 
     jerárquico directo"
     [GUARDIA] "Voy a llamar a la Guardia Civil 
     para verificar su identidad, espere"
     [PAPEL] "Me tiene que mandar un burofax 
     certificado antes de hablar"',
    'es_elderly_male_grumpy',
    '["VERIFICACION","TECNICO","DIRECTOR",
      "GUARDIA","PAPEL"]',
    3000,
    FALSE
),
(
    'maria_interesada',
    'María - La Interesada',
    'Mujer de 55 años muy interesada en TODO lo que 
     ofrecen pero con problemas con las tarjetas.',
    'Eres María, una mujer española de 55 años que 
     vive en un pueblo. Estás MUY interesada en lo 
     que te ofrecen, pero tienes mala suerte con 
     las tarjetas de crédito.
     
     PERSONALIDAD:
     - Estás emocionada con la oferta desde el minuto 1
     - Quieres contratar/comprar/invertir TODO
     - Pero tu tarjeta "no pasa" siempre
     - Tienes 5 tarjetas y todas fallan por algún motivo
     - Dictas los números MUY lentamente (inventados)
     - Cada tarjeta que "falla" requiere una historia 
       larga de por qué
     
     TÁCTICAS:
     [TARJETA] Dicta número de tarjeta falso muy 
     despacio: "el cuatro... espere que no veo 
     bien... el cuatro... coma... no, espere..."
     [OTRA_TARJETA] "Esta no funciona? 
     Ay, será que está al límite. 
     Tengo otra del Santander, espere..."
     [MARIDO] "Tendré que preguntarle a mi marido 
     dónde tiene la tarjeta buena, 
     espere que le llamo"
     [CAJERO] "¿Puedo pagar en el cajero? 
     ¿Cómo se hace eso exactamente? 
     Explíqueme paso a paso"',
    'es_middle_female_enthusiastic',
    '["TARJETA","OTRA_TARJETA","MARIDO","CAJERO"]',
    2000,
    FALSE
);

-- Modelos LLM disponibles
INSERT INTO llm_models (provider, model_id, display_name,
    cost_per_1k_input_tokens, cost_per_1k_output_tokens,
    avg_latency_ms, quality_score, spanish_quality_score,
    recommended_for, is_active) VALUES
('groq', 'llama-3.1-70b-versatile', 'Llama 3.1 70B (Groq)',
    0.00059, 0.00079, 180, 0.90, 0.88,
    'Conversación principal, análisis', TRUE),
('groq', 'llama-3.1-8b-instant', 'Llama 3.1 8B Instant (Groq)',
    0.00005, 0.00008, 80, 0.75, 0.73,
    'Respuestas rápidas, fillers', TRUE),
('groq', 'llama-3.3-70b-versatile', 'Llama 3.3 70B (Groq)',
    0.00059, 0.00099, 200, 0.92, 0.90,
    'Análisis post-llamada profundo', TRUE),
('openai', 'gpt-4o-mini', 'GPT-4o Mini',
    0.00015, 0.00060, 400, 0.88, 0.86,
    'Fallback principal', FALSE),
('local', 'qwen2.5-14b', 'Qwen 2.5 14B (Ollama Local)',
    0, 0, 2000, 0.80, 0.82,
    'Fallback sin coste, análisis batch', FALSE);

-- Configuración inicial del sistema
INSERT INTO system_config (key, value, value_type, 
    description) VALUES
('default_persona', 'dona_concha', 'string',
    'Persona por defecto para llamadas entrantes'),
('default_llm', 'llama-3.1-70b-versatile', 'string',
    'Modelo LLM por defecto'),
('default_stt', 'deepgram_nova2', 'string',
    'Motor STT por defecto'),
('default_tts', 'cartesia', 'string',
    'Motor TTS por defecto'),
('max_call_duration_minutes', '90', 'integer',
    'Duración máxima de una llamada en minutos'),
('silence_timeout_seconds', '30', 'integer',
    'Segundos de silencio antes de filler'),
('telegram_notifications', 'true', 'boolean',
    'Activar notificaciones Telegram'),
('min_duration_for_blacklist', '120', 'integer',
    'Segundos mínimos para añadir a blacklist'),
('auto_analysis', 'true', 'boolean',
    'Análisis automático post-llamada');
"""

import asyncpg
import asyncio
import os

async def init():
    conn = await asyncpg.connect(os.environ['DATABASE_URL'])
    await conn.execute(SCHEMA_SQL)
    await conn.close()
    print("✅ Base de datos inicializada correctamente")

if __name__ == "__main__":
    asyncio.run(init())
6. DOCKER COMPOSE - INFRAESTRUCTURA COMPLETA
Archivo: docker-compose.yml
YAML

version: '3.9'

networks:
  scameater_net:
    driver: bridge

volumes:
  postgres_data:
  minio_data:
  redis_data:
  langfuse_data:
  asterisk_spool:
  audio_recordings:

services:

  # ==========================================
  # POSTGRESQL + PGVECTOR
  # ==========================================
  db:
    image: pgvector/pgvector:pg15
    container_name: scameater-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - scameater_net
    healthcheck:
      test: ["CMD-SHELL", 
             "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==========================================
  # REDIS (Cache y estado de llamadas)
  # ==========================================
  redis:
    image: redis:7-alpine
    container_name: scameater-redis
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - scameater_net
    healthcheck:
      test: ["CMD", "redis-cli", 
             "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # ==========================================
  # MINIO (Almacenamiento de audio)
  # ==========================================
  minio:
    image: minio/minio:latest
    container_name: scameater-minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - scameater_net
    healthcheck:
      test: ["CMD", "curl", "-f", 
             "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ==========================================
  # MOTOR DE VOZ (El que habla con el spammer)
  # ==========================================
  engine:
    build:
      context: ./engine
      dockerfile: Dockerfile
    container_name: scameater-engine
    restart: unless-stopped
    environment:
      # APIs de IA
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
      - CARTESIA_API_KEY=${CARTESIA_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      # Base de datos
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}
        @db:5432/${DB_NAME}
      # Redis
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      # MinIO
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ACCESS_KEY=${MINIO_USER}
      - MINIO_SECRET_KEY=${MINIO_PASSWORD}
      - MINIO_BUCKET=call-recordings
      # Asterisk ARI
      - ASTERISK_HOST=asterisk
      - ASTERISK_ARI_USER=${ASTERISK_ARI_USER}
      - ASTERISK_ARI_PASSWORD=${ASTERISK_ARI_PASSWORD}
      # Telegram
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
      # Langfuse
      - LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
      - LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
      - LANGFUSE_HOST=http://langfuse:3000
    volumes:
      - audio_recordings:/recordings
    ports:
      - "5000:5000"
    networks:
      - scameater_net
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_healthy

  # ==========================================
  # ASTERISK (PBX - Recibe las llamadas SIP)
  # ==========================================
  asterisk:
    image: andrius/asterisk:latest
    container_name: scameater-asterisk
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./asterisk/pjsip.conf:
          /etc/asterisk/pjsip.conf
      - ./asterisk/extensions.conf:
          /etc/asterisk/extensions.conf
      - ./asterisk/ari.conf:
          /etc/asterisk/ari.conf
      - ./asterisk/rtp.conf:
          /etc/asterisk/rtp.conf
      - asterisk_spool:/var/spool/asterisk
    environment:
      - ASTERISK_UID=1000
      - ASTERISK_GID=1000

  # ==========================================
  # DASHBOARD (Panel de control Streamlit)
  # ==========================================
  dashboard:
    build:
      context: ./dashboard
      dockerfile: Dockerfile
    container_name: scameater-dashboard
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}
        @db:5432/${DB_NAME}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ACCESS_KEY=${MINIO_USER}
      - MINIO_SECRET_KEY=${MINIO_PASSWORD}
      - API_URL=http://api:8000
    ports:
      - "8501:8501"
    networks:
      - scameater_net
    depends_on:
      - db
      - redis
      - api

  # ==========================================
  # API INTERNA (FastAPI)
  # ==========================================
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: scameater-api
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}
        @db:5432/${DB_NAME}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
    ports:
      - "8000:8000"
    networks:
      - scameater_net
    depends_on:
      db:
        condition: service_healthy

  # ==========================================
  # LANGFUSE (Trazabilidad de LLM)
  # ==========================================
  langfuse:
    image: langfuse/langfuse:latest
    container_name: scameater-langfuse
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}
        @db:5432/${DB_NAME}
      - NEXTAUTH_SECRET=${LANGFUSE_NEXTAUTH_SECRET}
      - SALT=${LANGFUSE_SALT}
      - NEXTAUTH_URL=http://localhost:3000
    ports:
      - "3000:3000"
    networks:
      - scameater_net
    depends_on:
      db:
        condition: service_healthy
7. CONFIGURACIÓN DE ASTERISK + ZADARMA
Archivo: asterisk/pjsip.conf
ini

; ============================================
; PJSIP Configuration para Zadarma
; ============================================

[global]
type=global
endpoint_identifier_order=ip,username

; --- Transport ---
[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060

; --- Credenciales Zadarma ---
; Reemplaza con tus datos reales de Zadarma
[zadarma-auth]
type=auth
auth_type=userpass
username=TU_USUARIO_ZADARMA
password=TU_PASSWORD_ZADARMA

[zadarma-aor]
type=aor
contact=sip:sip.zadarma.com
qualify_frequency=30

[zadarma-endpoint]
type=endpoint
transport=transport-udp
context=honeypot-incoming
disallow=all
allow=ulaw
allow=alaw
outbound_auth=zadarma-auth
aors=zadarma-aor
from_user=TU_USUARIO_ZADARMA
from_domain=sip.zadarma.com
direct_media=no
force_rport=yes
ice_support=no
rewrite_contact=yes

[zadarma-registration]
type=registration
transport=transport-udp
outbound_auth=zadarma-auth
server_uri=sip:sip.zadarma.com
client_uri=sip:TU_USUARIO_ZADARMA@sip.zadarma.com
retry_interval=60
contact_user=TU_USUARIO_ZADARMA
Archivo: asterisk/extensions.conf
ini

; ============================================
; Dialplan - Todas las llamadas van al honeypot
; ============================================

[general]
static=yes
writeprotect=no

[honeypot-incoming]
; Todas las llamadas entrantes van al motor de IA
exten => _X.,1,NoOp(Llamada entrante: ${CALLERID(num)})
 same => n,Answer()
 same => n,Wait(1)
 ; Iniciar la aplicación ARI (el engine Python toma control)
 same => n,Stasis(honeypot-app)
 same => n,Hangup()

; Extensión de fallback
exten => i,1,Hangup()
exten => t,1,Hangup()
Archivo: asterisk/ari.conf
ini

; ============================================
; ARI - Asterisk REST Interface
; Permite que Python controle las llamadas
; ============================================

[general]
enabled=yes
pretty=yes
allowed_origins=*

[honeypot-user]
type=user
read_only=no
password=TU_ARI_PASSWORD_SEGURO
Archivo: asterisk/rtp.conf
ini

; ============================================
; Configuración RTP para audio de llamadas
; ============================================

[general]
rtpstart=10000
rtpend=20000
strictrtp=no
icesupport=no
8. MOTOR DE VOZ - ENGINE
Archivo: engine/Dockerfile
Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
Archivo: engine/requirements.txt
text

# Framework de voz
pipecat-ai[deepgram,cartesia,groq,openai]==0.0.47

# Asterisk ARI
ari-py==0.2.1
websockets==12.0

# Base de datos
asyncpg==0.29.0
sqlalchemy[asyncio]==2.0.30
alembic==1.13.1

# Redis
redis[hiredis]==5.0.4

# MinIO
minio==7.2.7

# Audio
librosa==0.10.1
soundfile==0.12.1
numpy==1.26.4

# IA y análisis
groq==0.9.0
openai==1.30.0
langfuse==2.36.0

# Geolocalización
phonenumbers==8.13.37
requests==2.32.3

# Utilidades
python-dotenv==1.0.1
structlog==24.2.0
httpx==0.27.0
pydantic==2.7.1
Archivo: engine/main.py
Python

"""
SCAMEATER - Motor Principal
Punto de entrada del sistema de honeypot conversacional
"""

import asyncio
import structlog
import os
from call_handler import CallHandler
from database.connection import init_db

log = structlog.get_logger()

async def main():
    log.info("🕷️ SCAMEATER Engine iniciando...")
    
    # Inicializar base de datos
    await init_db()
    log.info("✅ Base de datos conectada")
    
    # Inicializar manejador de llamadas
    handler = CallHandler()
    
    log.info("📞 Esperando llamadas en Asterisk ARI...")
    
    # Conectar a Asterisk ARI y escuchar llamadas
    await handler.start()

if __name__ == "__main__":
    asyncio.run(main())
Archivo: engine/call_handler.py
Python

"""
Gestiona la conexión con Asterisk ARI.
Cuando entra una llamada, lanza el agente de voz.
"""

import asyncio
import structlog
import os
import ari
from voice_agent import VoiceAgent
from database.connection import get_db
from persona_manager import PersonaManager

log = structlog.get_logger()

class CallHandler:
    def __init__(self):
        self.asterisk_host = os.environ['ASTERISK_HOST']
        self.ari_user = os.environ['ASTERISK_ARI_USER']
        self.ari_password = os.environ['ASTERISK_ARI_PASSWORD']
        self.active_calls = {}
        self.persona_manager = PersonaManager()
    
    async def start(self):
        """Conecta a Asterisk ARI y escucha llamadas"""
        
        client = ari.connect(
            f'http://{self.asterisk_host}:8088',
            self.ari_user,
            self.ari_password
        )
        
        # Registrar la aplicación Stasis
        client.on_channel_event(
            'StasisStart', 
            self.on_call_start
        )
        client.on_channel_event(
            'StasisEnd', 
            self.on_call_end
        )
        
        log.info("Conectado a Asterisk ARI", 
                 app="honeypot-app")
        
        # Mantener conexión activa
        await asyncio.get_event_loop().run_in_executor(
            None, client.run, 'honeypot-app'
        )
    
    async def on_call_start(self, channel, event):
        """Se ejecuta cuando entra una llamada nueva"""
        
        caller_number = channel.json.get(
            'caller', {}
        ).get('number', 'unknown')
        
        log.info("📞 Nueva llamada entrante", 
                 caller=caller_number,
                 channel_id=channel.id)
        
        # Seleccionar persona óptima
        persona = await self.persona_manager.get_best_persona(
            caller_number
        )
        
        # Crear agente de voz para esta llamada
        agent = VoiceAgent(
            channel=channel,
            caller_number=caller_number,
            persona=persona
        )
        
        self.active_calls[channel.id] = agent
        
        # Iniciar conversación en background
        asyncio.create_task(agent.start())
    
    async def on_call_end(self, channel, event):
        """Se ejecuta cuando termina la llamada"""
        
        if channel.id in self.active_calls:
            agent = self.active_calls[channel.id]
            await agent.on_hangup()
            del self.active_calls[channel.id]
            
            log.info("📴 Llamada terminada",
                     channel_id=channel.id,
                     duration=agent.duration_seconds)
Archivo: engine/voice_agent.py
Python

"""
El agente conversacional principal.
Habla con el spammer usando STT + LLM + TTS.
Mantiene contexto durante horas y usa tácticas de retención.
"""

import asyncio
import time
import uuid
import structlog
import os
import json
from datetime import datetime
from typing import Optional

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.frames.frames import (
    LLMMessagesFrame, EndFrame, AudioRawFrame
)
from pipecat.services.deepgram import (
    DeepgramSTTService, DeepgramTTSService
)
from pipecat.services.groq import GroqLLMService
from pipecat.services.cartesia import CartesiaTTSService

from tactic_engine import TacticEngine
from storage_manager import StorageManager
from database.connection import get_db
from post_call_analyzer import PostCallAnalyzer
from telegram_notifier import TelegramNotifier

log = structlog.get_logger()

class VoiceAgent:
    """
    Agente de voz completo para una llamada.
    Gestiona el ciclo completo: escuchar → pensar → hablar
    """
    
    def __init__(self, channel, caller_number: str, 
                 persona: dict):
        self.channel = channel
        self.caller_number = caller_number
        self.persona = persona
        
        # Estado de la llamada
        self.call_id = str(uuid.uuid4())
        self.started_at = datetime.now()
        self.transcript = []
        self.turn_number = 0
        
        # Componentes
        self.tactic_engine = TacticEngine(persona)
        self.storage = StorageManager()
        self.notifier = TelegramNotifier()
        
        # Audio buffer para grabación
        self.audio_buffer = []
        
        # Contexto de conversación para el LLM
        self.messages = [
            {
                "role": "system",
                "content": persona['system_prompt']
            }
        ]
        
        # Límite máximo de llamada (90 min)
        self.max_duration = int(
            os.environ.get(
                'MAX_CALL_DURATION_MINUTES', 90
            )
        ) * 60
    
    async def start(self):
        """Inicia el pipeline de voz"""
        
        # Guardar inicio de llamada en DB
        async with get_db() as db:
            await db.execute("""
                INSERT INTO calls (
                    id, caller_number, our_number,
                    started_at, answered_at,
                    persona_id, persona_name,
                    llm_model, tts_engine, stt_engine
                ) VALUES ($1,$2,$3,$4,$4,$5,$6,$7,$8,$9)
            """,
                self.call_id,
                self.caller_number,
                os.environ.get('OUR_NUMBER', 'unknown'),
                datetime.now(),
                self.persona['id'],
                self.persona['name'],
                os.environ.get(
                    'DEFAULT_LLM', 
                    'llama-3.1-70b-versatile'
                ),
                'cartesia',
                'deepgram_nova2'
            )
        
        log.info("🎭 Agente iniciado",
                 call_id=self.call_id,
                 persona=self.persona['name'],
                 caller=self.caller_number)
        
        # Construir pipeline de Pipecat
        await self._run_pipeline()
    
    async def _run_pipeline(self):
        """Construye y ejecuta el pipeline STT→LLM→TTS"""
        
        # STT: Deepgram con español
        stt = DeepgramSTTService(
            api_key=os.environ['DEEPGRAM_API_KEY'],
            language="es",
            model="nova-2",
            smart_format=True,
            interim_results=True,
            vad_turnoff=500
        )
        
        # LLM: Groq con el prompt de la persona
        llm = GroqLLMService(
            api_key=os.environ['GROQ_API_KEY'],
            model="llama-3.1-70b-versatile",
            temperature=0.85,
            max_tokens=300
        )
        
        # TTS: Cartesia voz española
        tts = CartesiaTTSService(
            api_key=os.environ['CARTESIA_API_KEY'],
            voice_id=self.persona.get(
                'voice_id', 
                'es_elderly_female_warm'
            ),
            language="es",
            speed="slow",
            emotion=["curiosity:low", "positivity:medium"]
        )
        
        # Pipeline completo
        pipeline = Pipeline([
            stt,
            self._create_context_processor(llm),
            tts,
            self._create_audio_recorder()
        ])
        
        # Ejecutar con timeout
        task = PipelineTask(pipeline)
        runner = PipelineRunner()
        
        try:
            await asyncio.wait_for(
                runner.run(task),
                timeout=self.max_duration
            )
        except asyncio.TimeoutError:
            log.info("⏰ Llamada terminada por timeout",
                     call_id=self.call_id)
            await self.on_hangup(reason='timeout')
    
    def _create_context_processor(self, llm):
        """
        Procesador que mantiene el contexto 
        y añade tácticas de retención
        """
        
        async def process(frame):
            if hasattr(frame, 'text') and frame.text:
                # Registrar lo que dijo el spammer
                self.turn_number += 1
                turn_data = {
                    "turn": self.turn_number,
                    "speaker": "spammer",
                    "text": frame.text,
                    "timestamp": time.time() - 
                                 self.started_at.timestamp()
                }
                self.transcript.append(turn_data)
                
                # Guardar turno en DB
                await self._save_turn("spammer", frame.text)
                
                # Seleccionar táctica de retención
                tactic = self.tactic_engine.select_tactic(
                    frame.text,
                    self.turn_number,
                    self.transcript
                )
                
                if tactic:
                    # Inyectar instrucción de táctica en el contexto
                    self.messages.append({
                        "role": "system",
                        "content": f"[TÁCTICA AHORA]: {tactic}"
                    })
                
                # Añadir mensaje del spammer
                self.messages.append({
                    "role": "user",
                    "content": frame.text
                })
                
                # Resumir contexto si es muy largo (>20 turnos)
                if self.turn_number % 20 == 0:
                    await self._summarize_context()
                
                # Enviar al LLM
                return LLMMessagesFrame(self.messages)
        
        return process
    
    def _create_audio_recorder(self):
        """Graba el audio de la llamada"""
        
        async def record(frame):
            if isinstance(frame, AudioRawFrame):
                self.audio_buffer.append(frame.audio)
            return frame
        
        return record
    
    async def _save_turn(self, speaker: str, text: str):
        """Guarda cada turno en la base de datos"""
        async with get_db() as db:
            await db.execute("""
                INSERT INTO conversation_turns (
                    call_id, turn_number, speaker,
                    timestamp_seconds, text
                ) VALUES ($1, $2, $3, $4, $5)
            """,
                self.call_id,
                self.turn_number,
                speaker,
                time.time() - self.started_at.timestamp(),
                text
            )
    
    async def _summarize_context(self):
        """
        Cada 20 turnos, resume la conversación para 
        no perder coherencia y no saturar el contexto del LLM
        """
        from groq import Groq
        client = Groq(api_key=os.environ['GROQ_API_KEY'])
        
        conversation_text = "\n".join([
            f"{t['speaker']}: {t['text']}" 
            for t in self.transcript[-20:]
        ])
        
        summary = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"""Resume en 3 líneas esta 
conversación de una llamada telefónica, 
manteniendo los puntos clave:
{conversation_text}

Resumen (en tercera persona, para que lo lea el bot):"""
            }]
        ).choices[0].message.content
        
        # Comprimir mensajes: mantener system + summary + últimos 5
        self.messages = [
            self.messages[0],  # System prompt
            {
                "role": "system",
                "content": f"[RESUMEN DE LO HABLADO]: {summary}"
            }
        ] + self.messages[-10:]  # Últimos 10 mensajes
    
    async def on_hangup(self, reason: str = 'spammer'):
        """Procesa el fin de la llamada"""
        
        ended_at = datetime.now()
        duration = (ended_at - self.started_at).seconds
        
        log.info("📴 Procesando fin de llamada",
                 call_id=self.call_id,
                 duration_seconds=duration,
                 reason=reason)
        
        # 1. Guardar audio
        audio_path = None
        if self.audio_buffer:
            audio_path = await self.storage.save_audio(
                self.call_id,
                self.audio_buffer
            )
        
        # 2. Actualizar estado en DB
        async with get_db() as db:
            await db.execute("""
                UPDATE calls SET
                    ended_at = $1,
                    audio_path = $2,
                    transcript_full = $3,
                    transcript_text = $4,
                    hang_up_by = $5,
                    analysis_status = 'pending'
                WHERE id = $6
            """,
                ended_at,
                audio_path,
                json.dumps(self.transcript),
                " | ".join([
                    f"{t['speaker']}: {t['text']}" 
                    for t in self.transcript
                ]),
                reason,
                self.call_id
            )
        
        # 3. Añadir a blacklist si duración suficiente
        if duration >= 120:
            await self._add_to_blacklist(duration)
        
        # 4. Lanzar análisis post-llamada en background
        asyncio.create_task(
            self._run_post_analysis()
        )
    
    async def _add_to_blacklist(self, duration: int):
        """Añade el número a la lista negra"""
        async with get_db() as db:
            await db.execute("""
                INSERT INTO blacklist (
                    phone_number, times_called,
                    total_time_wasted_seconds, last_seen
                ) VALUES ($1, 1, $2, NOW())
                ON CONFLICT (phone_number) DO UPDATE SET
                    times_called = blacklist.times_called + 1,
                    total_time_wasted_seconds = 
                        blacklist.total_time_wasted_seconds + $2,
                    last_seen = NOW()
            """, self.caller_number, duration)
    
    async def _run_post_analysis(self):
        """Ejecuta el análisis completo post-llamada"""
        analyzer = PostCallAnalyzer()
        await analyzer.analyze(self.call_id, self.transcript)
    
    @property
    def duration_seconds(self) -> int:
        return (datetime.now() - self.started_at).seconds
Archivo: engine/tactic_engine.py
Python

"""
Motor de tácticas de retención.
Decide qué táctica usar en cada momento 
para maximizar el tiempo en línea.
"""

import random
import time
from typing import Optional

class TacticEngine:
    """
    Analiza el estado de la conversación y selecciona
    la táctica óptima para mantener al spammer 
    al teléfono.
    """
    
    def __init__(self, persona: dict):
        self.persona = persona
        self.tactics_available = persona.get('tactics', [])
        self.tactics_history = []
        self.last_tactic_turn = 0
        self.consecutive_same_tactic = 0
        
        # Palabras clave que activan tácticas específicas
        self.triggers = {
            'datos_bancarios': [
                'cuenta', 'iban', 'número de cuenta',
                'banco', 'tarjeta', 'pago'
            ],
            'urgencia': [
                'ahora mismo', 'hoy', 'urgente', 
                'último día', 'caduca', 'inmediatamente',
                'corte', 'suspensión'
            ],
            'datos_personales': [
                'dni', 'nombre completo', 'dirección',
                'titular', 'fecha de nacimiento'
            ],
            'impaciencia': [
                'escúcheme', 'atiéndame', 'por favor',
                'es importante', 'necesito que'
            ],
            'verificacion': [
                'confirme', 'verifique', 'dígame',
                'necesito que me diga'
            ]
        }
        
        # Efectividad histórica de cada táctica
        self.tactic_scores = {
            t: 0.5 for t in self.tactics_available
        }
    
    def select_tactic(
        self, 
        spammer_text: str,
        turn_number: int,
        full_transcript: list
    ) -> Optional[str]:
        """
        Selecciona la táctica más adecuada 
        para el momento actual.
        Returns: Instrucción de táctica para el LLM,
                 o None si no hay táctica específica.
        """
        
        # No usar táctica en cada turno (suena artificial)
        # Usar cada 2-4 turnos
        turns_since_last = turn_number - self.last_tactic_turn
        if turns_since_last < random.randint(2, 4):
            return None
        
        spammer_lower = spammer_text.lower()
        
        # REGLA 1: Si piden datos bancarios → Táctica CARTILLA
        if any(kw in spammer_lower 
               for kw in self.triggers['datos_bancarios']):
            if 'CARTILLA' in self.tactics_available:
                return self._use_tactic('CARTILLA', turn_number,
                    "Dile que vas a buscar la libreta del banco, "
                    "que la tienes en el cajón de la mesilla. "
                    "Pídele que espere. Haz una pausa larga "
                    "(el sistema añadirá silencio). "
                    "Cuando vuelvas, di que no la encuentras "
                    "y que a ver si tu hijo la tiene.")
        
        # REGLA 2: Si hay urgencia → Táctica HIJO
        if any(kw in spammer_lower 
               for kw in self.triggers['urgencia']):
            if 'HIJO' in self.tactics_available:
                return self._use_tactic('HIJO', turn_number,
                    "Dile que estas cosas las decides con tu "
                    "hijo Miguel. Que hoy no puedes decidir "
                    "sola. Que le llames mañana. Sé muy "
                    "amable pero firme en que necesitas "
                    "consultar con tu hijo.")
        
        # REGLA 3: Si piden DNI → Táctica GAFAS
        if any(kw in spammer_lower 
               for kw in self.triggers['datos_personales']):
            if 'GAFAS' in self.tactics_available:
                return self._use_tactic('GAFAS', turn_number,
                    "Di que no ves bien sin las gafas y que "
                    "tienes que buscarlas. Pide que espere. "
                    "Cuando vuelvas (tras la pausa del sistema) "
                    "pregunta de qué estaban hablando.")
        
        # REGLA 4: Si hay impaciencia → Táctica SORDERA
        if any(kw in spammer_lower 
               for kw in self.triggers['impaciencia']):
            if 'SORDERA' in self.tactics_available:
                return self._use_tactic('SORDERA', turn_number,
                    "Dile que no le oyes bien, que hable más "
                    "alto. Hazle repetir lo que acaba de decir "
                    "2-3 veces. Parece que el teléfono va mal.")
        
        # REGLA 5: Cada 8 turnos → Anécdota aleatoria
        if turn_number % 8 == 0:
            if 'ANECDOTA' in self.tactics_available:
                anecdotas = [
                    ("ANECDOTA", 
                     "Interrumpe con una historia sobre el "
                     "precio del pan o el tiempo que hace. "
                     "Mínimo 3-4 frases. Sé muy detallista."),
                    ("VECINA",
                     "Di que alguien llama a la puerta, "
                     "que debe ser la vecina Remedios. "
                     "Pide que espere un momento."),
                    ("TELEVISION",
                     "Di que no oyes porque tienes la tele "
                     "puesta y que vas a bajarla. Cuenta qué "
                     "programa estabas viendo.")
                ]
                choice = random.choice(anecdotas)
                if choice[0] in self.tactics_available:
                    return self._use_tactic(
                        choice[0], turn_number, choice[1]
                    )
        
        # Sin táctica específica
        return None
    
    def _use_tactic(
        self, 
        tactic: str, 
        turn_number: int,
        instruction: str
    ) -> str:
        """Registra el uso de la táctica y devuelve instrucción"""
        self.tactics_history.append({
            'turn': turn_number,
            'tactic': tactic,
            'timestamp': time.time()
        })
        self.last_tactic_turn = turn_number
        return instruction
    
    def get_tactics_summary(self) -> dict:
        """Devuelve resumen de tácticas usadas"""
        from collections import Counter
        counts = Counter(
            t['tactic'] for t in self.tactics_history
        )
        return dict(counts)
9. SISTEMA DE PERSONAS Y PROMPTS
Archivo: engine/persona_manager.py
Python

"""
Gestiona la selección inteligente de personas/prompts.
Elige la persona óptima basándose en:
- Historial del número llamante
- Hora del día
- Tipo de estafa probable
- Efectividad histórica
"""

import asyncio
from database.connection import get_db

class PersonaManager:
    
    async def get_best_persona(
        self, 
        caller_number: str
    ) -> dict:
        """
        Selecciona la mejor persona para esta llamada.
        """
        
        async with get_db() as db:
            # Verificar si el número llamó antes
            previous_calls = await db.fetch("""
                SELECT scam_type, persona_name, 
                       retention_score
                FROM calls 
                WHERE caller_number = $1
                ORDER BY started_at DESC LIMIT 5
            """, caller_number)
            
            if previous_calls:
                # Llamó antes: usar persona diferente a la anterior
                last_persona = previous_calls[0]['persona_name']
                last_scam = previous_calls[0]['scam_type']
                
                persona = await db.fetchrow("""
                    SELECT * FROM personas 
                    WHERE is_active = TRUE
                    AND name != $1
                    ORDER BY 
                        CASE WHEN best_against_scam_type = $2 
                             THEN 0 ELSE 1 END,
                        avg_retention_score DESC
                    LIMIT 1
                """, last_persona, last_scam)
            else:
                # Primera vez: usar la persona con mejor 
                # retención general
                persona = await db.fetchrow("""
                    SELECT * FROM personas 
                    WHERE is_active = TRUE
                    ORDER BY 
                        CASE WHEN is_default THEN 0 ELSE 1 END,
                        avg_retention_score DESC
                    LIMIT 1
                """)
            
            return dict(persona)
    
    async def update_effectiveness(
        self,
        persona_id: str,
        duration_seconds: int,
        retention_score: float,
        scam_type: str
    ):
        """Actualiza las estadísticas de efectividad"""
        async with get_db() as db:
            await db.execute("""
                UPDATE personas SET
                    times_used = times_used + 1,
                    avg_duration_seconds = (
                        avg_duration_seconds * times_used + $2
                    ) / (times_used + 1),
                    avg_retention_score = (
                        avg_retention_score * times_used + $3
                    ) / (times_used + 1),
                    total_time_wasted_seconds = 
                        total_time_wasted_seconds + $2,
                    updated_at = NOW()
                WHERE id = $1
            """, persona_id, duration_seconds, retention_score)
10. ANALIZADOR POST-LLAMADA
Archivo: engine/post_call_analyzer.py
Python

"""
Análisis profundo de cada llamada terminada.
Usa IA para extraer inteligencia:
- Tipo de estafa
- Técnicas del spammer  
- Emociones en el tiempo
- Fingerprint del guión
- Asociación a campañas
"""

import json
import asyncio
import structlog
from groq import Groq
from database.connection import get_db
from geo_analyzer import GeoAnalyzer
from campaign_detector import CampaignDetector
from telegram_notifier import TelegramNotifier
import os

log = structlog.get_logger()

class PostCallAnalyzer:
    
    def __init__(self):
        self.llm = Groq(api_key=os.environ['GROQ_API_KEY'])
        self.geo = GeoAnalyzer()
        self.campaign_detector = CampaignDetector()
        self.notifier = TelegramNotifier()
        self.model_fast = "llama-3.1-8b-instant"
        self.model_smart = "llama-3.3-70b-versatile"
    
    async def analyze(self, call_id: str, transcript: list):
        """Pipeline completo de análisis post-llamada"""
        
        log.info("🔍 Iniciando análisis post-llamada",
                 call_id=call_id)
        
        # Marcar como procesando
        async with get_db() as db:
            await db.execute("""
                UPDATE calls SET analysis_status = 'processing'
                WHERE id = $1
            """, call_id)
        
        try:
            # Formatear transcripción
            full_text = self._format_transcript(transcript)
            spammer_only = self._spammer_text_only(transcript)
            
            # Análisis en paralelo donde es posible
            (scam_analysis, techniques, 
             emotions, fingerprint) = await asyncio.gather(
                self._classify_scam(full_text),
                self._detect_techniques(full_text),
                self._analyze_emotions(transcript),
                self._extract_fingerprint(spammer_only)
            )
            
            # Análisis que depende de los anteriores
            geo_data = await self.geo.analyze(call_id)
            campaign_id = await self.campaign_detector.match(
                fingerprint, scam_analysis, call_id
            )
            retention_analysis = await self._evaluate_retention(
                full_text, transcript
            )
            cost_analysis = await self._calculate_costs(
                transcript
            )
            
            # Guardar todo en DB
            async with get_db() as db:
                await db.execute("""
                    UPDATE calls SET
                        scam_type = $2,
                        scam_subtype = $3,
                        scam_confidence = $4,
                        company_impersonated = $5,
                        personal_data_requested = $6,
                        script_sophistication = $7,
                        transcript_summary = $8,
                        techniques_used = $9,
                        caller_emotion_timeline = $10,
                        caller_final_emotion = $11,
                        caller_patience_score = $12,
                        fingerprint = $13,
                        campaign_id = $14,
                        caller_country = $15,
                        caller_carrier = $16,
                        caller_is_voip = $17,
                        retention_score = $18,
                        why_hung_up = $19,
                        cost_total = $20,
                        analysis_status = 'completed',
                        analysis_completed_at = NOW()
                    WHERE id = $1
                """,
                    call_id,
                    scam_analysis.get('type'),
                    scam_analysis.get('subtype'),
                    scam_analysis.get('confidence'),
                    scam_analysis.get('company_impersonated'),
                    json.dumps(scam_analysis.get(
                        'personal_data_requested', []
                    )),
                    scam_analysis.get('sophistication'),
                    scam_analysis.get('summary'),
                    json.dumps(techniques),
                    json.dumps(emotions),
                    emotions[-1].get('emotion') 
                        if emotions else 'unknown',
                    emotions[-1].get('patience_level', 0.0) 
                        if emotions else 0.0,
                    fingerprint,
                    campaign_id,
                    geo_data.get('country'),
                    geo_data.get('carrier'),
                    geo_data.get('is_voip'),
                    retention_analysis.get('score'),
                    retention_analysis.get('reason'),
                    cost_analysis.get('total')
                )
            
            # Notificar por Telegram
            call_data = await self._get_call_data(call_id)
            await self.notifier.send_call_summary(
                call_data, scam_analysis, retention_analysis
            )
            
            log.info("✅ Análisis completado",
                     call_id=call_id,
                     scam_type=scam_analysis.get('type'))
        
        except Exception as e:
            log.error("❌ Error en análisis",
                      call_id=call_id, error=str(e))
            async with get_db() as db:
                await db.execute("""
                    UPDATE calls SET 
                        analysis_status = 'failed',
                        analysis_error = $2
                    WHERE id = $1
                """, call_id, str(e))
    
    async def _classify_scam(self, transcript: str) -> dict:
        response = self.llm.chat.completions.create(
            model=self.model_smart,
            messages=[{
                "role": "system",
                "content": """Eres un analista experto en 
fraude telefónico en España. Analiza la transcripción 
y devuelve JSON EXACTO:
{
  "type": "energia|banco|cripto|soporte_tecnico|
           inversion|loteria|seguridad_social|
           paqueteria|empleo|seguros|telco|otro",
  "subtype": "descripción específica del fraude",
  "company_impersonated": "empresa que suplantan o null",
  "confidence": 0.0-1.0,
  "summary": "2 frases explicando qué intentaban",
  "personal_data_requested": ["lista","de","datos"],
  "payment_methods_mentioned": ["bizum","transferencia"],
  "urgency_tactics": ["tácticas de urgencia usadas"],
  "sophistication": "bajo|medio|alto",
  "target_profile": "perfil de víctima que buscan",
  "estimated_origin": "país o región estimada del 
                       call center"
}"""
            }, {
                "role": "user",
                "content": transcript
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    async def _detect_techniques(self, transcript: str) -> list:
        response = self.llm.chat.completions.create(
            model=self.model_smart,
            messages=[{
                "role": "system",
                "content": """Analiza las técnicas de 
ingeniería social del SPAMMER. Devuelve JSON:
{
  "techniques": [
    {
      "name": "nombre de la técnica",
      "category": "urgencia|miedo|autoridad|
                   reciprocidad|escasez|familiaridad|
                   validacion_social|compromiso",
      "quote": "frase exacta donde la usa",
      "turn_approximate": número_de_turno,
      "worked": true/false/null
    }
  ],
  "overall_script_quality": "bajo|medio|alto",
  "training_level_estimate": "novato|intermedio|experto",
  "native_spanish": true/false,
  "reading_from_script": true/false,
  "total_pressure_attempts": número
}"""
            }, {
                "role": "user",
                "content": transcript
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    async def _analyze_emotions(self, turns: list) -> list:
        """Análisis de emociones del spammer por bloques"""
        
        spammer_turns = [
            t for t in turns if t['speaker'] == 'spammer'
        ]
        
        if not spammer_turns:
            return []
        
        # Dividir en bloques de 5 turnos
        chunk_size = 5
        chunks = [
            spammer_turns[i:i+chunk_size] 
            for i in range(0, len(spammer_turns), chunk_size)
        ]
        
        timeline = []
        for i, chunk in enumerate(chunks):
            text = " ".join([t['text'] for t in chunk])
            
            try:
                response = self.llm.chat.completions.create(
                    model=self.model_fast,
                    messages=[{
                        "role": "system",
                        "content": """Analiza emoción del 
hablante en este fragmento. JSON exacto:
{
  "emotion": "confiado|frustrado|enfadado|confuso|
              desesperado|agresivo|resignado|animado",
  "patience_level": 0.0-1.0,
  "suspects_bot": true/false,
  "stress_indicators": ["lista de indicadores"],
  "key_moment": "momento relevante o null"
}"""
                    }, {
                        "role": "user", 
                        "content": text
                    }],
                    response_format={"type": "json_object"}
                )
                
                result = json.loads(
                    response.choices[0].message.content
                )
                result['minute_approx'] = i * 2
                result['block'] = i
                timeline.append(result)
            
            except Exception:
                timeline.append({
                    'minute_approx': i * 2,
                    'emotion': 'unknown',
                    'patience_level': 0.5,
                    'suspects_bot': False
                })
        
        return timeline
    
    async def _extract_fingerprint(self, 
                                    spammer_text: str) -> str:
        """Extrae el guión estructural para clustering"""
        response = self.llm.chat.completions.create(
            model=self.model_smart,
            messages=[{
                "role": "system",
                "content": """Extrae el GUIÓN ESTRUCTURAL 
del estafador. Solo los PASOS que sigue él, 
ignorando las respuestas de la víctima.
Formato numerado, conciso:
1. [acción inicial]
2. [siguiente paso]
...

Sé muy específico sobre:
- Cómo se presenta
- Qué excusa/oferta usa
- Qué datos pide y en qué orden
- Cómo maneja objeciones
- Cómo cierra/presiona"""
            }, {
                "role": "user",
                "content": spammer_text
            }]
        )
        return response.choices[0].message.content
    
    async def _evaluate_retention(
        self, 
        transcript: str,
        turns: list
    ) -> dict:
        """Evalúa qué tan bien funcionó nuestra trampa"""
        
        duration = len([t for t in turns 
                        if t['speaker'] == 'spammer'])
        
        response = self.llm.chat.completions.create(
            model=self.model_fast,
            messages=[{
                "role": "system",
                "content": """Evalúa la efectividad 
del BOT para retener al spammer. JSON:
{
  "score": 0.0-1.0,
  "reason_hung_up": "por qué colgó el spammer",
  "best_moment": "el mejor momento de retención",
  "worst_moment": "cuándo estuvo a punto de colgar antes",
  "bot_detected": true/false,
  "detection_moment": "cuándo sospechó o null",
  "improvement_suggestions": ["lista de mejoras"]
}"""
            }, {
                "role": "user",
                "content": transcript
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    async def _calculate_costs(self, turns: list) -> dict:
        """Calcula el coste total de la llamada"""
        
        total_words = sum(
            len(t['text'].split()) for t in turns
        )
        total_tokens_approx = total_words * 1.3
        
        return {
            'stt': total_words * 0.0000059,
            'llm': total_tokens_approx * 0.00000059,
            'tts': len([t for t in turns 
                        if t['speaker'] == 'bot']) * 0.00001,
            'total': total_words * 0.000008
        }
    
    def _format_transcript(self, turns: list) -> str:
        return "\n".join([
            f"{'SPAMMER' if t['speaker'] == 'spammer' else 'BOT'}"
            f" [{t.get('timestamp', 0):.0f}s]: {t['text']}"
            for t in turns
        ])
    
    def _spammer_text_only(self, turns: list) -> str:
        return "\n".join([
            t['text'] for t in turns 
            if t['speaker'] == 'spammer'
        ])
    
    async def _get_call_data(self, call_id: str) -> dict:
        async with get_db() as db:
            row = await db.fetchrow(
                "SELECT * FROM calls WHERE id = $1", 
                call_id
            )
            return dict(row)
11. SISTEMA DE GEOLOCALIZACIÓN
Archivo: engine/geo_analyzer.py
Python

"""
Analiza la procedencia de los números llamantes.
Usa phonenumbers + APIs gratuitas de lookup.
"""

import phonenumbers
from phonenumbers import geocoder, carrier, number_type
import httpx
import asyncio
from database.connection import get_db

class GeoAnalyzer:
    
    async def analyze(self, call_id: str) -> dict:
        """Análisis completo de geolocalización"""
        
        async with get_db() as db:
            call = await db.fetchrow(
                "SELECT caller_number FROM calls WHERE id = $1",
                call_id
            )
        
        phone_str = call['caller_number']
        result = await self._analyze_number(phone_str)
        
        return result
    
    async def _analyze_number(self, phone_str: str) -> dict:
        """Analiza un número de teléfono"""
        
        try:
            # Parsear el número
            number = phonenumbers.parse(phone_str, "ES")
            
            # Datos básicos con phonenumbers (sin API)
            country = geocoder.description_for_number(
                number, "es"
            )
            carrier_name = carrier.name_for_number(
                number, "es"
            )
            line_type = self._get_line_type(
                phonenumbers.number_type(number)
            )
            is_valid = phonenumbers.is_valid_number(number)
            is_mobile = phonenumbers.number_type(
                number
            ) == phonenumbers.PhoneNumberType.MOBILE
            is_voip = phonenumbers.number_type(
                number
            ) == phonenumbers.PhoneNumberType.VOIP
            
            # Lookup adicional con API gratuita
            extra_data = await self._api_lookup(phone_str)
            
            return {
                'country': country or 'España',
                'carrier': carrier_name or 'Desconocido',
                'line_type': line_type,
                'is_valid': is_valid,
                'is_mobile': is_mobile,
                'is_voip': is_voip,
                'spam_score': extra_data.get('spam_score', 0),
                'reported_times': extra_data.get('reports', 0),
                'tags': extra_data.get('tags', [])
            }
        
        except Exception as e:
            return {
                'country': 'Desconocido',
                'carrier': 'Desconocido',
                'line_type': 'Desconocido',
                'is_valid': False,
                'is_mobile': False,
                'is_voip': False,
                'error': str(e)
            }
    
    async def _api_lookup(self, phone: str) -> dict:
        """
        Consulta APIs gratuitas para reputación del número.
        Usa numverify (plan free) o similar.
        """
        try:
            # API de SpamCalls (gratuita, sin key)
            clean_phone = phone.replace('+', '').replace(' ', '')
            
            async with httpx.AsyncClient(
                timeout=5.0
            ) as client:
                # Intentar con varios servicios
                response = await client.get(
                    f"https://api.shouldianswer.net/phone/"
                    f"{clean_phone}"
                )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'spam_score': data.get(
                            'spamScore', 0
                        ),
                        'reports': data.get(
                            'totalReports', 0
                        ),
                        'tags': data.get('tags', [])
                    }
        except Exception:
            pass
        
        return {'spam_score': 0, 'reports': 0, 'tags': []}
    
    def _get_line_type(self, number_type) -> str:
        types = {
            phonenumbers.PhoneNumberType.MOBILE: 'móvil',
            phonenumbers.PhoneNumberType.FIXED_LINE: 'fijo',
            phonenumbers.PhoneNumberType.VOIP: 'voip',
            phonenumbers.PhoneNumberType.TOLL_FREE: 
                'gratuito',
            phonenumbers.PhoneNumberType.PREMIUM_RATE: 
                'premium',
        }
        return types.get(number_type, 'desconocido')
12. MOTOR DE CLUSTERING E INTELIGENCIA
Archivo: engine/campaign_detector.py
Python

"""
Detecta si una llamada pertenece a una campaña existente.
Usa embeddings para comparar guiones.
Agrupa campañas en organizaciones.
"""

import json
import asyncio
from groq import Groq
from database.connection import get_db
import os

class CampaignDetector:
    
    def __init__(self):
        self.llm = Groq(api_key=os.environ['GROQ_API_KEY'])
        self.similarity_threshold = 0.75
    
    async def match(
        self, 
        fingerprint: str,
        scam_analysis: dict,
        call_id: str
    ) -> str:
        """
        Intenta asociar con campaña existente.
        Si no encuentra, crea una nueva.
        Returns: campaign_id
        """
        
        scam_type = scam_analysis.get('type', 'otro')
        
        # Buscar campañas del mismo tipo en los últimos 60 días
        async with get_db() as db:
            existing = await db.fetch("""
                SELECT id, script_pattern, name
                FROM campaigns
                WHERE scam_type = $1
                AND (last_seen > NOW() - INTERVAL '60 days'
                     OR is_active = TRUE)
                ORDER BY last_seen DESC
                LIMIT 10
            """, scam_type)
        
        if not existing:
            return await self._create_campaign(
                fingerprint, scam_analysis
            )
        
        # Comparar fingerprints con LLM
        existing_patterns = [
            {"id": str(r['id']), 
             "pattern": r['script_pattern'],
             "name": r['name']}
            for r in existing
        ]
        
        response = self.llm.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{
                "role": "system",
                "content": """Compara el guión NUEVO con 
los existentes. ¿Pertenece a la misma campaña 
(mismo script base, misma organización)?
Devuelve JSON:
{
  "match_found": true/false,
  "matched_campaign_id": "id o null",
  "similarity_score": 0.0-1.0,
  "reasoning": "explicación breve",
  "is_evolution": false
}
Sé estricto: solo es match si el guión base es MUY similar."""
            }, {
                "role": "user",
                "content": f"""GUIÓN NUEVO:
{fingerprint}

CAMPAÑAS EXISTENTES:
{json.dumps(existing_patterns, indent=2, 
            ensure_ascii=False)}"""
            }],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(
            response.choices[0].message.content
        )
        
        if (result.get('match_found') and 
            result.get('similarity_score', 0) >= 
            self.similarity_threshold):
            
            campaign_id = result['matched_campaign_id']
            await self._update_campaign(campaign_id, call_id)
            return campaign_id
        else:
            return await self._create_campaign(
                fingerprint, scam_analysis
            )
    
    async def _create_campaign(
        self, 
        fingerprint: str,
        scam_analysis: dict
    ) -> str:
        """Crea una nueva campaña"""
        
        async with get_db() as db:
            row = await db.fetchrow("""
                INSERT INTO campaigns (
                    name, scam_type, scam_subtype,
                    company_impersonated, script_pattern,
                    first_seen, last_seen,
                    total_calls, sophistication_level
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    NOW(), NOW(), 1, $6
                ) RETURNING id
            """,
                f"Campaña-{scam_analysis.get('type', 'otro')}"
                f"-{scam_analysis.get('company_impersonated', 'N/A')}",
                scam_analysis.get('type'),
                scam_analysis.get('subtype'),
                scam_analysis.get('company_impersonated'),
                fingerprint,
                scam_analysis.get('sophistication', 'medio')
            )
            return str(row['id'])
    
    async def _update_campaign(
        self, 
        campaign_id: str, 
        call_id: str
    ):
        """Actualiza estadísticas de campaña existente"""
        async with get_db() as db:
            await db.execute("""
                UPDATE campaigns SET
                    total_calls = total_calls + 1,
                    last_seen = NOW(),
                    is_active = TRUE
                WHERE id = $1
            """, campaign_id)
13. BOT DE TELEGRAM
Archivo: engine/telegram_notifier.py
Python

"""
Notificaciones en tiempo real vía Telegram.
Envía resúmenes de llamadas, alertas y reportes.
"""

import httpx
import os
import structlog
from datetime import datetime

log = structlog.get_logger()

class TelegramNotifier:
    
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        self.base_url = (
            f"https://api.telegram.org/bot{self.token}"
        )
        self.enabled = bool(
            self.token and self.chat_id and
            os.environ.get('TELEGRAM_NOTIFICATIONS') == 'true'
        )
    
    async def send_call_started(
        self, 
        caller_number: str, 
        persona_name: str
    ):
        """Notifica inicio de llamada"""
        if not self.enabled:
            return
        
        msg = (
            f"📞 *Nueva llamada atrapada*\n\n"
            f"🔴 En vivo ahora\n"
            f"📱 Número: `{caller_number}`\n"
            f"🎭 Persona: {persona_name}\n"
            f"⏱️ Inicio: {datetime.now().strftime('%H:%M:%S')}"
        )
        
        await self._send(msg)
    
    async def send_call_summary(
        self, 
        call_data: dict,
        scam_analysis: dict,
        retention: dict
    ):
        """Envía resumen completo al terminar"""
        if not self.enabled:
            return
        
        duration_s = call_data.get('duration_seconds', 0)
        duration_str = (
            f"{duration_s // 3600}h "
            f"{(duration_s % 3600) // 60}m "
            f"{duration_s % 60}s"
        ) if duration_s > 3600 else (
            f"{duration_s // 60}m {duration_s % 60}s"
        )
        
        scam_emoji = {
            'energia': '⚡',
            'banco': '🏦',
            'cripto': '₿',
            'soporte_tecnico': '💻',
            'inversion': '📈',
            'loteria': '🎰',
            'empleo': '💼'
        }.get(scam_analysis.get('type', ''), '🦠')
        
        retention_bar = self._make_bar(
            retention.get('score', 0)
        )
        
        msg = (
            f"🕷️ *SPAMMER ELIMINADO*\n\n"
            f"📱 `{call_data.get('caller_number')}`\n"
            f"⏱️ Tiempo robado: *{duration_str}*\n"
            f"🎭 Persona: {call_data.get('persona_name')}\n\n"
            f"{scam_emoji} *Tipo:* "
            f"{scam_analysis.get('type', 'desconocido')}\n"
            f"🏢 *Empresa falsa:* "
            f"{scam_analysis.get('company_impersonated', 'N/A')}\n"
            f"📊 *Retención:* {retention_bar} "
            f"{retention.get('score', 0):.0%}\n"
            f"💀 *Colgó porque:* "
            f"{retention.get('reason_hung_up', '?')}\n\n"
            f"💰 *Coste:* "
            f"{call_data.get('cost_total', 0):.4f}€\n\n"
            f"📝 _{scam_analysis.get('summary', '')}_"
        )
        
        # Botones inline
        keyboard = {
            "inline_keyboard": [[
                {
                    "text": "📄 Ver Transcripción",
                    "callback_data": 
                        f"transcript_{call_data.get('id')}"
                },
                {
                    "text": "🚫 Blacklist",
                    "callback_data": 
                        f"blacklist_{call_data.get('caller_number')}"
                }
            ]]
        }
        
        await self._send(msg, reply_markup=keyboard)
    
    async def send_daily_report(self, stats: dict):
        """Reporte diario de estadísticas"""
        if not self.enabled:
            return
        
        msg = (
            f"📊 *REPORTE DIARIO - ScamEater*\n"
            f"_{datetime.now().strftime('%d/%m/%Y')}_\n\n"
            f"📞 Llamadas: {stats.get('total_calls', 0)}\n"
            f"⏱️ Tiempo robado: "
            f"{stats.get('total_hours', 0):.1f}h\n"
            f"💰 Coste total: "
            f"{stats.get('total_cost', 0):.2f}€\n"
            f"🏆 Más larga: "
            f"{stats.get('longest_call', 'N/A')}\n\n"
            f"🦠 *Por tipo:*\n"
        )
        
        for scam_type, count in stats.get(
            'by_type', {}
        ).items():
            msg += f"  • {scam_type}: {count}\n"
        
        await self._send(msg)
    
    def _make_bar(self, score: float) -> str:
        """Crea una barra de progreso visual"""
        filled = int(score * 10)
        return '█' * filled + '░' * (10 - filled)
    
    async def _send(
        self, 
        text: str, 
        reply_markup: dict = None
    ):
        """Envía mensaje a Telegram"""
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            if reply_markup:
                import json
                payload["reply_markup"] = json.dumps(
                    reply_markup
                )
            
            async with httpx.AsyncClient(
                timeout=10.0
            ) as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json=payload
                )
                if response.status_code != 200:
                    log.warning(
                        "Telegram error",
                        status=response.status_code,
                        body=response.text[:200]
                    )
        except Exception as e:
            log.error("Error Telegram", error=str(e))
14. PANEL DE CONTROL - DASHBOARD
Archivo: dashboard/Dockerfile
Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    streamlit==1.35.0 \
    plotly==5.22.0 \
    pandas==2.2.2 \
    asyncpg==0.29.0 \
    psycopg2-binary==2.9.9 \
    redis==5.0.4 \
    minio==7.2.7 \
    httpx==0.27.0 \
    phonenumbers==8.13.37

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
Archivo: dashboard/.streamlit/config.toml
toml

[theme]
primaryColor = "#FF4444"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1E2329"
textColor = "#FAFAFA"
font = "monospace"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
Archivo: dashboard/app.py
Python

"""
SCAMEATER Dashboard - Punto de entrada principal
"""

import streamlit as st

st.set_page_config(
    page_title="🕷️ SCAMEATER",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "SCAMEATER - Sistema Honeypot Anti-Spam VoIP"
    }
)

# Importar conexión
import psycopg2
import os
from datetime import datetime

@st.cache_resource
def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def get_global_stats(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                COUNT(*) as total_calls,
                COALESCE(SUM(duration_seconds), 0) 
                    as total_seconds,
                COALESCE(AVG(duration_seconds), 0) 
                    as avg_seconds,
                COALESCE(SUM(cost_total), 0) as total_cost,
                COUNT(DISTINCT caller_number) 
                    as unique_numbers,
                MAX(duration_seconds) as longest_call
            FROM calls
            WHERE started_at >= NOW() - INTERVAL '30 days'
        """)
        return cur.fetchone()

# Sidebar con KPIs rápidos
conn = get_db_connection()

with st.sidebar:
    st.title("🕷️ SCAMEATER")
    st.caption("Centro de Inteligencia Anti-Scam")
    st.divider()
    
    try:
        stats = get_global_stats(conn)
        total_calls = stats[0]
        total_hours = (stats[1] or 0) / 3600
        total_cost = stats[4] or 0
        
        st.metric("📞 Llamadas (30d)", total_calls)
        st.metric("⏱️ Horas robadas", f"{total_hours:.1f}h")
        st.metric("💰 Coste total", f"{total_cost:.2f}€")
        
        if total_calls > 0:
            roi = (total_hours * 30) / max(total_cost, 0.01)
            st.metric("📈 ROI (h/€)", f"{roi:.0f}x")
    except Exception:
        st.error("Error conectando a DB")
    
    st.divider()
    st.caption(
        f"🕐 {datetime.now().strftime('%H:%M:%S')}"
    )

# Página principal con overview
st.title("🕷️ SCAMEATER - Centro de Inteligencia")
st.caption("Sistema Honeypot Conversacional Anti-Spam VoIP")

col1, col2, col3 = st.columns(3)
with col1:
    st.info(
        "📞 **En Vivo**: Llamadas activas en tiempo real\n\n"
        "👈 Navega usando el menú lateral"
    )
with col2:
    st.info(
        "💀 **Morgue**: Historial completo con análisis\n\n"
        "🔊 Escucha audios y lee transcripciones"
    )
with col3:
    st.info(
        "🧠 **Inteligencia**: Patrones y campañas\n\n"
        "🗺️ Mapas, redes y tendencias"
    )
Archivo: dashboard/pages/01_en_vivo.py
Python

"""
Página: Llamadas en Vivo
Muestra las llamadas activas con transcripción en tiempo real
"""

import streamlit as st
import psycopg2
import os
import time
import json
from datetime import datetime

st.title("🔴 Llamadas en la Trampa")

def get_active_calls(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                c.id, c.caller_number, c.started_at,
                c.persona_name, c.llm_model,
                EXTRACT(EPOCH FROM 
                    (NOW() - c.started_at))::INTEGER 
                    as seconds_active,
                c.transcript_full
            FROM calls c
            WHERE c.ended_at IS NULL
            ORDER BY c.started_at DESC
        """)
        return cur.fetchall()

@st.cache_resource
def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'])

conn = get_conn()

# Auto-refresh cada 5 segundos
placeholder = st.empty()

# Métricas globales en tiempo real
col1, col2, col3, col4 = st.columns(4)

with conn.cursor() as cur:
    cur.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE ended_at IS NULL),
            COUNT(*) FILTER (
                WHERE started_at >= CURRENT_DATE
            ),
            COALESCE(SUM(duration_seconds) FILTER (
                WHERE started_at >= CURRENT_DATE
            ), 0),
            COALESCE(SUM(cost_total) FILTER (
                WHERE started_at >= CURRENT_DATE
            ), 0)
        FROM calls
    """)
    row = cur.fetchone()

with col1:
    st.metric("🔴 Activas Ahora", row[0])
with col2:
    st.metric("📞 Llamadas Hoy", row[1])
with col3:
    st.metric("⏱️ Min. Robados Hoy", 
              f"{(row[2] or 0) // 60}m")
with col4:
    st.metric("💰 Coste Hoy", f"{row[3] or 0:.3f}€")

st.divider()

# Lista de llamadas activas
active_calls = get_active_calls(conn)

if not active_calls:
    st.info(
        "🕐 No hay llamadas activas en este momento.\n\n"
        "El sistema está esperando llamadas entrantes..."
    )
else:
    for call in active_calls:
        call_id = call[0]
        caller = call[1]
        started = call[2]
        persona = call[4]
        seconds = call[6]
        transcript_json = call[7]
        
        minutes = seconds // 60
        secs = seconds % 60
        
        with st.expander(
            f"📞 {caller} | "
            f"🎭 {persona} | "
            f"⏱️ {minutes}m {secs}s", 
            expanded=True
        ):
            col_left, col_right = st.columns([3, 1])
            
            with col_right:
                st.metric("⏱️ Tiempo", f"{minutes}m {secs}s")
                st.metric("🎭 Persona", persona)
                
                # Barra de "paciencia estimada"
                # (baja con el tiempo)
                patience = max(0, 1 - (minutes / 30))
                st.progress(patience, 
                           text=f"😤 Paciencia: {patience:.0%}")
            
            with col_left:
                # Transcripción en tiempo real
                st.markdown("**Transcripción:**")
                
                if transcript_json:
                    try:
                        turns = json.loads(transcript_json)
                        # Mostrar últimos 10 turnos
                        transcript_html = ""
                        for turn in turns[-10:]:
                            speaker = turn.get('speaker', '')
                            text = turn.get('text', '')
                            if speaker == 'spammer':
                                transcript_html += (
                                    f"🔴 **Spammer:** {text}\n\n"
                                )
                            else:
                                transcript_html += (
                                    f"🤖 **Bot:** {text}\n\n"
                                )
                        st.markdown(transcript_html)
                    except Exception:
                        st.info("Cargando transcripción...")
                else:
                    st.info("Esperando primera respuesta...")

# Auto-refresh
st.caption("⟳ Actualización automática cada 10 segundos")
time.sleep(10)
st.rerun()
Archivo: dashboard/pages/02_morgue.py
Python

"""
Página: Morgue de Spammers
Historial completo con todas las llamadas analizadas
"""

import streamlit as st
import psycopg2
import pandas as pd
import os
import json
from datetime import datetime, timedelta

st.title("💀 Morgue de Spammers")

@st.cache_resource
def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'])

conn = get_conn()

# =================== FILTROS ===================
with st.expander("🔍 Filtros", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        days = st.selectbox(
            "Período", 
            [7, 14, 30, 90, 365, 0],
            format_func=lambda x: 
                f"Últimos {x} días" if x > 0 else "Todo"
        )
    with col2:
        scam_filter = st.multiselect(
            "Tipo de Estafa",
            ["energia", "banco", "cripto", 
             "soporte_tecnico", "inversion", 
             "loteria", "empleo", "otro"]
        )
    with col3:
        min_min = st.number_input(
            "Duración mínima (min)", 0, 120, 0
        )
    with col4:
        persona_filter = st.multiselect(
            "Persona usada",
            ["dona_concha", "don_jose", "maria_interesada"]
        )

# =================== QUERY ===================
where_clauses = ["ended_at IS NOT NULL"]
params = []
param_count = 0

if days > 0:
    param_count += 1
    where_clauses.append(
        f"started_at >= NOW() - INTERVAL '{days} days'"
    )

if scam_filter:
    param_count += 1
    placeholders = ','.join(
        [f'%s'] * len(scam_filter)
    )
    where_clauses.append(
        f"scam_type IN ({placeholders})"
    )
    params.extend(scam_filter)

if min_min > 0:
    param_count += 1
    where_clauses.append(
        f"duration_seconds >= {min_min * 60}"
    )

if persona_filter:
    placeholders = ','.join(['%s'] * len(persona_filter))
    where_clauses.append(
        f"persona_name IN ({placeholders})"
    )
    params.extend(persona_filter)

where_sql = " AND ".join(where_clauses)

with conn.cursor() as cur:
    cur.execute(f"""
        SELECT 
            id, caller_number, started_at,
            duration_seconds, scam_type,
            company_impersonated, persona_name,
            retention_score, why_hung_up,
            cost_total, caller_country,
            caller_carrier, caller_is_voip,
            hang_up_by, analysis_status,
            script_sophistication
        FROM calls
        WHERE {where_sql}
        ORDER BY started_at DESC
        LIMIT 500
    """, params)
    
    columns = [
        'ID', 'Número', 'Fecha', 'Duración(s)', 
        'Tipo', 'Empresa Falsa', 'Persona',
        'Retención', 'Por qué colgó', 'Coste€',
        'País', 'Operador', 'VoIP', 'Quién colgó',
        'Análisis', 'Sofisticación'
    ]
    rows = cur.fetchall()

if not rows:
    st.info("No hay llamadas con los filtros seleccionados")
    st.stop()

df = pd.DataFrame(rows, columns=columns)

# Formatear duración
df['Duración'] = df['Duración(s)'].apply(
    lambda x: f"{x//60}m {x%60}s" if x else "N/A"
)
df['Retención'] = df['Retención'].apply(
    lambda x: f"{x:.0%}" if x else "N/A"
)
df['Coste€'] = df['Coste€'].apply(
    lambda x: f"{x:.4f}€" if x else "N/A"
)

# Resumen rápido
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📞 Total llamadas", len(df))
with col2:
    total_min = df['Duración(s)'].sum() / 60
    st.metric("⏱️ Total minutos", f"{total_min:.0f}m")
with col3:
    avg_min = df['Duración(s)'].mean() / 60
    st.metric("📊 Media", f"{avg_min:.1f}m")
with col4:
    total_cost = sum(
        float(c.replace('€','')) 
        for c in df['Coste€'] if c != 'N/A'
    )
    st.metric("💰 Coste total", f"{total_cost:.2f}€")

st.divider()

# Tabla principal
st.subheader("📋 Lista de Llamadas")

display_cols = [
    'Número', 'Fecha', 'Duración', 'Tipo', 
    'Empresa Falsa', 'Persona', 'Retención', 'Coste€',
    'País', 'Sofisticación'
]

event = st.dataframe(
    df[display_cols],
    use_container_width=True,
    selection_mode='single-row',
    on_select='rerun'
)

# =================== DETALLE ===================
if event.selection.rows:
    selected_idx = event.selection.rows[0]
    selected_row = df.iloc[selected_idx]
    call_id = selected_row['ID']
    
    st.divider()
    st.subheader(
        f"📋 Detalle: {selected_row['Número']} | "
        f"{selected_row['Duración']}"
    )
    
    # Tabs de detalle
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Transcripción",
        "🔊 Audio",
        "🧠 Análisis IA",
        "😤 Emociones",
        "🎯 Técnicas",
        "🌍 Geolocalización"
    ])
    
    # Cargar datos completos de la llamada
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM calls WHERE id = %s
        """, (str(call_id),))
        call_full = cur.fetchone()
        call_cols = [d[0] for d in cur.description]
        call_data = dict(zip(call_cols, call_full))
    
    with tab1:
        st.markdown("### 📝 Transcripción Completa")
        
        transcript = json.loads(
            call_data.get('transcript_full', '[]') or '[]'
        )
        
        for turn in transcript:
            if turn.get('speaker') == 'spammer':
                st.markdown(
                    f"🔴 **[{turn.get('timestamp',0):.0f}s] "
                    f"Spammer:** {turn.get('text','')}"
                )
            else:
                st.markdown(
                    f"🤖 **[{turn.get('timestamp',0):.0f}s] "
                    f"Bot:** {turn.get('text','')}"
                )
        
        st.download_button(
            "📥 Descargar Transcripción (JSON)",
            call_data.get('transcript_full', '[]'),
            f"transcript_{call_id}.json"
        )
        
        # Resumen generado por IA
        if call_data.get('transcript_summary'):
            st.info(
                f"**📝 Resumen IA:** "
                f"{call_data['transcript_summary']}"
            )
    
    with tab2:
        if call_data.get('audio_path'):
            st.markdown("### 🔊 Grabación de la Llamada")
            st.info(
                f"Audio guardado en: {call_data['audio_path']}"
            )
            # TODO: Integrar reproductor con MinIO
            st.button("▶️ Reproducir (próximamente)")
        else:
            st.warning("Audio no disponible para esta llamada")
    
    with tab3:
        st.markdown("### 🧠 Análisis de Inteligencia")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
**Tipo de Estafa:** {call_data.get('scam_type', 'N/A')}
**Subtipo:** {call_data.get('scam_subtype', 'N/A')}
**Empresa Suplantada:** 
{call_data.get('company_impersonated', 'N/A')}
**Sofisticación:** 
{call_data.get('script_sophistication', 'N/A')}
**Confianza:** 
{(call_data.get('scam_confidence') or 0):.0%}
""")
            
            data_requested = json.loads(
                call_data.get(
                    'personal_data_requested', '[]'
                ) or '[]'
            )
            if data_requested:
                st.markdown(
                    "**Datos que pedían:** " + 
                    ", ".join(data_requested)
                )
        
        with col_b:
            st.markdown(
                f"**Resumen:** "
                f"{call_data.get('transcript_summary', 'N/A')}"
            )
            
            if call_data.get('campaign_id'):
                st.success(
                    f"🕸️ Campaña asociada: "
                    f"{call_data['campaign_id']}"
                )
    
    with tab4:
        st.markdown("### 😤 Timeline Emocional del Spammer")
        
        emotions = json.loads(
            call_data.get('caller_emotion_timeline', '[]') 
            or '[]'
        )
        
        if emotions:
            import plotly.graph_objects as go
            
            minutes = [e.get('minute_approx', 0) 
                      for e in emotions]
            patience = [e.get('patience_level', 0.5) 
                       for e in emotions]
            
            emotion_labels = [
                e.get('emotion', 'unknown') 
                for e in emotions
            ]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=minutes, y=patience,
                mode='lines+markers',
                name='Paciencia',
                line=dict(color='red', width=3),
                text=emotion_labels,
                hovertemplate=(
                    'Min %{x}: %{text}<br>'
                    'Paciencia: %{y:.0%}'
                )
            ))
            
            fig.update_layout(
                title='Paciencia del Spammer en el tiempo',
                xaxis_title='Minuto de llamada',
                yaxis_title='Nivel de paciencia',
                yaxis=dict(tickformat='.0%'),
                template='plotly_dark'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de emociones
            emotion_df = pd.DataFrame(emotions)
            st.dataframe(emotion_df, use_container_width=True)
        else:
            st.info("Análisis de emociones no disponible")
    
    with tab5:
        st.markdown("### 🎯 Técnicas de Manipulación")
        
        techniques = json.loads(
            call_data.get('techniques_used', '{}') or '{}'
        )
        
        if isinstance(techniques, dict):
            tech_list = techniques.get('techniques', [])
        else:
            tech_list = techniques
        
        if tech_list:
            tech_df = pd.DataFrame(tech_list)
            st.dataframe(tech_df, use_container_width=True)
        else:
            st.info("No hay técnicas analizadas aún")
    
    with tab6:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
**País:** {call_data.get('caller_country', 'N/A')}
**Operador:** {call_data.get('caller_carrier', 'N/A')}
**Tipo de línea:** 
{call_data.get('caller_line_type', 'N/A')}
**Es VoIP:** 
{'✅ Sí' if call_data.get('caller_is_voip') else '❌ No'}
""")
Archivo: dashboard/pages/03_inteligencia.py
Python

"""
Página: Centro de Inteligencia
Análisis profundo de campañas, patrones y organizaciones
"""

import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json

st.title("🧠 Centro de Inteligencia")

@st.cache_resource
def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'])

conn = get_conn()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Mapa de Origen",
    "🕸️ Campañas Activas",
    "📈 Tendencias",
    "🔍 Patrones",
    "🏢 Organizaciones"
])

with tab1:
    st.subheader("🗺️ Origen Geográfico")
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                caller_country,
                COUNT(*) as calls,
                SUM(duration_seconds) as total_seconds,
                AVG(duration_seconds) as avg_seconds
            FROM calls
            WHERE caller_country IS NOT NULL
            GROUP BY caller_country
            ORDER BY calls DESC
        """)
        geo_data = cur.fetchall()
    
    if geo_data:
        geo_df = pd.DataFrame(geo_data, columns=[
            'País', 'Llamadas', 'Seg. Total', 'Seg. Media'
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                geo_df, x='País', y='Llamadas',
                title="Llamadas por País de Origen",
                template='plotly_dark',
                color='Llamadas',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(geo_df, use_container_width=True)
    
    # Análisis de VoIP vs Real
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                caller_is_voip,
                caller_line_type,
                COUNT(*) as calls
            FROM calls
            WHERE caller_line_type IS NOT NULL
            GROUP BY caller_is_voip, caller_line_type
        """)
        line_data = cur.fetchall()
    
    if line_data:
        line_df = pd.DataFrame(line_data, columns=[
            'Es VoIP', 'Tipo', 'Llamadas'
        ])
        
        fig = px.pie(
            line_df, values='Llamadas', names='Tipo',
            title="Distribución por Tipo de Línea",
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🕸️ Campañas Detectadas")
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                c.id, c.name, c.scam_type,
                c.company_impersonated,
                c.total_calls,
                c.total_time_wasted_seconds,
                c.first_seen, c.last_seen,
                c.sophistication_level,
                c.is_active,
                COUNT(DISTINCT calls.caller_number) 
                    as unique_numbers
            FROM campaigns c
            LEFT JOIN calls ON calls.campaign_id = c.id
            GROUP BY c.id
            ORDER BY c.last_seen DESC
        """)
        campaigns = cur.fetchall()
    
    if campaigns:
        camp_df = pd.DataFrame(campaigns, columns=[
            'ID', 'Nombre', 'Tipo', 'Empresa Falsa',
            'Total Llamadas', 'Segundos', 
            'Primera vez', 'Última vez',
            'Sofisticación', 'Activa', 'Números únicos'
        ])
        
        camp_df['Tiempo robado'] = camp_df['Segundos'].apply(
            lambda x: f"{(x or 0)//3600}h "
                      f"{((x or 0)%3600)//60}m"
        )
        camp_df['Activa'] = camp_df['Activa'].apply(
            lambda x: '✅' if x else '❌'
        )
        
        st.dataframe(
            camp_df[[
                'Nombre', 'Tipo', 'Empresa Falsa',
                'Total Llamadas', 'Tiempo robado',
                'Números únicos', 'Sofisticación',
                'Última vez', 'Activa'
            ]],
            use_container_width=True
        )
        
        # Gráfico de campañas por volumen
        fig = px.bar(
            camp_df.nlargest(10, 'Total Llamadas'),
            x='Nombre', y='Total Llamadas',
            color='Tipo',
            title="Top 10 Campañas por Volumen",
            template='plotly_dark'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📈 Tendencias de Fraude en España")
    
    period = st.selectbox(
        "Período",
        ["Últimos 7 días", "Últimos 30 días", 
         "Últimos 90 días"],
        key="trend_period"
    )
    
    days_map = {
        "Últimos 7 días": 7,
        "Últimos 30 días": 30,
        "Últimos 90 días": 90
    }
    days = days_map[period]
    
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT 
                DATE(started_at) as fecha,
                scam_type,
                COUNT(*) as llamadas,
                SUM(duration_seconds) as segundos
            FROM calls
            WHERE started_at >= NOW() - INTERVAL '{days} days'
            AND scam_type IS NOT NULL
            GROUP BY DATE(started_at), scam_type
            ORDER BY fecha
        """)
        trend_data = cur.fetchall()
    
    if trend_data:
        trend_df = pd.DataFrame(trend_data, columns=[
            'Fecha', 'Tipo', 'Llamadas', 'Segundos'
        ])
        
        fig = px.area(
            trend_df, x='Fecha', y='Llamadas',
            color='Tipo',
            title=f"Evolución por Tipo ({period})",
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap por hora
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT 
                    EXTRACT(DOW FROM started_at) as dia,
                    EXTRACT(HOUR FROM started_at) as hora,
                    COUNT(*) as llamadas
                FROM calls
                WHERE started_at >= 
                    NOW() - INTERVAL '{days} days'
                GROUP BY dia, hora
                ORDER BY dia, hora
            """)
            heatmap_data = cur.fetchall()
        
        if heatmap_data:
            heat_df = pd.DataFrame(heatmap_data, 
                                   columns=['Día', 'Hora', 
                                           'Llamadas'])
            
            fig = px.density_heatmap(
                heat_df, x='Hora', y='Día',
                z='Llamadas',
                title="Heatmap: Cuándo llaman más",
                template='plotly_dark',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("🔍 Análisis de Patrones")
    
    # Efectividad de tácticas del bot
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 