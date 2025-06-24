# 🌐 Multilingual Translator

**Multilingual Translator** is an intelligent, real-time translator built with Flask and Streamlit. It enables users to input text in one language and translate it into another, and optionally hear the translated output. This tool is ideal for seamless multilingual communication and supports over 20 global languages.

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