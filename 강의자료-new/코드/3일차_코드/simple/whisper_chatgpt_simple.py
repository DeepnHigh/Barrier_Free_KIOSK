import openai
from openai import OpenAI
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
from playsound import playsound  # mp3 재생용

# OpenAI API
os.environ["OPENAI_API_KEY"] = (
    ""
)
client = OpenAI()

initial_prompt = """
당신은 카페의 친절한 직원입니다.
다음 순서에 따라서 주문을 받으면 됩니다.

[1단계]
- [아메리카노, 카페라떼, 카푸치노] 메뉴 중 하나를 주문받으면 됩니다.

[2단계]
- [아이스, 핫] 중 하나를 주문받으세요.

[3단계]
{아메리카노:2500, 카페라떼:3000, 카푸치노: 3500}
- 위 금액 책정에 따라 총 금액을 계산하세요.
- 주문 내역과 총 금액을 말하고 주문해 주셔서 감사합니다 라고 말하세요.
- 맨 마지막 말로 '종료합니다' 를 반드시 말하세요.

"""


# TTS로 음성 생성 및 재생
def speak(text):
    print(f"🗣️ speak(): {text}")
    response = openai.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text,
    )
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
        audio_file.write(response.content)
        audio_file.flush()
        audio_path = audio_file.name

    playsound(audio_path)
    os.remove(audio_path)


# 음성 녹음
SAMPLERATE = 16000
DURATION = 3


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


def ask(question, message_history=[], model="o4-mini-2025-04-16"):
    if len(message_history) == 0:
        # 최초 질문
        message_history.append(
            {
                "role": "system",
                "content": initial_prompt,
            }
        )

    # 사용자 질문 추가
    message_history.append(
        {
            "role": "user",
            "content": question,
        },
    )

    # GPT에 질문을 전달하여 답변을 생성
    completion = client.chat.completions.create(
        model=model,
        messages=message_history,
    )

    # 사용자 질문에 대한 답변을 추가
    message_history.append(
        {"role": "assistant", "content": completion.choices[0].message.content}
    )

    return message_history


if __name__ == "__main__":
    message_history = ask("안녕하세요?", message_history=[])
    speak(message_history[-1]["content"])

    while True:
        audio_data = record_audio()
        user_text = transcribe(audio_data)
        print(f"📝 인식된 말: {user_text}")
        message_history = ask(user_text, message_history=message_history)
        speak(message_history[-1]["content"])

        if any(
            x in message_history[-1]["content"]
            for x in ["종료", "끝", "그만", "결제", "주문 끝", "주문 완료", "다 했어"]
        ):
            break
