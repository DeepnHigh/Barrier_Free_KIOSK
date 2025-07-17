import openai
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import uuid
from playsound import playsound  # mp3 재생용

# OpenAI API 키를 환경변수로 설정합니다.
# 반드시 본인의 OpenAI API 키로 입력해야 합니다.
os.environ["OPENAI_API_KEY"] = (
    ""
)
# 오디오 녹음 설정
SAMPLERATE = 16000  # 오디오 샘플링 레이트(Hz)
DURATION = 3  # 녹음 길이(초)


def record_audio():
    """
    마이크로부터 오디오를 녹음합니다.
    입력: 없음
    출력: 녹음된 오디오 데이터(numpy array)
    동작:
        - 지정된 샘플레이트와 길이로 마이크 입력을 녹음합니다.
        - 녹음이 끝날 때까지 대기합니다.
    """
    print("🎙️ 녹음 중...")
    audio = sd.rec(
        int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1, dtype="int16"
    )
    sd.wait()  # 녹음이 끝날 때까지 대기
    return audio


# Whisper API 호출 (최신 openai>=1.0.0 방식)
def transcribe(audio_data):
    """
    Whisper API를 사용해 오디오 데이터를 텍스트로 변환합니다.
    입력: audio_data (numpy array, 녹음된 오디오)
    출력: 변환된 텍스트(str)
    동작:
        - 임시 wav 파일로 오디오 데이터를 저장합니다.
        - Whisper API에 파일을 업로드하여 텍스트로 변환합니다.
        - 임시 파일을 삭제합니다.
    """
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

# 대화 흐름을 관리하는 메인 함수
def main():
    """
    음성 인식 및 TTS를 활용한 간단한 대화 시나리오를 실행합니다.
    입력: 없음
    출력: 없음
    동작:
        - '시작'이라는 음성 명령을 기다립니다.
        - '시작'이 감지되면 인사 및 선택지 안내를 음성으로 출력합니다.
        - 이후 '콜라' 또는 '사이다' 중 하나를 선택하면 해당 음성을 출력하고 종료합니다.
    """
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
