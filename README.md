# 🌐 Multilingual Translator

**Multilingual Translator** a real-time multilingual translation app that allows users to type in one language and receive an instant translation in another, optionally with audio output. It supports 20+ languages and enables smooth, conversational interaction through a clean Streamlit interface. The backend is built with **Flask** and uses **OpenAI's LLMs** for high-quality translation and text-to-speech synthesis. The architecture follows an **MCP** server concept, where each task—text handling, translation, and speech generation—is treated as a modular tool. This design enables clean separation of logic, easier maintenance, and scalability for adding more tools (like summarization or Q\&A) in the future.


![Index](static/Index1.png)

## 🎯 Features

* 🔤 **Text-to-Text Translation**: Translate any input between major global languages using OpenAI.
* 🗣️ **Text-to-Speech Generation**: Speak out translations in a natural voice.
* 📲 **Real-time Interface**: Built with Streamlit for an interactive front-end experience.
* 🌍 **Supports 20+ Languages**: Easily switch source and target languages from dropdowns.


## Architecture Overview

```
        ┌──────────────────────────────┐
        │        Streamlit UI          │
        │  - Text Input                │
        │  - Language Dropdown         │
        │  - Button: Translate & Speak │
        └────────────┬─────────────────┘
                     │
                     ▼
            User Input Triggered
                     │
                     ▼
┌────────────────────────────────────────────┐
│              Flask MCP Server              │
│────────────────────────────────────────────│
│ - Receives input text & user_id            │
│ - Adds to context_store[user_id]           │
│ - GPT translates based on history          │
│ - Audio (mp3) is generated using OpenAI    │
│ - Returns translated text + audio URL      │
└────────────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Streamlit Displays Output  │
        │ - Text area for translation│
        │ - Audio player for speech  │
        └────────────────────────────┘
```
## 📸 Screenshot

![Index](static/Index2.png)

## 🔮 Future Enhancements

🗣️ Improve Voice Accuracy
Enhance speech-to-text reliability and support real-time voice streaming.

🧵 Conversational Thread Memory
Store previous translations per user for smarter context switching.

🌐 Multilingual Chat Mode
Enable live chat interface between two people speaking different languages.

📱 Mobile-Friendly Interface
Optimize Streamlit UI for small screens with mic and TTS controls.

## Author

👤 **[Vetrivel Maheswaran](https://github.com/Vetrivel07)**

## Connect With Me 🌐

**[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vetrivel%20Maheswaran-green)](https://www.linkedin.com/in/vetrivel-maheswaran/)**

**[![PortFolio](https://img.shields.io/badge/Portfolio-Vetrivel%20Maheswaran-blue)](https://vetrivel07.github.io/vetrivel-maheswaran)**

<p align="center"><b>© Created by Vetrivel Maheswaran</b></p?