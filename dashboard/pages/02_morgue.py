"""Histórico - Call history."""
import streamlit as st
import httpx
from datetime import datetime, timedelta

st.title("📜 Histórico")
st.caption("Historial completo de llamadas")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    date_from = st.date_input("Desde", datetime.now() - timedelta(days=7))
with col2:
    date_to = st.date_input("Hasta", datetime.now())
with col3:
    scam_filter = st.selectbox("Tipo de scam", ["Todos", "Energía", "Telecomunicaciones", "Banca", "Inversión"])

st.markdown("---")

# Placeholder table
st.info("No hay llamadas registradas todavía. Las llamadas aparecerán aquí cuando se reciban.")

# In production, this would query the database and display:
# - Date/time
# - Caller (redacted)
# - Duration
# - Scam type
# - Confidence
# - Persona used
# - Actions (view details, play audio, etc.)