"""Blacklist - Phone number blacklist management."""
import streamlit as st
import httpx

st.title("🚫 Blacklist")
st.caption("Números confirmados como spammers")

st.info("La blacklist está vacía actualmente.")

# In production:
# - Table of blacklisted numbers
# - Export to Android/iOS buttons
# - Add manually / remove
# - Confidence score