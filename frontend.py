import streamlit as st
import os, requests, hashlib, tempfile
from streamlit_mic_recorder import mic_recorder


st.set_page_config(page_title="Multilingual Translator", layout="wide")
st.title("Multilingual Translator")

API_BASE = "http://127.0.0.1:5000"

# session state
if "inp" not in st.session_state:
    st.session_state["inp"] = ""
if "last_audio_md5" not in st.session_state:
    st.session_state["last_audio_md5"] = None

# Apply pending text before widgets
if "pending_inp" in st.session_state:
    st.session_state["inp"] = st.session_state.pop("pending_inp")

def md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()

# language pickers side-by-side
left, right = st.columns(2)
languages = [
    "English","Tamil","Hindi","Telugu","Kannada","Malayalam","Marathi",
    "Gujarati","Bengali","Punjabi","Urdu","Arabic","French","German",
    "Spanish","Chinese","Japanese","Korean","Russian","Portuguese"
]
source_lang = left.selectbox("Source Language", languages, index=0)
target_lang = right.selectbox("Target Language", languages, index=1)

# main columns: input (with recorder) | output
col1, col2 = st.columns(2)

with col1:
    
    # Bind textarea to a key; do NOT assign its return value
    st.text_area("Text to translate", key="inp", height=100)

    # Mic + Translate on one line
    row_mic, row_translate = st.columns([1, 6])

    with row_mic:
        rec = mic_recorder(
            start_prompt="🎙️",
            stop_prompt="🔴",
            key="mic",
            use_container_width=True
        )

    with row_translate:
        translate_clicked = st.button("Translate", key="translate_btn", use_container_width=True)

    if rec and rec.get("bytes"):
        audio_bytes = rec["bytes"]
        cur_md5 = md5(audio_bytes)
        if cur_md5 != st.session_state["last_audio_md5"]:
            st.session_state["last_audio_md5"] = cur_md5
            with st.spinner("Transcribing..."):
                files = {"audio": ("speech.webm", audio_bytes, "audio/webm")}
                try:
                    r = requests.post(f"{API_BASE}/stt", files=files, timeout=60)
                    if r.ok:
                        st.session_state["pending_inp"] = r.json().get("text", "").strip()
                        st.rerun()
                    else:
                        st.error(f"STT failed: {r.status_code} {r.text}")
                except Exception as e:
                    st.error(f"STT error: {e}")

    if translate_clicked:
        txt = st.session_state["inp"].strip()
        if not txt:
            st.warning("Type or record something to translate.")
        else:
            try:
                resp = requests.get(
                    f"{API_BASE}/translate",
                    params={
                        "input_text": txt,
                        "source_lang": source_lang,
                        "target_lang": target_lang
                    },
                    timeout=120
                )
                if resp.ok:
                    data = resp.json()
                    st.session_state["translated_text"] = data.get("translated_text","")
                    st.session_state["audio_url"] = data.get("audio_url","")
                else:
                    st.error(f"Translate failed: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Translate error: {e}")

with col2:
    
    st.text_area(
        "Translated Text",
        st.session_state.get("translated_text",""),
        height=100
    )
    au = st.session_state.get("audio_url")
    if au:
        st.audio(f"{API_BASE}{au}", format="audio/mp3")