from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
import os, uuid
from werkzeug.utils import secure_filename

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# TOOL: TEXT TRANSLATION + TTS
def translate_tool(input_text, source_lang, target_lang):
    #a. Build Message
    messages = [
        {"role": "system", "content": f"You are an Excellent translator. You should Translate the user input from {source_lang} to {target_lang}."},
        {"role": "user", "content": input_text},
    ]

    # b. Get translated response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )
    translated_text = response.choices[0].message.content.strip()

    # c. Convert translated text to speech
    audio_response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=translated_text,
        response_format="mp3"
    )
    
    os.makedirs("audio", exist_ok=True)
    filename = f"{uuid.uuid4().hex}.mp3"
    with open(os.path.join("audio", filename), "wb") as f:
        f.write(audio_response.content)

    # d. Return output
    return {
        "translated_text": translated_text,
        "audio_url": f"/audio/{filename}"
    }

# ROUTE: API ENDPOINT
@app.route("/translate", methods=["GET"])
def translate():
    input_text = request.args.get("input_text")
    source_lang = request.args.get("source_lang", "English")
    target_lang = request.args.get("target_lang", "Tamil")

    if not input_text:
        return jsonify({"error": "Missing input"}), 400

    return jsonify(translate_tool(input_text, source_lang, target_lang))
    

@app.route("/stt", methods=["POST"])
def stt():
    if "audio" not in request.files:
        return jsonify({"error": "no audio"}), 400
    f = request.files["audio"]
    fname = secure_filename(f.filename or "audio.webm")
    path = os.path.join("audio", fname)
    os.makedirs("audio", exist_ok=True)
    f.save(path)

    # Transcribe
    with open(path, "rb") as af:
        tr = client.audio.transcriptions.create(
            model="whisper-1",   # replace if you use a different STT model
            file=af
        )
    text = tr.text if hasattr(tr, "text") else tr["text"]
    return jsonify({"text": text})

# ROUTE: AUDIO FETCH
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("audio", filename, mimetype="audio/mp3")

if __name__ == "__main__":
    app.run(debug=True)
