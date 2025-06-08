import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import openai
import pyttsx3


# OpenAI API
client = openai.OpenAI(api_key="")  # 또는 os.environ["OPENAI_API_KEY"]

initial_prompt = """
당신은 카페의 친절한 직원입니다.
다음 순서에 따라서 주문을 받으면 됩니다.

[1단계]
- [커피, 차, 에이드, 스무디] 메뉴 중 하나를 주문받으면 됩니다.

[2단계]
- 메뉴가 커피이면 [아메리카노, 라떼] 중 하나를 주문받으세요.
- 메뉴가 차 이면 [캐모마일, 얼그레이] 중 하나를 주문받으세요.
- 메뉴가 에이드 이면 [청포도, 레몬] 중 하나를 주문받으세요.
- 메뉴가 스무디 이면 [딸기, 망고] 중 하나를 주문받으세요.

[3단계]
- 메뉴가 [커피, 차] 중 하나일 경우 [아이스, 핫] 중 하나를 주문받으세요.
- 메뉴가 [에이드, 스무디] 중 하나일 경우 건너뛰면 됩니다.

[4단계]
- 추가 주문을 할 건지 묻고, 주문할 경우 현재의 메뉴를 기억하고 [1단계]로 돌아가세요.
- 추가 주문이 없을 경우 현재의 메뉴를 기억하고 다음 단계로 넘어가세요.

[5단계]
{아메리카노:2500, 라떼:3000, 캐모마일:2700, 얼그레이:2700, 청포도:3200, 레몬:3200, 딸기:3500, 망고:3500}
- 위 금액 책정에 따라 총 금액을 계산하세요.
- 총 금액을 말하고 주문해 주셔서 감사합니다 라고 말하세요.
- 맨 마지막 말로 '종료합니다' 를 반드시 말하세요.


"""

# TTS
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)
engine.setProperty("voice", engine.getProperty("voices")[0].id)
 
def speak(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()

# 음성 녹음
SAMPLERATE = 16000
DURATION = 5

def record_audio():
    print("🎙️ 녹음 중...")
    audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    return audio

def transcribe(audio_data):
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


# 메인 루프
def main():
    message_history = ask("안녕하세요?", message_history=[])
    speak(message_history[-1]["content"])

    
    while True:
        audio_data = record_audio()
        user_text = transcribe(audio_data)
        print(f"📝 인식된 말: {user_text}")
        message_history = ask(user_text, message_history=message_history)
        speak(message_history[-1]["content"])
        

        if any(x in message_history[-1]["content"] for x in ["종료", "끝", "그만", "결제", "주문 끝", "주문 완료", "다 했어"]):
            break

if __name__ == "__main__":
    main()
