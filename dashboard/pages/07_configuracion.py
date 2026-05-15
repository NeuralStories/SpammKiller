"""Configuración - System configuration."""
import streamlit as st

st.title("⚙️ Configuración")
st.caption("Configuración del sistema")

st.subheader("Parámetros de llamada")

max_duration = st.slider(
    "Duración máxima de llamada (minutos)",
    min_value=10,
    max_value=120,
    value=90,
    step=10
)

silence_timeout = st.slider(
    "Timeout de silencio (segundos)",
    min_value=10,
    max_value=120,
    value=30,
    step=5
)

st.markdown("---")
st.subheader("Notificaciones Telegram")
telegram_enabled = st.checkbox("Activar notificaciones")
st.markdown("---")
st.subheader("Retención de datos")
st.text(f"Audios: 30 días | Transcripciones: 90 días | Metadatos: 2 años")