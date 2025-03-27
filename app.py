import streamlit as st
import time
import random
import base64
from pathlib import Path

st.set_page_config(page_title="우슈 산타 타이머", layout="centered")

# 오디오 재생 함수
def play_audio(file_path):
    audio_bytes = Path(file_path).read_bytes()
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio autoplay>
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# 애니메이션 스타일 추가
st.markdown("""
    <style>
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    .timer {
        font-size: 80px;
        text-align: center;
        font-weight: bold;
        margin: 20px 0;
        color: #FF4B4B;
        animation: pulse 1s infinite;
    }
    .status {
        font-size: 32px;
        text-align: center;
        margin-bottom: 10px;
        color: #FFFFFF;
    }
    body {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎅 우슈 산타 타이머")

# Session state 초기화
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
    st.session_state.is_rest = False
    st.session_state.time_left = 180
    st.session_state.round = 1

# 사이드바 설정
round_time = st.sidebar.number_input("라운드 시간 (초)", min_value=10, value=180, step=10)
rest_time = st.sidebar.number_input("휴식 시간 (초)", min_value=10, value=60, step=10)

# 상태 출력
status_text = "휴식 중" if st.session_state.is_rest else f"라운드 {st.session_state.round}"
st.markdown(f"<div class='status'>{status_text}</div>", unsafe_allow_html=True)

# 타이머 표시
mins, secs = divmod(st.session_state.time_left, 60)
st.markdown(f"<div class='timer'>{mins:02}:{secs:02}</div>", unsafe_allow_html=True)

# 버튼 동작
def start_timer():
    st.session_state.is_running = True

def pause_timer():
    st.session_state.is_running = False

def reset_timer():
    st.session_state.is_running = False
    st.session_state.is_rest = False
    st.session_state.time_left = round_time
    st.session_state.round = 1

col1, col2, col3 = st.columns(3)
col1.button("▶️ 시작", on_click=start_timer)
col2.button("⏸️ 일시정지", on_click=pause_timer)
col3.button("🔁 리셋", on_click=reset_timer)

# 타이머 진행
if st.session_state.is_running:
    time.sleep(1)
    st.session_state.time_left -= 1

    # 소리 재생 조건
    if st.session_state.time_left == 3:
        play_audio("sounds/start_warning.wav")
    if st.session_state.time_left == 5:
        play_audio("sounds/end_warning.wav")
    if st.session_state.time_left == 0:
        if st.session_state.is_rest:
            play_audio("sounds/start_loud.wav")  # 라운드 시작 소리
            st.session_state.round += 1
            st.session_state.is_rest = False
            st.session_state.time_left = round_time
        else:
            play_audio("sounds/end_loud.wav")  # 라운드 종료 소리
            st.session_state.is_rest = True
            st.session_state.time_left = rest_time

    st.experimental_rerun()
