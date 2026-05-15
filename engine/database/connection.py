"""Database connection pool and utilities."""
import asyncpg
import os
from typing import Optional
import structlog

log = structlog.get_logger()

_pool: Optional[asyncpg.Pool] = None


async def init_db():
    """Initialize the database connection pool."""
    global _pool
    _pool = await asyncpg.create_pool(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 5432)),
        user=os.environ.get('DB_USER', 'scameater'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'scameater'),
        min_size=5,
        max_size=20,
    )
    log.info("Database pool initialized")


async def close_db():
    """Close the database connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        log.info("Database pool closed")


async def get_db():
    """Get a database connection from the pool."""
    if _pool is None:
        await init_db()
    return _pool.acquire()


async def release_db(conn):
    """Release a database connection back to the pool."""
    if _pool:
        await _pool.release(conn)


async def init_schema():
    """Initialize database schema (run once after first start)."""
    async with get_db() as conn:
        await conn.execute('''
            CREATE EXTENSION IF NOT EXISTS vector;
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

            CREATE TABLE IF NOT EXISTS calls (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                caller_number VARCHAR(30) NOT NULL,
                our_number VARCHAR(30),
                asterisk_channel_id VARCHAR(200),
                started_at TIMESTAMP NOT NULL DEFAULT NOW(),
                answered_at TIMESTAMP,
                ended_at TIMESTAMP,
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
                cost_total DECIMAL(10,6) DEFAULT 0,
                scam_type VARCHAR(100),
                scam_confidence DECIMAL(3,2),
                caller_country VARCHAR(100),
                caller_region VARCHAR(100),
                caller_city VARCHAR(100),
                caller_carrier VARCHAR(100),
                caller_line_type VARCHAR(50),
                analysis_status VARCHAR(20) DEFAULT 'pending',
                analysis_completed_at TIMESTAMP,
                analysis_error TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS conversation_turns (
                id SERIAL PRIMARY KEY,
                call_id UUID NOT NULL REFERENCES calls(id) ON DELETE CASCADE,
                turn_number INTEGER NOT NULL,
                speaker VARCHAR(10) NOT NULL,
                timestamp_seconds DECIMAL(10,3),
                text TEXT NOT NULL,
                audio_segment_path VARCHAR(500),
                sentiment_score DECIMAL(3,2),
                emotion VARCHAR(50),
                tactic_used VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            );

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

            CREATE INDEX IF NOT EXISTS idx_calls_caller_number ON calls(caller_number);
            CREATE INDEX IF NOT EXISTS idx_calls_started_at ON calls(started_at DESC);
            CREATE INDEX IF NOT EXISTS idx_turns_call_id ON conversation_turns(call_id);
        ''')
        log.info("Database schema initialized")