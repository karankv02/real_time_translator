# 🌐 Real-Time Language Translation App

An interactive **multi-language real-time translation app** built using **Streamlit** and **Hugging Face Transformers**.  
It supports **speech, text, and file-based translation** between multiple languages and includes **text-to-speech (TTS)** playback for the translated output.

---

## 🚀 Features

- 🎙️ **Speech-to-Text Translation** — Speak in one language and hear the translated output instantly.  
- 📝 **Text Input Translation** — Type text to translate between any supported language pairs.  
- 📂 **File Upload Support** — Upload `.txt` files for bulk translation.  
- 🔊 **Text-to-Speech Output** — Hear the translated text spoken back to you using Google TTS.  
- ⚡ **Real-Time Processing** — Fast inference with MarianMT translation models from Hugging Face.  
- 🧠 **Multi-language Support:**  
  - English  
  - Spanish  
  - French  
  - German  
  - Italian  
  - Portuguese  
  - Hindi  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Streamlit |
| **Speech Recognition** | SpeechRecognition |
| **Translation** | Hugging Face Transformers (MarianMT) |
| **Text-to-Speech** | gTTS (Google Text-to-Speech) |
| **Audio Handling** | pydub |
| **Language Models** | Helsinki-NLP MarianMT models |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/karankv02/real_time_translator.git
cd real-time-translation-app
2️⃣ Create a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt

💡 Note: ffmpeg must be installed on your system for pydub playback.
On Windows: choco install ffmpeg
On macOS: brew install ffmpeg

▶️ Running the App
bash
Copy code
streamlit run app.py
Then open the local URL shown in your terminal (usually http://localhost:8501).

```

## 🧠 How It Works
Speech Input (SpeechRecognition): Captures user voice and converts it to text in the selected source language.

Translation (MarianMT Model): Uses pre-trained translation models from Hugging Face (Helsinki-NLP/opus-mt-*) for conversion between languages.

Text-to-Speech (gTTS): Converts the translated text back into speech.

Streamlit UI: Provides a clean interface to choose input type, source/target languages, and hear the result.

## 👨‍💻 Author
Karan Vakkalad
Final Year CSE | Full-Stack Developer | AI & ML Enthusiast

## ⭐ Acknowledgements
Streamlit

Hugging Face Transformers

Google Text-to-Speech (gTTS)

pydub

If you found this project helpful, please ⭐ star this repository!
 
