import streamlit as st
import random
import time
import os
import json

youDict = {"Snake": 1, "Water": -1, "Gun": 0}
reverseDict = {1: "Snake", -1: "Water", 0: "Gun"}
LEADERBOARD_FILE = "leaderboard.json"

st.set_page_config(page_title="Multiplayer Snake Water Gun", page_icon="🎮")

st.title("🐍💧🔫 Snake - Water - Gun Game")

# Game Mode
mode = st.radio("Choose Mode:", ["Player vs Player", "Player vs Computer"])

if "score1" not in st.session_state:
    st.session_state.score1 = 0
    st.session_state.score2 = 0
if "timer_expired" not in st.session_state:
    st.session_state.timer_expired = False

player_name = st.text_input("Enter your name:", value="Player1")

# Timer
start_time = time.time()
TIMER_LIMIT = 10  # seconds

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧑 Player 1")
    choice1 = st.radio("Choose:", ["Snake", "Water", "Gun"], key="p1")

with col2:
    if mode == "Player vs Player":
        st.subheader("🧑‍🤝‍🧑 Player 2")
        choice2 = st.radio("Choose:", ["Snake", "Water", "Gun"], key="p2")
    else:
        choice2 = random.choice(["Snake", "Water", "Gun"])
        st.subheader("🤖 Computer will choose automatically.")

if st.button("🎯 Play Round"):
    if time.time() - start_time > TIMER_LIMIT:
        st.warning("⏱️ Time's up! You took too long.")
        st.session_state.timer_expired = True
        st.session_state.score2 += 1
    else:
        you = youDict[choice1]
        opponent = youDict[choice2]

        st.write(f"🧑 Player 1 chose: **{choice1}**")
        st.write(f"🧑‍🤝‍🧑 {'Player 2' if mode == 'Player vs Player' else 'Computer'} chose: **{choice2}**")

        if you == opponent:
            st.info("It's a draw!")
        elif (you == 1 and opponent == -1) or (you == -1 and opponent == 0) or (you == 0 and opponent == 1):
            st.success("✅ Player 1 Wins This Round!")
            st.session_state.score1 += 1
        else:
            st.success(f"✅ {'Player 2' if mode == 'Player vs Player' else 'Computer'} Wins This Round!")
            st.session_state.score2 += 1

        # Scores
        st.divider()
        st.subheader("🏆 Scoreboard")
        st.write(f"👉 {player_name}: {st.session_state.score1}")
        st.write(f"💻 {'Player 2' if mode == 'Player vs Player' else 'Computer'}: {st.session_state.score2}")

        # Leaderboard
        if mode == "Player vs Computer":
            def update_leaderboard(name, score):
                if not os.path.exists(LEADERBOARD_FILE):
                    with open(LEADERBOARD_FILE, "w") as f:
                        json.dump([], f)

                with open(LEADERBOARD_FILE, "r") as f:
                    board = json.load(f)

                board.append({"name": name, "score": score})
                board = sorted(board, key=lambda x: x["score"], reverse=True)[:5]

                with open(LEADERBOARD_FILE, "w") as f:
                    json.dump(board, f, indent=4)

            update_leaderboard(player_name, st.session_state.score1)

# Reset
if st.button("🔁 Reset Game"):
    st.session_state.score1 = 0
    st.session_state.score2 = 0
    st.session_state.timer_expired = False
    st.success("Game Reset!")

# Leaderboard
if st.button("📋 Show Leaderboard (Top 5)"):
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            board = json.load(f)
        st.subheader("🏅 Leaderboard")
        for entry in board:
            st.write(f"🥇 {entry['name']} : {entry['score']}")
    else:
        st.info("Leaderboard is empty. Play a few rounds first!")

# Theme Tip
with st.expander("🌗 Want Theme Support?"):
    st.markdown(
        """
        Streamlit uses your system/browser theme.  
        To switch manually:
        1. Click top-right ☰ menu
        2. Choose **Settings**
        3. Select light/dark theme
        """
    )
