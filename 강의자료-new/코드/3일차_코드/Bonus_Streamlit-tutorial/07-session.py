import streamlit as st

# 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 1
if "drink" not in st.session_state:
    st.session_state.drink = None
if "temperature" not in st.session_state:
    st.session_state.temperature = None


# 1단계: 음료 선택
if st.session_state.step == 1:
    st.subheader("1단계: 음료를 선택하세요")
    tabs = st.tabs(["커피", "차"])
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("아메리카노"):
                st.session_state.drink = "아메리카노"
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("카페라떼"):
                st.session_state.drink = "카페라떼"
                st.session_state.step = 2
                st.rerun()
    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("녹차", use_container_width=True):
                st.session_state.drink = "녹차"
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("홍차", use_container_width=True):
                st.session_state.drink = "홍차"
                st.session_state.step = 2
                st.rerun()

# 2단계: 온도 선택
elif st.session_state.step == 2:
    st.subheader("2단계: 온도를 선택하세요")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧊 ICE"):
            st.session_state.temperature = "ICE"
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🔥 HOT"):
            st.session_state.temperature = "HOT"
            st.session_state.step = 3
            st.rerun()

# 3단계: 결과 출력
elif st.session_state.step == 3:
    st.subheader("✅ 주문 결과")
    st.write(f"선택한 음료: **{st.session_state.drink}**")
    st.write(f"선택한 온도: **{st.session_state.temperature}**")

    if st.button("🔄 다시 선택하기"):
        st.session_state.step = 1
        st.session_state.drink = None
        st.session_state.temperature = None
        st.rerun()
