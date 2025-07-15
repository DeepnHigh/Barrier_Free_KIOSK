import openai
from openai import OpenAI
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
from playsound import playsound # mp3 재생용
import uuid # For generating unique filenames

os.environ["OPENAI_API_KEY"] = (
    ""
)
client = OpenAI()
initial_prompt1 = """
    ### 역할
    당신은 매우 발랄한 고등학교 1학년 여학생입니다. 서로를 소개하는 대화를 진행해 주세요.
    
    ### 목표
    당신이 알아내야 할 정보는 다음과 같습니다:
    1) 이름 2) 성별 3) 나이 4) 학교
    모두 알아낸 다음, 알아낸 내용을 정리해서 얘기해주세요. 
    
    ### 주의사항
    질문은 하나씩 해주세요.
    이모티콘은 사용하지 마세요 
"""

# TTS로 음성 생성 및 재생
def speak(text):
    print(f"🗣️ speak(): {text}")
    response = openai.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text,
    )
    
    # Generate a unique filename in the current working directory
    # This avoids potential issues with long or complex tempfile paths
    unique_filename = f"temp_audio_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(os.getcwd(), unique_filename)

    try:
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)
        
        playsound(audio_path)
    except Exception as e:
        print(f"Error playing audio with playsound: {e}")
        print("Please check if the path is valid and if an appropriate MP3 player is associated with .mp3 files.")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path) # Clean up the temporary file


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
    # Using tempfile for recording is generally safer as playsound isn't involved
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        wav.write(temp_wav.name, SAMPLERATE, audio_data)
        temp_wav_path = temp_wav.name

    with open(temp_wav_path, "rb") as file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1", file=file, language="ko"
        )

    os.remove(temp_wav_path)
    return transcript.text


def ask(question, message_history=[], model="gpt-3.5-turbo"):
    if len(message_history) == 0:
        # 최초 질문
        message_history.append(
            {
                "role": "system",
                "content": initial_prompt1,
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


if __name__ == "__main__":
    main()