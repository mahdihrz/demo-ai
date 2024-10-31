from io import BytesIO

import streamlit as st
from openai import OpenAI
import tempfile
from dotenv import load_dotenv
import os
import pathlib

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = openai_api_key)

st.title("Transcribe Audio")
st.write("Upload an audio file to transcribe it using Whisper API.")
audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

if st.button("Transcribe"):
    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=pathlib.Path(audio_file.name).suffix) as temp_audio:
            temp_audio.write(audio_file.getbuffer())
            temp_audio_path = temp_audio.name

        with st.spinner("Transcribing audio..."):
            try:
                with open(temp_audio_path, "rb") as audio:
                    vars(audio)
                    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio)

                st.success("Transcription completed!")
                st.write("Transcription:")
                st.write(transcript.text)

                if transcript.text:
                    transcription_data = BytesIO(transcript.text.encode("utf-8"))
                    st.download_button(
                        label="Download Transcription",
                        data=transcription_data,
                        file_name="audio_transcription.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Error transcribing audio: {e}")
    else:
        st.error("Please upload an audio file.")
