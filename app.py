"""ASGI entrypoint for Vercel (and uvicorn)."""

from pathlib import Path

import streamlit as st

app = st.App(str(Path(__file__).with_name("streamlit_app.py")))

if __name__ == "__main__":
    app.run()
