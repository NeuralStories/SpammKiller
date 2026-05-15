import os
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

@st.cache_resource
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        # Fallback to individual vars if URL not set
        user = os.environ.get("DB_USER", "scameater")
        password = os.environ.get("DB_PASSWORD", "change_me_in_production")
        host = os.environ.get("DB_HOST", "db")
        port = os.environ.get("DB_PORT", "5432")
        db_name = os.environ.get("DB_NAME", "scameater")
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    
    try:
        conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        conn.autocommit = True
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def fetch_data(query, params=None):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                return cur.fetchall()
            return []
    except Exception as e:
        st.error(f"Query error: {e}")
        return []
