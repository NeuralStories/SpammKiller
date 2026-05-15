"""En Vivo - Currently active calls."""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Agregamos la ruta del directorio padre para poder importar db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from db import fetch_data
except ImportError:
    st.error("Error cargando db.py")
    fetch_data = lambda q, p=None: []

st.title("📞 En Vivo")
st.caption("Llamadas activas en este momento")

# Fetch active calls (analysis_status = pending and ended_at IS NULL)
active_calls = fetch_data("""
    SELECT id, caller_number, started_at, persona_name, llm_model
    FROM calls 
    WHERE ended_at IS NULL
    ORDER BY started_at DESC
""")

if not active_calls:
    st.info("No hay llamadas activas en este momento")
else:
    for call in active_calls:
        duration = (datetime.now() - call['started_at']).total_seconds()
        
        with st.expander(f"Llamada: {call['caller_number']} ({int(duration)}s) - {call['persona_name']}", expanded=True):
            st.write(f"**ID:** {call['id']}")
            st.write(f"**Modelo LLM:** {call['llm_model']}")
            
            # Fetch latest transcript lines
            turns = fetch_data("""
                SELECT speaker, text, timestamp_seconds 
                FROM conversation_turns 
                WHERE call_id = %s 
                ORDER BY turn_number DESC LIMIT 5
            """, (call['id'],))
            
            st.subheader("Últimos mensajes:")
            if turns:
                for turn in reversed(turns):
                    role = "🤖" if turn['speaker'] == "agent" else "😈"
                    st.markdown(f"**{role} ({int(turn['timestamp_seconds'])}s):** {turn['text']}")
            else:
                st.write("*Conectando...*")
            
            if st.button("Cortar Llamada", key=f"hangup_{call['id']}"):
                st.warning("Función de colgado manual próximamente")

st.markdown("---")
st.subheader("Métricas en tiempo real")

# Metrics
total_active = len(active_calls)

# Total spammers
stats = fetch_data("SELECT COUNT(*) as total FROM calls WHERE ended_at IS NOT NULL")
total_spammers = stats[0]['total'] if stats else 0

# Cost (Mocked for now since table might not exist)
try:
    total_cost = fetch_data("SELECT SUM(cost_total) as cost FROM api_usage")
    cost = total_cost[0]['cost'] if total_cost and total_cost[0]['cost'] else 0.0
except Exception:
    cost = 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Llamadas activas", str(total_active))
col2.metric("Duración media", "0s") # Pending implementation
col3.metric("Coste actual", f"{cost:.2f}€")
col4.metric("Spammers procesados", str(total_spammers))