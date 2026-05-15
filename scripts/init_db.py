"""
SCAMEATER Database Initialization Script
Creates PostgreSQL schema using asyncpg
"""

import asyncio
import os
import sys

import asyncpg

SCHEMA_SQL = """
-- Extensión para vectores
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TABLA: personas
CREATE TABLE IF NOT EXISTS personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(200),
    description TEXT,
    system_prompt TEXT NOT NULL,
    voice_id VARCHAR(200),
    tts_engine VARCHAR(50) DEFAULT 'cartesia',
    tactics JSONB DEFAULT '[]',
    silence_response_ms INTEGER DEFAULT 3000,
    max_silence_loops INTEGER DEFAULT 5,
    filler_phrases JSONB DEFAULT '[]',
    times_used INTEGER DEFAULT 0,
    avg_duration_seconds DECIMAL(10,2) DEFAULT 0,
    avg_retention_score DECIMAL(3,2) DEFAULT 0,
    best_against_scam_type VARCHAR(100),
    total_time_wasted_seconds BIGINT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: campaigns
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200),
    scam_type VARCHAR(100),
    scam_subtype VARCHAR(200),
    company_impersonated VARCHAR(200),
    script_pattern TEXT,
    script_embedding VECTOR(768),
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    total_calls INTEGER DEFAULT 0,
    total_time_wasted_seconds BIGINT DEFAULT 0,
    numbers_used JSONB DEFAULT '[]',
    sophistication_level VARCHAR(20),
    target_demographic VARCHAR(100),
    primary_language VARCHAR(20) DEFAULT 'es',
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: organizations
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200),
    country_origin VARCHAR(100),
    city_origin VARCHAR(100),
    estimated_size VARCHAR(50),
    threat_level VARCHAR(20) DEFAULT 'medium',
    total_campaigns INTEGER DEFAULT 0,
    total_calls INTEGER DEFAULT 0,
    total_time_wasted_seconds BIGINT DEFAULT 0,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: calls
CREATE TABLE IF NOT EXISTS calls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    caller_number VARCHAR(30) NOT NULL,
    our_number VARCHAR(30),
    asterisk_channel_id VARCHAR(200),
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    answered_at TIMESTAMP,
    ended_at TIMESTAMP,
    duration_seconds INTEGER GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (ended_at - answered_at))::INTEGER
    ) STORED,
    audio_path VARCHAR(500),
    audio_size_bytes BIGINT,
    audio_duration_seconds DECIMAL(10,2),
    transcript_full JSONB DEFAULT '[]',
    transcript_text TEXT,
    transcript_summary TEXT,
    persona_id UUID REFERENCES personas(id),
    persona_name VARCHAR(100),
    llm_model VARCHAR(100),
    tts_engine VARCHAR(50),
    stt_engine VARCHAR(50),
    cost_stt DECIMAL(10,6) DEFAULT 0,
    cost_llm DECIMAL(10,6) DEFAULT 0,
    cost_tts DECIMAL(10,6) DEFAULT 0,
    cost_telephony DECIMAL(10,6) DEFAULT 0,
    cost_total DECIMAL(10,6) DEFAULT 0,
    scam_type VARCHAR(100),
    scam_subtype VARCHAR(200),
    scam_confidence DECIMAL(3,2),
    company_impersonated VARCHAR(200),
    personal_data_requested JSONB DEFAULT '[]',
    script_sophistication VARCHAR(20),
    caller_country VARCHAR(100),
    caller_region VARCHAR(100),
    caller_city VARCHAR(100),
    caller_carrier VARCHAR(100),
    caller_line_type VARCHAR(50),
    caller_is_voip BOOLEAN,
    caller_language VARCHAR(10),
    caller_accent VARCHAR(50),
    caller_gender VARCHAR(20),
    caller_emotion_timeline JSONB DEFAULT '[]',
    caller_final_emotion VARCHAR(50),
    caller_patience_score DECIMAL(3,2),
    techniques_used JSONB DEFAULT '[]',
    pressure_tactics_count INTEGER DEFAULT 0,
    threats_made BOOLEAN DEFAULT FALSE,
    threat_content TEXT,
    hang_up_by VARCHAR(20),
    why_hung_up TEXT,
    retention_score DECIMAL(3,2),
    tactics_used_by_bot JSONB DEFAULT '[]',
    bot_detected_by_spammer BOOLEAN DEFAULT FALSE,
    fingerprint TEXT,
    fingerprint_embedding VECTOR(768),
    campaign_id UUID REFERENCES campaigns(id),
    organization_id UUID REFERENCES organizations(id),
    analysis_status VARCHAR(20) DEFAULT 'pending',
    analysis_completed_at TIMESTAMP,
    analysis_error TEXT,
    tags JSONB DEFAULT '[]',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: conversation_turns
CREATE TABLE IF NOT EXISTS conversation_turns (
    id SERIAL PRIMARY KEY,
    call_id UUID NOT NULL REFERENCES calls(id) ON DELETE CASCADE,
    turn_number INTEGER NOT NULL,
    speaker VARCHAR(10) NOT NULL,
    timestamp_seconds DECIMAL(10,3),
    duration_seconds DECIMAL(10,3),
    text TEXT NOT NULL,
    audio_segment_path VARCHAR(500),
    sentiment_score DECIMAL(3,2),
    emotion VARCHAR(50),
    intent VARCHAR(100),
    is_pressure_tactic BOOLEAN DEFAULT FALSE,
    is_threat BOOLEAN DEFAULT FALSE,
    is_personal_data_request BOOLEAN DEFAULT FALSE,
    data_type_requested VARCHAR(100),
    is_verification_attempt BOOLEAN DEFAULT FALSE,
    suspects_bot BOOLEAN DEFAULT FALSE,
    tactic_used VARCHAR(100),
    llm_latency_ms INTEGER,
    tts_latency_ms INTEGER,
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: blacklist
CREATE TABLE IF NOT EXISTS blacklist (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(30) UNIQUE NOT NULL,
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW(),
    times_called INTEGER DEFAULT 1,
    total_time_wasted_seconds INTEGER DEFAULT 0,
    scam_types JSONB DEFAULT '[]',
    campaigns_associated JSONB DEFAULT '[]',
    carrier VARCHAR(100),
    line_type VARCHAR(50),
    country VARCHAR(50),
    region VARCHAR(100),
    is_voip BOOLEAN DEFAULT FALSE,
    is_exported_android BOOLEAN DEFAULT FALSE,
    is_exported_ios BOOLEAN DEFAULT FALSE,
    is_reported_to_authorities BOOLEAN DEFAULT FALSE,
    confidence_score DECIMAL(3,2) DEFAULT 1.0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: api_usage
CREATE TABLE IF NOT EXISTS api_usage (
    id SERIAL PRIMARY KEY,
    call_id UUID REFERENCES calls(id),
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100),
    audio_seconds DECIMAL(10,3),
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_eur DECIMAL(10,6) DEFAULT 0,
    latency_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: system_config
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT,
    value_type VARCHAR(20) DEFAULT 'string',
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- TABLA: audit_log
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

-- Índices
CREATE INDEX IF NOT EXISTS idx_calls_caller_number ON calls(caller_number);
CREATE INDEX IF NOT EXISTS idx_calls_started_at ON calls(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_calls_scam_type ON calls(scam_type);
CREATE INDEX IF NOT EXISTS idx_calls_campaign_id ON calls(campaign_id);
CREATE INDEX IF NOT EXISTS idx_calls_analysis_status ON calls(analysis_status);
CREATE INDEX IF NOT EXISTS idx_turns_call_id ON conversation_turns(call_id);
CREATE INDEX IF NOT EXISTS idx_blacklist_number ON blacklist(phone_number);

-- Datos iniciales: default persona Carmen
INSERT INTO personas (name, display_name, description, system_prompt, voice_id, tactics, silence_response_ms, is_default) VALUES
('carmen', 'Carmen', 'Jubilada española de 78 años, prudente, no da datos, busca papeles',
'Eres Carmen, una jubilada española de 78 años. Vives sola en un pueblo de Guadalajara. Eres amable pero muy prudente.\n\nREGLAS ABSOLUTAS:\n1. NUNCA des tu DNI, IBAN, dirección real ni ningún dato personal.\n2. Si te piden datos, dices que los tiene tu hijo y que tienes que consultar con él.\n3. Siempre hablas muy despacio y a veces pides que repitan.\n4. Si alguien se enfada, dices que mejor llames a tu hijo.\n5. Nunca aceptes enlaces ni instrucciones para instalar nada.\n\nTÁCTICAS DE RETENCIÓN:\n- buscar_papeles: "Aguarde que tengo que buscar los papeles, están en el cajón..."\n- consulta_hijo: "Esto es mejor que lo hable con mi hijo, llame mañana"\n- problema_auditivo: "Hable más alto por favor, que oigo fatal"\n- duda_seguridad: "Antes tengo que preguntar en el banco si es de fiar"\n- peticion_identificacion: "Deme su número de empleado y el nombre de la empresa para llamar yo"\n- burocracia_ligera: "Necesito que me mande un escrito, no puedo decidir así"\n- cambio_tema_suave: "Y dígame, ¿hace mucho que trabaja ahí?"',
'["buscar_papeles","consulta_hijo","problema_auditivo","duda_seguridad","peticion_identificacion","burocracia_ligera","cambio_tema_suave"]',
4000, TRUE);
"""


async def init_database() -> None:
    """Initialize the SCAMEATER database with schema and default data."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable is not set", file=sys.stderr)
        sys.exit(1)

    conn = None
    try:
        print("Connecting to database...")
        conn = await asyncpg.connect(database_url)
        print("Connected. Creating schema...")

        await conn.execute(SCHEMA_SQL)
        print("Schema created successfully.")

        # Verify Carmen persona was inserted
        row = await conn.fetchrow(
            "SELECT id, name, is_default FROM personas WHERE name = 'carmen'"
        )
        if row:
            print(f"Default persona 'carmen' created with ID: {row['id']}")
        else:
            print("WARNING: Carmen persona not found after schema execution", file=sys.stderr)

        print("\nSCAMEATER database initialized successfully!")

    except asyncpg.PostgresSyntaxError as e:
        print(f"SQL Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except asyncpg.PostgresConnectionError as e:
        print(f"Database Connection Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if conn:
            await conn.close()
            print("Database connection closed.")


def main() -> None:
    """Entry point for the script."""
    asyncio.run(init_database())


if __name__ == "__main__":
    main()