import streamlit as st
import time
import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import pyttsx3
import torch



# 페이지 설정
st.set_page_config(
    page_title="커피 & 녹차 키오스크",
    page_icon="☕",
    layout="wide"
)

# 세션 상태 초기화
if 'drink_type' not in st.session_state:
    st.session_state.drink_type = None
if 'size' not in st.session_state:
    st.session_state.size = None
if 'temperature' not in st.session_state:
    st.session_state.temperature = None
if 'countdown' not in st.session_state:
    st.session_state.countdown = 5

# 제목
st.title("☕ 커피 & 녹차 키오스크")

# 첫 번째 화면 - 음료 종류 선택
if st.session_state.drink_type is None:
    st.subheader("음료를 선택해주세요")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("커피", use_container_width=True):
            st.session_state.drink_type = "커피"
            st.rerun()
    
    with col2:
        if st.button("녹차", use_container_width=True):
            st.session_state.drink_type = "녹차"
            st.rerun()
    st.subheader("음성 키오스크를 원하시면 아래 버튼을 눌러주세요")
    if st.button("음성 키오스크", use_container_width=True):
        st.session_state.voice_mode = True
        st.rerun()


# 두 번째 화면 - 사이즈 또는 온도 선택
elif st.session_state.drink_type == "커피" and st.session_state.size is None:
    st.subheader("커피 사이즈를 선택해주세요")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Small", use_container_width=True):
            st.session_state.size = "Small"
            st.rerun()
    
    with col2:
        if st.button("Medium", use_container_width=True):
            st.session_state.size = "Medium"
            st.rerun()
    
    with col3:
        if st.button("Large", use_container_width=True):
            st.session_state.size = "Large"
            st.rerun()

elif st.session_state.drink_type == "녹차" and st.session_state.temperature is None:
    st.subheader("녹차 온도를 선택해주세요")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Hot", use_container_width=True):
            st.session_state.temperature = "Hot"
            st.rerun()
    
    with col2:
        if st.button("Iced", use_container_width=True):
            st.session_state.temperature = "Iced"
            st.rerun()

# 주문 결과 표시
else:
    st.subheader("주문이 완료되었습니다!")
    
    if st.session_state.drink_type == "커피":
        st.write(f"주문하신 음료: {st.session_state.drink_type} ({st.session_state.size})")
    else:
        st.write(f"주문하신 음료: {st.session_state.drink_type} ({st.session_state.temperature})")
    
    # 카운트다운 표시
    countdown_placeholder = st.empty()
    countdown_placeholder.write(f"{st.session_state.countdown}초 후 첫 화면으로 돌아갑니다...")
    
    # 카운트다운 감소
    if st.session_state.countdown > 0:
        time.sleep(1)
        st.session_state.countdown -= 1
        st.rerun()
    else:
        # 카운트다운이 끝나면 첫 화면으로 돌아가기
        st.session_state.drink_type = None
        st.session_state.size = None
        st.session_state.temperature = None
        st.session_state.countdown = 5
        st.rerun()
    
    if st.button("새로운 주문하기"):
        st.session_state.drink_type = None
        st.session_state.size = None
        st.session_state.temperature = None
        st.session_state.countdown = 5
        st.rerun() 