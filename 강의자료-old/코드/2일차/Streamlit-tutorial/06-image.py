import streamlit as st

tabs = st.tabs(["☕ 커피", "🍵 차"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/americano.jpg", use_container_width=True)
        st.button("아메리카노")
    with col2:
        st.image("images/latte.jpg", use_container_width=True)
        st.button("라떼")
with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/camomile.jpg", use_container_width=True)
        st.button("캐모마일", use_container_width=True)
    with col2:
        st.image("images/algray.jpg", use_container_width=True)
        st.button("얼그레이", use_container_width=True)
