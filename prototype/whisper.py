import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import openai
import pyttsx3
from difflib import get_close_matches
import re

# OpenAI API
client = openai.OpenAI(api_key="")  # 또는 os.environ["OPENAI_API_KEY"]

# 음료 가격 및 카테고리
DRINK_PRICES = {
    "아메리카노": 2500, "라떼": 3000,
    "캐모마일": 2700, "얼그레이": 2700,
    "청포도": 3200, "레몬": 3200,
    "딸기": 3500, "망고": 3500
}
HOT_ICE_ITEMS = ["아메리카노", "라떼", "캐모마일", "얼그레이"]
DRINK_CATEGORIES = {
    "커피": ["아메리카노", "라떼"],
    "차": ["캐모마일", "얼그레이"],
    "에이드": ["청포도", "레몬"],
    "스무디": ["딸기", "망고"]
}
ALL_DRINKS = list(DRINK_PRICES.keys())
TEMP_KEYWORDS = ["아이스", "핫", "차가운", "따뜻"]

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

def match_keyword(text, keyword_pool, cutoff=0.7):
    return get_close_matches(text, keyword_pool, n=1, cutoff=cutoff)[0] if get_close_matches(text, keyword_pool, n=1, cutoff=cutoff) else None

# 주문 상태
order_list = []
current_task = None

# 수량 추출
def extract_quantity(text):
    match = re.search(r"(\d+)잔", text)
    if match:
        return int(match.group(1))
    return 1

# 온도 추출
def extract_temperature(text):
    if "아이스" in text or "차가운" in text:
        return "아이스"
    elif "핫" in text or "따뜻" in text:
        return "핫"
    return None

# 사용자 입력 분석 및 주문 파싱
def parse_order(text):
    quantity = extract_quantity(text)
    temp = extract_temperature(text)
    for drink in ALL_DRINKS:
        if drink in text:
            order = {"name": drink, "temp": temp if drink in HOT_ICE_ITEMS else None, "price": DRINK_PRICES[drink], "quantity": quantity}
            order_list.append(order)
            desc = f"{temp + ' ' if temp else ''}{drink} {quantity}잔"
            speak(f"{desc} 추가되었습니다.")

# 주문 확인 및 종료 조건
def summarize_order():
    if not order_list:
        speak("주문하신 음료가 없습니다.")
        return
    summary = ", ".join([f"{o['temp']} {o['name']} {o['quantity']}잔" if o['temp'] else f"{o['name']} {o['quantity']}잔" for o in order_list])
    total = sum([o['price'] * o['quantity'] for o in order_list])
    speak(f"{summary} 주문 확인되었습니다. 총 {total}원입니다.")
    speak("카드를 투입해주세요. 결제가 완료되면 음료가 준비됩니다.")

# 금액 요청 처리
def handle_price_request():
    if not order_list:
        speak("현재까지 주문하신 음료가 없습니다.")
    else:
        total = sum([o['price'] * o['quantity'] for o in order_list])
        speak(f"현재까지 총 금액은 {total}원입니다.")

# 메인 루프
def main():
    speak("안녕하세요. 음료를 주문해주세요. 종료하려면 '종료'라고 말해주세요." \
    " 음료 종류로는 커피, 차, 에이드, 스무디가 있습니다.")
    while True:
        audio_data = record_audio()
        user_text = transcribe(audio_data)
        print(f"📝 인식된 말: {user_text}")

        if any(x in user_text for x in ["종료", "끝", "그만", "결제", "주문 끝", "주문 완료", "다 했어"]):
            summarize_order()
            speak("주문이 완료되어 프로그램을 종료합니다. 감사합니다.")
            break

        if any(x in user_text for x in ["금액", "얼마", "가격"]):
            handle_price_request()
            continue

        if "메뉴" in user_text or ("어떤" in user_text and "있어" in user_text):
            for category, items in DRINK_CATEGORIES.items():
                speak(f"{category} 카테고리에는 {', '.join(items)}가 있습니다.")
            continue

        parse_order(user_text)

if __name__ == "__main__":
    main()
