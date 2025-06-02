import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import openai
import pyttsx3
from difflib import get_close_matches
import re

# OpenAI API 설정
client = openai.OpenAI(api_key="")  # 또는 os.environ["OPENAI_API_KEY"]

# TTS 설정
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)
engine.setProperty("voice", engine.getProperty("voices")[0].id)

def speak(text):
    """텍스트를 음성으로 출력"""
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()

# 음성 녹음 설정
SAMPLERATE = 16000
DURATION = 5

def record_audio():
    """음성 녹음"""
    print("🎙️ 녹음 중...")
    audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    return audio

def transcribe(audio_data):
    """Whisper로 음성 텍스트 변환"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        wav.write(temp_file.name, SAMPLERATE, audio_data)
        temp_file.close()

        with open(temp_file.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ko"
            )

        os.unlink(temp_file.name)
    return transcript.text.strip()
