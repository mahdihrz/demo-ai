from time import sleep

import streamlit as st
import requests
import tempfile
from dotenv import load_dotenv
import os
import pathlib


def make_request(url, headers, method="GET", data=None, files=None):
    if method == "POST":
        response = requests.post(url, headers=headers, json=data, files=files)
    else:
        response = requests.get(url, headers=headers)
    return response.json()

load_dotenv()
gladia_key = os.getenv("GLADIA_API_KEY")

headers = {
    "x-gladia-key": os.getenv("GLADIA_API_KEY", gladia_key),  # Replace with your Gladia Token
    "accept": "application/json",
}

st.title("Transcribe Audio using Gladia")
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
                    files = {
                        'audio': (temp_audio_path, audio, f'audio/{pathlib.Path(audio_file.name).suffix[1:]}')
                    }

                    upload_response = make_request(
                        "https://api.gladia.io/v2/upload/", headers, method="POST", files=files
                    )
                    st.write("Audio uploaded")
                    st.write(upload_response)
                    audio_url = upload_response.get("audio_url")

                    st.write(audio_url)

                    data = {
                        "audio_url": audio_url,
                        "diarization": True,
                        "diarization_config": {
                            "number_of_speakers": 2
                        },
                        "sentences": True,
                        "detect_language": False,
                        "language": "fr",
                        "subtitles": False
                    }
                    headers["Content-Type"] = "application/json"

                    st.write("- Sending request to Gladia API...")
                    post_response = make_request(
                        "https://api.gladia.io/v2/transcription/", headers, method="POST", data=data
                    )

                    st.write("Post response with Transcription ID:", post_response)
                    result_url = post_response.get("result_url")

                    if result_url:
                        while True:
                            with st.spinner("Polling for results..."):
                                poll_response = make_request(result_url, headers)

                                if poll_response.get("status") == "done":
                                    st.write("- Transcription done: \n")
                                    data = poll_response.get("result")

                                    for entry in data.get("sentences").get("results"):
                                        speaker = entry.get("speaker")
                                        sentence = entry.get("sentence")
                                        st.write(f"Speaker {speaker}: {sentence}")
                                    break
                                elif poll_response.get("status") == "error":
                                    st.write("- Transcription failed")
                                    st.write(poll_response)
                                # else:
                                    # st.write("Transcription status:", poll_response.get("status"))
                                sleep(5)

            except Exception as e:
                st.error(f"Error transcribing audio: {e}")
    else:
        st.error("Please upload an audio file.")