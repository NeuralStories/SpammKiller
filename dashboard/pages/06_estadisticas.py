"""Estadísticas - Global statistics and KPIs."""
import streamlit as st
import plotly.express as px

st.title("📊 Estadísticas")
st.caption("KPIs y métricas globales del sistema")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total llamadas", "0")
col2.metric("Tiempo total retenido", "0 min")
col3.metric("Coste total", "0.00€")
col4.metric("Spammers bloqueados", "0")

st.markdown("---")
st.subheader("Coste por día")
st.info("El gráfico de costes aparecerá aquí")

# In production:
# - Cost per day/week/month
# - Calls per day
# - Average call duration
# - Cost per scam type