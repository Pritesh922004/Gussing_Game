import random

import streamlit as st


DIFFICULTIES = {
    "Easy": {"attempts": 10, "range": 50},
    "Medium": {"attempts": 7, "range": 100},
    "Hard": {"attempts": 5, "range": 200},
}


def start_new_game(difficulty):
    settings = DIFFICULTIES[difficulty]
    st.session_state.difficulty = difficulty
    st.session_state.max_attempts = settings["attempts"]
    st.session_state.upper_bound = settings["range"]
    st.session_state.secret_number = random.randint(1, settings["range"])
    st.session_state.attempts_used = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.last_message = f"A new {difficulty} game has started."
    st.session_state.last_type = "info"


def ensure_state():
    if "secret_number" not in st.session_state:
        start_new_game("Medium")


def check_guess(guess):
    if st.session_state.game_over:
        return

    st.session_state.attempts_used += 1
    secret_number = st.session_state.secret_number
    remaining_attempts = st.session_state.max_attempts - st.session_state.attempts_used

    if guess == secret_number:
        st.session_state.game_over = True
        st.session_state.last_message = (
            f"Correct! You guessed the number in {st.session_state.attempts_used} attempt(s)."
        )
        st.session_state.last_type = "success"
        st.session_state.history.append(f"Attempt {st.session_state.attempts_used}: {guess} - Correct")
        return

    direction = "Too low!" if guess < secret_number else "Too high!"
    hint = "You are very close!" if abs(guess - secret_number) <= 5 else "Try again."
    st.session_state.history.append(
        f"Attempt {st.session_state.attempts_used}: {guess} - {direction} {hint}"
    )

    if remaining_attempts == 0:
        st.session_state.game_over = True
        st.session_state.last_message = f"Game over! The number was {secret_number}."
        st.session_state.last_type = "error"
    else:
        st.session_state.last_message = f"{direction} {hint} Attempts left: {remaining_attempts}"
        st.session_state.last_type = "warning"


def show_message():
    message_type = st.session_state.get("last_type", "info")
    message = st.session_state.get("last_message", "")
    if message:
        getattr(st, message_type)(message)


def main():
    st.set_page_config(page_title="Number Guessing Game UI", page_icon="🎯")
    ensure_state()

    st.title("🎯 Number Guessing Game UI")
    st.write("Guess the secret number before your attempts run out.")

    current_difficulty = st.session_state.get("difficulty", "Medium")
    difficulty = st.selectbox(
        "Select difficulty",
        list(DIFFICULTIES.keys()),
        index=list(DIFFICULTIES.keys()).index(current_difficulty),
    )

    if st.button("Start New Game", use_container_width=True):
        start_new_game(difficulty)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number Range", f"1 to {st.session_state.upper_bound}")
    with col2:
        attempts_left = st.session_state.max_attempts - st.session_state.attempts_used
        st.metric("Attempts Left", attempts_left)

    show_message()

    if not st.session_state.game_over:
        with st.form("guess_form"):
            guess = st.number_input(
                "Enter your guess",
                min_value=1,
                max_value=st.session_state.upper_bound,
                step=1,
            )
            submitted = st.form_submit_button("Submit Guess")
        if submitted:
            check_guess(int(guess))
            show_message()

    if st.session_state.history:
        st.subheader("Guess History")
        for item in st.session_state.history:
            st.write(f"- {item}")


if __name__ == "__main__":
    main()