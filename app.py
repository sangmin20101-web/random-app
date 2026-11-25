import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="숫자 야구 게임", page_icon="⚾")

st.title("⚾ 숫자 야구 게임")
st.write("컴퓨터가 생각한 **서로 다른 3자리 숫자**를 맞혀보세요!")

# 게임 초기화 함수
def init_game():
    # 1~9 사이의 서로 다른 숫자 3개 뽑기 (첫 자리에 0이 오지 않게 설정)
    digits = list(range(1, 10))
    random.shuffle(digits)
    st.session_state.answer = "".join(map(str, digits[:3]))
    st.session_state.history = []
    st.session_state.game_over = False

# 세션 상태 초기화 (새로고침해도 게임 상태 유지)
if "answer" not in st.session_state:
    init_game()

# 사이드바: 게임 규칙 및 새 게임 버튼
with st.sidebar:
    st.header("📜 게임 규칙")
    st.markdown("""
    - **1~9** 사이의 **서로 다른 3자리 숫자**를 입력합니다.
    - **스트라이크 (S)**: 숫자와 위치가 모두 맞음
    - **볼 (B)**: 숫자는 맞지만 위치가 다름
    - **아웃 (OUT)**: 맞는 숫자가 하나도 없음
    """)
    if st.button("🔄 새 게임 시작", use_container_width=True):
        init_game()
        st.rerun()

# 사용자 입력 폼
if not st.session_state.game_over:
    with st.form(key="guess_form", clear_on_submit=True):
        guess = st.text_input("3자리 숫자를 입력하세요 (예: 123)", max_chars=3)
        submit = st.form_submit_button("던지기!")

        if submit:
            # 입력값 검증
            if len(guess) != 3 or not guess.isdigit() or "0" in guess:
                st.error("⚠️ 1부터 9까지의 숫자 3자리를 정확히 입력해주세요.")
            elif len(set(guess)) != 3:
                st.error("⚠️ 중복되지 않는 서로 다른 숫자를 입력해주세요.")
            else:
                # 스트라이크, 볼 판정
                strikes = 0
                balls = 0
                answer = st.session_state.answer

                for i in range(3):
                    if guess[i] == answer[i]:
                        strikes += 1
                    elif guess[i] in answer:
                        balls += 1

                # 결과 텍스트 생성
                if strikes == 3:
                    result = "🎉 **홈런! 정답입니다!**"
                    st.session_state.game_over = True
                elif strikes == 0 and balls == 0:
                    result = "❌ 아웃 (OUT)"
                else:
                    result = f"🟡 {strikes}S {balls}B"

                # 기록 저장
                st.session_state.history.append((guess, result))
                st.rerun()
else:
    st.success(f"축하합니다! 정답은 **{st.session_state.answer}** 였습니다. ({len(st.session_state.history)}번 만에 성공)")
    if st.button("다시 플레이하기"):
        init_game()
        st.rerun()

# 이전 시도 기록 출력
if st.session_state.history:
    st.subheader("📋 투구 기록")
    # 최신 기록이 위로 오도록 역순 출력
    for idx, (g, r) in enumerate(reversed(st.session_state.history), 1):
        attempt_num = len(st.session_state.history) - idx + 1
        st.write(f"**{attempt_num}회차:** `{g}` ➔ {r}")
