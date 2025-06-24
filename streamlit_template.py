import streamlit as st
import requests
import os

# UI setup
st.set_page_config(page_title="Multilingual Translator", layout="wide")
st.title("Multilingual Translator")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Text")

    user_input = st.text_area("Text to translate:", height=150)

    languages = [
    "English", "Tamil", "Hindi", "Telugu", "Kannada", "Malayalam", "Marathi",
    "Gujarati", "Bengali", "Punjabi", "Urdu", "Arabic", "French", "German",
    "Spanish", "Chinese", "Japanese", "Korean", "Russian", "Portuguese"
    ]

    source_lang = st.selectbox("Source Language", languages, index=0)
    target_lang = st.selectbox("Target Language", languages, index=1)

    if st.button("Translate & Speak"):
        if not user_input:
            st.warning("Please enter text to translate.")
        else:
            response = requests.get(
                "http://127.0.0.1:5000/translate",
                params={
                    "user_id": "vetri",
                    "input_text": user_input,
                    "source_lang": source_lang,
                    "target_lang": target_lang
                }
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state["translated_text"] = result["translated_text"]
                st.session_state["audio_url"] = result["audio_url"]
            else:
                st.error("Failed to get translation.")

with col2:
    st.subheader("Translated Output")

    if "translated_text" in st.session_state:
        st.text_area("Translated Text", st.session_state["translated_text"], height=150)

    if "audio_url" in st.session_state:
        st.audio(f"http://127.0.0.1:5000{st.session_state['audio_url']}", format="audio/mp3")
