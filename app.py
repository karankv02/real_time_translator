import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import uuid

# Load translation model function
@st.cache_resource
def load_model(model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Translation function using MarianMT model
def translate_text(tokenizer, model, text):
    if text.strip() == "":
        return ""
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=256, truncation=True)
    translated = model.generate(inputs, max_length=256, num_beams=5, early_stopping=True)
    output = tokenizer.decode(translated[0], skip_special_tokens=True)
    return output

# Speech-to-Text function using SpeechRecognition
def speech_to_text(language_code):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        try:
            audio = r.listen(source, timeout=5)
            st.success("Processing audio...")
            # Use dynamic language code for speech recognition
            text = r.recognize_google(audio, language=language_code)
            return text
        except sr.UnknownValueError:
            return "Speech not recognized. Please try again."
        except sr.RequestError:
            return "Could not request results. Check your internet connection."
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."

# Text-to-Speech function using gTTS

def text_to_speech(text, lang):
    # Create a placeholder to show "Speaking..." message
    speaking_status = st.empty()
    speaking_status.info("Speaking the translated text...")

    # Temporary filename for gTTS output
    temp_filename = f"tts_output_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(temp_filename)

    # Play audio using pydub
    audio = AudioSegment.from_file(temp_filename, format="mp3")
    play(audio)

    # Remove the file after playback
    os.remove(temp_filename)
    
    # Clear the placeholder message after speaking
    speaking_status.empty()

# Language pairs dictionary
LANGUAGE_MODELS = {
    "English to Spanish": ("Helsinki-NLP/opus-mt-en-es", "es"),
    "English to French": ("Helsinki-NLP/opus-mt-en-fr", "fr"),
    "English to German": ("Helsinki-NLP/opus-mt-en-de", "de"),
    "English to Italian": ("Helsinki-NLP/opus-mt-en-it", "it"),
    "English to Portuguese": ("Helsinki-NLP/opus-mt-en-pt", "pt"),
    "Spanish to English": ("Helsinki-NLP/opus-mt-es-en", "en"),
    "French to English": ("Helsinki-NLP/opus-mt-fr-en", "en"),
    "German to English": ("Helsinki-NLP/opus-mt-de-en", "en"),
    "English to Hindi": ("Helsinki-NLP/opus-mt-en-hi", "hi"),
    "Hindi to English": ("Helsinki-NLP/opus-mt-hi-en", "en"),
}

# Streamlit UI - Title
st.title("Multi-Language Translator 🌐🎙️")
st.write("Translate text or speech to multiple languages and hear it back!")

# Sidebar for Settings
st.sidebar.title("Settings")

# Input Method Selection (Audio or Text)
input_type = st.sidebar.radio("Choose Input Method:", ["Audio Input (Speech-to-Text)", "Text Input", "File Upload"])

# Language Selection
source_lang = st.sidebar.selectbox("Choose Source Language:", ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Hindi"])
target_lang = st.sidebar.selectbox("Choose Target Language:", ["Spanish", "French", "German", "Italian", "Portuguese", "English", "Hindi"])

# Constructing the model name from the selected source and target languages
model_key = f"{source_lang} to {target_lang}"
model_name, output_lang = LANGUAGE_MODELS.get(model_key, (None, None))

# Handle case where an invalid model is chosen
if model_name is None:
    st.sidebar.error("The selected language pair is not available. Please choose a valid pair.")
else:
    tokenizer, model = load_model(model_name)

    # Determine the speech recognition language based on the source and target languages
    language_codes = {
    "English": "en-IN",    # English (India) - You can change to "en-US" for US English
    "Hindi": "hi-IN",      
    "Spanish": "es-ES",    
    "French": "fr-FR",     
    "German": "de-DE",     
    "Italian": "it-IT",    
    "Portuguese": "pt-PT"  
    }

# Ensure that the speech recognition matches the selected source language
    language_code = language_codes.get(source_lang, "en-IN")  

    # Displaying UI and translation functionality based on the selected input type
    if input_type == "File Upload":
        st.write("### Upload a .txt file for translation")
        uploaded_file = st.file_uploader("Choose a file", type=["txt"])

        if uploaded_file is not None:
            # Read the file content
            file_content = uploaded_file.getvalue().decode("utf-8")
            st.write("**Original Text in File:**")
            st.write(file_content)

            # Translate file content
            if file_content.strip():
                with st.spinner("Translating..."):
                    translated_text = translate_text(tokenizer, model, file_content)
                    st.write("**Translated Text:**")
                    st.write(translated_text)

                    # Add button to repeat the translation audio
                    if st.button("🔁 Repeat Translation"):
                        text_to_speech(translated_text, output_lang)

    elif input_type == "Audio Input (Speech-to-Text)":
        st.write("### Speak Now")
        if st.button("🎤 Speak"):
            user_input = speech_to_text(language_code)
            st.text(f"Recognized Text: {user_input}")

            if user_input and user_input.strip():
                with st.spinner("Translating..."):
                    translation = translate_text(tokenizer, model, user_input)
                    st.write("**Translated Text:**")
                    st.write(translation)

                    # Speak the translated text
                    text_to_speech(translation, output_lang)
            else:
                st.error("No valid speech detected. Try again!")

    else:
        # Manual Text Input Section
        st.write("### Text Input")
        manual_input = st.text_area("Enter text to translate:")
        if manual_input.strip():
            with st.spinner("Translating..."):
                translation = translate_text(tokenizer, model, manual_input)
                st.write("**Translated Text:**")
                st.write(translation)

                # Speak the translated text
                text_to_speech(translation, output_lang)
