import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import pyttsx3
import torch

print(torch.cuda.is_available())
# Whisper 모델 로딩 (성능 중요하면 "medium" 추천)
model = whisper.load_model("medium") # .to("cuda")
print(f"📦 Whisper 모델이 사용하는 장치: {model.device}")
# pyttsx3 초기화
engine = pyttsx3.init()

# 음성 속도/볼륨 설정
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

# 사용 가능한 보이스 확인 (한국어 지원 보이스 인덱스를 골라야 함)
voices = engine.getProperty("voices")
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name} / {voice.languages}")

# (예시) 한국어 여성 보이스 선택
# 시스템에 따라 다를 수 있으니, 위 출력 보고 적절한 인덱스로 교체
engine.setProperty("voice", voices[0].id)


# 실시간 음성 출력
def speak(text):
    print(f"🗣️ speak() 호출됨: {text}")
    engine.say(text)
    engine.runAndWait()


# 녹음 설정
SAMPLERATE = 16000
DURATION = 5 # 몇 초 동안 녹음할지 결정


# 오디오 녹음
def record_audio():
    print("🎙️ 녹음 중...")
    audio = sd.rec(
        int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1, dtype="int16"
    )
    sd.wait()
    return audio


# Whisper로 텍스트 변환
def transcribe(audio_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        wav.write(temp_file.name, SAMPLERATE, audio_data)
        temp_file.close()
        result = model.transcribe(temp_file.name, language="ko", fp16=False)
        os.unlink(temp_file.name)
    return result["text"]


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
