import openai
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os

from playsound import playsound  # mp3 재생용

# OpenAI API 키
os.environ["OPENAI_API_KEY"] = (
    ""
)
# 녹음 설정
SAMPLERATE = 16000
DURATION = 3  # 녹음 길이 (초)


def record_audio():
    print("🎙️ 녹음 중...")
    audio = sd.rec(
        int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1, dtype="int16"
    )
    sd.wait()
    return audio


# Whisper API 호출 (최신 openai>=1.0.0 방식)
def transcribe(audio_data):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        wav.write(temp_wav.name, SAMPLERATE, audio_data)
        temp_wav_path = temp_wav.name

    with open(temp_wav_path, "rb") as file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1", file=file, language="ko"
        )

    os.remove(temp_wav_path)
    return transcript.text


# TTS로 음성 생성 및 재생
def speak(text):
    print(f"🗣️ speak(): {text}")
    response = openai.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        # ["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"] 가능
        input=text,
    )
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
        audio_file.write(response.content)
        audio_file.flush()
        audio_path = audio_file.name

    playsound(audio_path)
    os.remove(audio_path)


# 대화 흐름
def main():
    print("🎤 마이크가 켜졌습니다. '시작'이라고 말하세요.")
    state = "waiting"

    while True:
        audio_data = record_audio()
        text = transcribe(audio_data)
        print(f"📝 인식된 말: {text}")

        if state == "waiting" and "시작" in text:
            speak("안녕하세요. 자판기입니다. 콜라와 사이다 중 무엇을 원하세요?")
            state = "waiting_for_selection"

        elif state == "waiting_for_selection":
            if "콜라" in text:
                speak("콜라를 드리겠습니다.")
                break
            elif "사이다" in text:
                speak("사이다를 드리겠습니다.")
                break


if __name__ == "__main__":
    main()
