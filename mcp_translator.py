# 1. IMPORTS
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
import os, uuid

# 2. LOAD ENVIRONMENT
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 3. FLASK APP INIT
app = Flask(__name__)
context_store = {}

# 4. TOOL: TEXT TRANSLATION + TTS
def translate_tool(user_id, input_text, source_lang, target_lang):
    # a. Build message history
    history = context_store.get(user_id, [])
    messages = [
        {"role": "system", "content": f"You are a translator. Translate from {source_lang} to {target_lang}."}
    ] + [{"role": msg["role"], "content": msg["message"]} for msg in history]
    messages.append({"role": "user", "content": input_text})

    # b. Get translated response from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    translated_text = response.choices[0].message.content.strip()

    # c. Convert translated text to speech
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=translated_text,
        response_format="mp3"
    )
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("audio", filename)
    os.makedirs("audio", exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(audio_response.content)

    # d. Save conversation
    history.append({"role": "user", "message": input_text})
    history.append({"role": "assistant", "message": translated_text})
    context_store[user_id] = history

    # e. Return output
    return {
        "translated_text": translated_text,
        "audio_url": f"/audio/{filename}"
    }

# 5. ROUTE: API ENDPOINT
@app.route("/translate", methods=["GET"])
def translate():
    user_id = request.args.get("user_id")
    input_text = request.args.get("input_text")
    source_lang = request.args.get("source_lang", "English")
    target_lang = request.args.get("target_lang", "Tamil")

    if not user_id or not input_text:
        return jsonify({"error": "Missing input"}), 400

    result = translate_tool(user_id, input_text, source_lang, target_lang)
    return jsonify(result)

# 6. ROUTE: AUDIO FETCH
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("audio", filename, mimetype="audio/mp3")

# 7. RUN APP
if __name__ == "__main__":
    app.run(debug=True)
