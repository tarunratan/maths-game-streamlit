import streamlit as st
import random
import time

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "response_times" not in st.session_state:
    st.session_state.response_times = []
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"
if "page" not in st.session_state:
    st.session_state.page = "setup"  # Track the current page
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "MCQ"  # MCQ or Manual Input mode

# Generate a random multiplication question based on difficulty
def generate_question():
    if st.session_state.difficulty == "Easy":
        num1 = random.randint(1, 5)
        num2 = random.randint(1, 5)
    elif st.session_state.difficulty == "Medium":
        num1 = random.randint(5, 10)
        num2 = random.randint(5, 10)
    else:  # Hard
        num1 = random.randint(10, 15)
        num2 = random.randint(10, 15)

    correct_answer = num1 * num2
    wrong_answers = [correct_answer + random.randint(1, 5), correct_answer - random.randint(1, 5)]
    options = [correct_answer] + wrong_answers
    random.shuffle(options)
    return (f"What is {num1} * {num2}?", options, correct_answer)

# Page 1: Setup (Difficulty and Game Mode Selection)
def setup_page():
    st.title("Multiplication Game 🎮")
    st.write("Welcome! Please select your preferences to start the game.")

    # Difficulty selection
    st.session_state.difficulty = st.radio("Choose Difficulty", ["Easy", "Medium", "Hard"], index=0)

    # Game mode selection
    st.session_state.game_mode = st.radio("Choose Game Mode", ["MCQ", "Manual Input"], index=0)

    # Start game button
    if st.button("Start Game"):
        st.session_state.page = "game"
        st.rerun()

# Page 2: Main Game
def game_page():
    st.title("Multiplication Game 🎮")
    st.write("Test your multiplication skills!")

    # Generate a new question if needed
    if st.session_state.question is None and not st.session_state.game_over:
        st.session_state.question, st.session_state.options, st.session_state.correct_answer = generate_question()
        st.session_state.start_time = time.time()

    # Display the question if the game is not over
    if not st.session_state.game_over:
        st.write(f"### {st.session_state.question}")

        # Timer (10 seconds per question)
        time_limit = 10
        time_remaining = time_limit - (time.time() - st.session_state.start_time)
        if time_remaining > 0:
            st.write(f"⏳ Time remaining: {int(time_remaining)} seconds")
        else:
            st.error("Time's up! Game over.")
            st.session_state.game_over = True
            st.rerun()

        # MCQ Mode: Display options as buttons
        if st.session_state.game_mode == "MCQ":
            for option in st.session_state.options:
                if st.button(str(option), key=option):
                    handle_answer(option)

        # Manual Input Mode: Allow user to type their answer
        else:
            user_answer = st.number_input("Enter your answer:", min_value=0, step=1, value=None)
            if st.button("Submit"):
                handle_answer(user_answer)

        # Display the score
        st.write(f"**Correct Answers:** {st.session_state.score}")

    # If the game is over, show statistics
    if st.session_state.game_over:
        st.write("### Game Over!")
        st.write(f"**Final Score (Correct Answers):** {st.session_state.score}")

        if st.session_state.response_times:
            # Calculate average response time
            average_time = sum(st.session_state.response_times) / len(st.session_state.response_times)
            st.write(f"⏱️ **Average Response Time:** {average_time:.2f} seconds")

        # Option to restart the game
        if st.button("Restart Game"):
            st.session_state.score = 0
            st.session_state.question = None
            st.session_state.start_time = None
            st.session_state.game_over = False
            st.session_state.response_times = []
            st.session_state.page = "setup"  # Go back to setup page
            st.rerun()

# Handle user's answer
def handle_answer(user_answer):
    response_time = time.time() - st.session_state.start_time
    st.session_state.response_times.append(response_time)  # Record response time

    if user_answer == st.session_state.correct_answer:
        st.success(f"Correct! You answered in {response_time:.2f} seconds.")
        st.session_state.score += 1  # Increment score by 1 for each correct answer

        # Generate a new question
        st.session_state.question, st.session_state.options, st.session_state.correct_answer = generate_question()
        st.session_state.start_time = time.time()
        st.rerun()
    else:
        st.error("Wrong answer! Game over.")
        st.session_state.game_over = True  # End the game
        st.rerun()

# Main app
def main():
    if st.session_state.page == "setup":
        setup_page()
    elif st.session_state.page == "game":
        game_page()

# Run the app
if __name__ == "__main__":
    main()