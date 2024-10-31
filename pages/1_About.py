import streamlit as st

st.title("About This Application")
st.write("""
This application provides three main features:
1. **About**: Overview of this application.
2. **Generate Article**: Generate articles based on a specified topic using OpenAI API and LangChain.
3. **Transcribe Audio**: Use OpenAI's Whisper API to transcribe audio files into text.
""")
