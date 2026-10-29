import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_setting(name: str, default=None):
    """Read Streamlit Cloud secrets first, then local environment variables."""
    try:
        value = st.secrets.get(name)
        if value not in (None, ""):
            return value
    except Exception:
        pass
    return os.getenv(name, default)
