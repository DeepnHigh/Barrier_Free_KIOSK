import streamlit as st
import pandas as pd
import time
import random
import os


# 엑셀에서 가격표 불러오기
@st.cache_data
def load_price_table():
    df = pd.read_excel("menu_price.xlsx")
    price_dict = {}
    for _, row in df.iterrows():
        cat = row["category"]
        menu = row["menu"]
        price = row["price"]
        if cat not in price_dict:
            price_dict[cat] = {}
        price_dict[cat][menu] = price
    return price_dict


PRICE_TABLE = load_price_table()


def reset_selection():
    st.session_state.menu = None
    st.session_state.temp = None
    st.session_state.category = None


for key, default in {
    "step": 1,
    "category": None,
    "menu": None,
    "temp": None,
    "orders": [],
    "payment_correct": None,
    "order_number": 1,
    "accessibility_mode": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# # 배리어프리 모드 활성화 함수
# def run_accessibility_mode():
#     st.session_state.accessibility_mode = True
#     st.session_state.step = 2
#     st.write("음성 인식 모드가 활성화됩니다. 기다려 주세요.")

#     # whisper.py 실행
#     os.system("python whisper_chatgpt.py")


def add_order():
    price = PRICE_TABLE[st.session_state.category][st.session_state.menu]
    st.session_state.orders.append(
        {
            "category": st.session_state.category,
            "menu": st.session_state.menu,
            "temp": st.session_state.temp,
            "price": price,
        }
    )


def show_cart():
    st.markdown("---")
    st.subheader("🧾 현재 주문 내역")
    col_main, col_side = st.columns([3, 1])

    with col_main:
        for i, order in enumerate(st.session_state.orders):
            col1, col2 = st.columns([5, 1])
            with col1:
                temp = f" ({order['temp']})" if order["temp"] else ""
                st.write(f"{i+1}. {order['menu']}{temp} - {order['price']}원")
            with col2:
                if st.session_state.step < 5:
                    if st.button("❌", key=f"delete_{i}"):
                        st.session_state.orders.pop(i)
                        st.rerun()
        total = sum(item["price"] for item in st.session_state.orders)
        st.write(f"**총 금액: {total}원**")

    if st.session_state.step < 4:
        with col_side:
            if st.button("💳 바로 결제", use_container_width=True):
                st.session_state.step = 5
                st.rerun()


st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 50px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


if st.session_state.step == 1:
    st.markdown('<div class="title">codi-kiosk</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("일반 주문", use_container_width=True):
            st.session_state.accessibility_mode = False
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("배리어프리 주문", use_container_width=True):
            st.session_state.accessibility_mode = True
            st.session_state.step = 2
            st.write("음성 인식 모드가 활성화됩니다. 기다려 주세요.")
            # whisper.py 실행
            os.system("python whisper_chatgpt.py")

elif st.session_state.step == 2:
    st.header("1. 음료 선택")

    tabs = st.tabs(["☕ 커피", "🍵 차", "🍹 에이드", "🥤 스무디"])

    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/coffee/americano.jpg", use_container_width=True)
            if st.button("아메리카노"):
                st.session_state.category = "커피"
                st.session_state.menu = "아메리카노"
                st.session_state.temp = None
        with col2:
            st.image("images/coffee/latte.jpg", use_container_width=True)
            if st.button("라떼"):
                st.session_state.category = "커피"
                st.session_state.menu = "라떼"
                st.session_state.temp = None

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/tea/camomile.jpg", use_container_width=True)
            if st.button("캐모마일"):
                st.session_state.category = "차"
                st.session_state.menu = "캐모마일"
                st.session_state.temp = None
        with col2:
            st.image("images/tea/algray.jpg", use_container_width=True)
            if st.button("얼그레이"):
                st.session_state.category = "차"
                st.session_state.menu = "얼그레이"
                st.session_state.temp = None

    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/ade/grape.jpg", use_container_width=True)
            if st.button("청포도"):
                st.session_state.category = "에이드"
                st.session_state.menu = "청포도"
                st.session_state.temp = None
                add_order()
                reset_selection()
                st.session_state.step = 4
                st.rerun()
        with col2:
            st.image("images/ade/lemon.jpg", use_container_width=True)
            if st.button("레몬"):
                st.session_state.category = "에이드"
                st.session_state.menu = "레몬"
                st.session_state.temp = None
                add_order()
                reset_selection()
                st.session_state.step = 4
                st.rerun()

    with tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/smoothie/ddalgi.jpg", use_container_width=True)
            if st.button("딸기"):
                st.session_state.category = "스무디"
                st.session_state.menu = "딸기"
                st.session_state.temp = None
                add_order()
                reset_selection()
                st.session_state.step = 4
                st.rerun()
        with col2:
            st.image("images/smoothie/mango.jpg", use_container_width=True)
            if st.button("망고"):
                st.session_state.category = "스무디"
                st.session_state.menu = "망고"
                st.session_state.temp = None
                add_order()
                reset_selection()
                st.session_state.step = 4
                st.rerun()

# 메뉴 및 온도 선택 완료 시
if st.session_state.menu:
    if st.session_state.category in ["커피", "차"]:
        st.subheader("온도 선택")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧊 아이스", key="ice_button"):
                st.session_state.temp = "아이스"
                add_order()
                reset_selection()
                st.session_state.step = 4
                st.rerun()
        with col2:
            if st.button("🔥 핫", key="hot_button"):
                st.session_state.temp = "핫"
                add_order()
                reset_selection()
                st.session_state.step = 4
                st.rerun()
    elif st.session_state.category in ["에이드", "스무디"]:
        st.session_state.temp = None
        add_order()
        reset_selection()
        st.session_state.step = 4
        st.rerun()


elif st.session_state.step == 3:
    st.header("2. 메뉴 선택")

    if st.session_state.category == "커피":
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/coffee/americano.jpg", use_container_width=True)
            if st.button("아메리카노"):
                st.session_state.menu = "아메리카노"
        with col2:
            st.image("images/coffee/latte.jpg", use_container_width=True)
            if st.button("라떼"):
                st.session_state.menu = "라떼"

    elif st.session_state.category == "차":
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/tea/camomile.jpg", use_container_width=True)
            if st.button("캐모마일"):
                st.session_state.menu = "캐모마일"
        with col2:
            st.image("images/tea/algray.jpg", use_container_width=True)
            if st.button("얼그레이"):
                st.session_state.menu = "얼그레이"

    elif st.session_state.category == "에이드":
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/ade/grape.jpg", use_container_width=True)
            if st.button("청포도"):
                st.session_state.menu = "청포도"
        with col2:
            st.image("images/ade/lemon.jpg", use_container_width=True)
            if st.button("레몬"):
                st.session_state.menu = "레몬"

    elif st.session_state.category == "스무디":
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/smoothie/ddalgi.jpg", use_container_width=True)
            if st.button("딸기"):
                st.session_state.menu = "딸기"
        with col2:
            st.image("images/smoothie/mango.jpg", use_container_width=True)
            if st.button("망고"):
                st.session_state.menu = "망고"

    if st.session_state.menu and st.session_state.category in ["커피", "차"]:
        st.subheader("온도 선택")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧊 아이스"):
                st.session_state.temp = "아이스"
        with col2:
            if st.button("🔥 핫"):
                st.session_state.temp = "핫"
    elif st.session_state.menu:
        st.session_state.temp = None

    if st.session_state.menu and (
        st.session_state.temp is not None
        or st.session_state.category in ["에이드", "스무디"]
    ):
        add_order()
        reset_selection()
        st.session_state.step = 4
        st.rerun()

elif st.session_state.step == 4:
    st.header("3. 추가 주문 하시겠습니까?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ 추가 주문하기", use_container_width=True):
            reset_selection()
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("💳 결제하기", use_container_width=True):
            st.session_state.step = 5
            st.rerun()

elif st.session_state.step == 5:
    st.header("4. 금액을 투입하세요")
    total_price = sum(item["price"] for item in st.session_state.orders)
    st.write(f"총 결제 금액: {total_price}원")
    payment = st.number_input("결제 금액 입력", min_value=0, step=100)

    if st.button("결제"):
        if payment == total_price:
            st.session_state.payment_correct = True
            st.session_state.order_number = random.randint(1000, 9999)
            st.success("결제 완료!")
            st.session_state.step = 6
            st.rerun()
        else:
            st.error("금액이 일치하지 않습니다. 다시 시도해주세요.")

elif st.session_state.step == 6:
    st.success("✅ 주문이 완료되었습니다!")
    st.write(f"주문번호: {st.session_state.order_number}번")
    for i, order in enumerate(st.session_state.orders, start=1):
        st.write(f"{i}. {order['menu']} ({order['temp'] or ''}) - {order['price']}원")

    with st.spinner("5초 후 처음으로 돌아갑니다..."):
        time.sleep(5)
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if st.session_state.step >= 2 and st.session_state.orders:
    show_cart()
