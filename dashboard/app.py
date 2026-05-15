"""SCAMEATER Dashboard - Main Streamlit application."""
import streamlit as st
import asyncio
from datetime import datetime, timedelta
import structlog

log = structlog.get_logger()

st.set_page_config(
    page_title="SCAMEATER - Panel de Control",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page navigation
PAGES = {
    "En Vivo": "pages/01_en_vivo.py",
    "Histórico": "pages/02_morgue.py",
    "Inteligencia": "pages/03_inteligencia.py",
    "Laboratorio": "pages/04_laboratorio.py",
    "Blacklist": "pages/05_blacklist.py",
    "Estadísticas": "pages/06_estadisticas.py",
    "Configuración": "pages/07_configuracion.py",
}


def main():
    """Main dashboard entry point."""
    st.title("🕷️ SCAMEATER")
    st.caption("Sistema Honeypot Conversacional Anti-Spam VoIP")

    # Sidebar navigation
    st.sidebar.title("Navegación")
    selection = st.sidebar.radio("Ir a", list(PAGES.keys()))

    # Status indicators
    st.sidebar.markdown("---")
    st.sidebar.subheader("Estado del Sistema")

    try:
        # Try to connect to API
        import httpx
        response = httpx.get("http://api:8000/health", timeout=2)
        if response.status_code == 200:
            st.sidebar.success("✅ Engine activo")
        else:
            st.sidebar.warning("⚠️ Engine con errores")
    except:
        st.sidebar.error("🔴 Engine desconectado")

    # Show selected page
    st.sidebar.markdown("---")
    st.sidebar.info(f"Páginas: {len(PAGES)}")

    # Display page
    st.info(f"Página seleccionada: **{selection}** (ir a la barra lateral)")


if __name__ == "__main__":
    main()