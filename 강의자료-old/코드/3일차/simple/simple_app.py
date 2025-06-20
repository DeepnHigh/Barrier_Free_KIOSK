import streamlit as st
import pandas as pd
import time
import random
import os


# 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 1
if "drink" not in st.session_state:
    st.session_state.drink = None
if "temperature" not in st.session_state:
    st.session_state.temperature = None

PRICE = {"아메리카노":2500, "카페라떼":3000, "카푸치노": 3500}


def reset_selection():
    st.session_state.menu = None
    st.session_state.temp = None
    st.session_state.category = None


# 배리어프리 모드 활성화 함수
def run_accessibility_mode():
    st.session_state.step = 2
    st.write("음성 인식 모드가 활성화되었습니다.")

    # whisper.py 실행
    os.system("python whisper_chatgpt_simple.py")


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



if st.session_state.step == 1:

    st.header("Codi-kiosk")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("배리어프리 주문", use_container_width=True):
            run_accessibility_mode()
    with col2:
        if st.button("일반 주문", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.header("1. 음료 선택")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("images/americano.jpg")
        if st.button("아메리카노", use_container_width=True):
            st.session_state.menu = "아메리카노"
            st.session_state.step = 3
            st.rerun()
    with col2:
        st.image("images/latte.jpg")
        if st.button("카페라떼", use_container_width=True):
            st.session_state.menu = "카페라떼"
            st.session_state.step = 3
            st.rerun()

    with col3:
        st.image("images/cappuchino.jpg")
        if st.button("카푸치노", use_container_width=True):
            st.session_state.menu = "카푸치노"
            st.session_state.step = 3
            st.rerun()

# 온도 선택
if st.session_state.step == 3:
    st.subheader("2. 온도 선택")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧊 아이스", key="ice_button"):
            st.session_state.temp = "아이스"
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("🔥 핫", key="hot_button"):
            st.session_state.temp = "핫"
            st.session_state.step = 4
            st.rerun()
    

elif st.session_state.step == 4:
    st.success("✅ 주문이 완료되었습니다!")
    st.write("주문내역:", st.session_state.temp + " " + st.session_state.menu)
    st.write("금액:", str(PRICE[st.session_state.menu])+"원")
    st.rerun()


