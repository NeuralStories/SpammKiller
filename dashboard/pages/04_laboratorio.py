"""Laboratorio - Prompts and models configuration."""
import streamlit as st

st.title("🔬 Laboratorio")
st.caption("Configuración de prompts y modelos")

st.subheader("Persona activa: Carmen")
st.text_area("Prompt del sistema",
    "Eres Carmen, una jubilada española de 78 años...",
    height=200,
    disabled=True)

st.markdown("---")
st.subheader("Modelos disponibles")

col1, col2, col3 = st.columns(3)
col1.metric("STT", "Deepgram Flux")
col2.metric("LLM", "Groq Llama-3.1-70B")
col3.metric("TTS", "Cartesia Sonic 3.5")