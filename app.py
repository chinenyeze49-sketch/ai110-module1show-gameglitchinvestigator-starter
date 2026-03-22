import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Guess History Section
st.sidebar.divider()
st.sidebar.subheader("📋 Guess History")

if st.session_state.history:
    for i, entry in enumerate(st.session_state.history, 1):
        guess = entry["guess"]
        outcome = entry["outcome"]
        
        # Determine emoji based on outcome
        if outcome == "Win":
            emoji = "✅"
        elif outcome == "Too High":
            emoji = "📈"
        elif outcome == "Too Low":
            emoji = "📉"
        elif outcome == "Invalid":
            emoji = "❌"
        else:
            emoji = "❓"
        
        st.sidebar.text(f"{emoji} Guess {i}: {guess}")
else:
    st.sidebar.caption("No guesses yet")

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)
with col4:
    st.empty()  # Spacer column

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing" and submit:
    if st.session_state.status == "won":
        st.info("You already won! Start a new game to play again.")
    else:
        st.info("Game over! Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append({"guess": raw_guess, "outcome": "Invalid"})
        st.error(err)
    else:
        outcome, message = check_guess(guess_int, st.session_state.secret)
        st.session_state.history.append({"guess": guess_int, "outcome": outcome})

        if show_hint:
            # Calculate distance for hot/cold indicator
            distance = abs(guess_int - st.session_state.secret)
            hot_cold_emoji = "🔥" if distance <= 10 else "🧊"
            
            # Color-coded hints
            if outcome == "Win":
                st.success(f"{message} {hot_cold_emoji}")
            elif outcome == "Too High":
                st.error(f"{message} {hot_cold_emoji}")
            else:  # Too Low
                st.info(f"{message} {hot_cold_emoji}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Display summary table when game ends
if st.session_state.status in ["won", "lost"]:
    st.divider()
    st.subheader("📊 Game Summary")
    
    # Build summary data
    summary_data = []
    for i, entry in enumerate(st.session_state.history, 1):
        guess = entry["guess"]
        outcome = entry["outcome"]
        
        if outcome == "Invalid":
            summary_data.append({
                "Guess #": i,
                "Guess": guess,
                "Outcome": outcome,
                "Status": "❌"
            })
        else:
            # Calculate distance for valid guesses
            distance = abs(guess - st.session_state.secret)
            hot_cold = "🔥" if distance <= 10 else "🧊"
            
            outcome_emoji = ""
            if outcome == "Win":
                outcome_emoji = "✅"
            elif outcome == "Too High":
                outcome_emoji = "📈"
            elif outcome == "Too Low":
                outcome_emoji = "📉"
            
            summary_data.append({
                "Guess #": i,
                "Guess": guess,
                "Outcome": outcome,
                "Distance": distance,
                "Status": f"{outcome_emoji} {hot_cold}"
            })
    
    # Display table
    st.table(summary_data)
    
    # Final stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attempts", st.session_state.attempts)
    with col2:
        st.metric("Final Score", st.session_state.score)
    with col3:
        valid_guesses = sum(1 for e in st.session_state.history if e["outcome"] != "Invalid")
        total_guesses = len(st.session_state.history)
        success_rate = (valid_guesses / total_guesses * 100) if total_guesses > 0 else 0
        st.metric("Valid Guesses", f"{success_rate:.0f}%")

if st.session_state.status == "playing":
    st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
