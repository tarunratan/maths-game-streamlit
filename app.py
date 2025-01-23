import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px

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
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
if "page" not in st.session_state:
    st.session_state.page = "setup"  # Track the current page
if "use_plotly" not in st.session_state:
    st.session_state.use_plotly = False  # Toggle for Plotly charts
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "MCQ"  # MCQ or Manual Input mode
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None  # Track user's answer in manual mode

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

# Set theme
def set_theme():
    if st.session_state.theme == "Dark":
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: white;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: white;
                color: black;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

# Page 1: Setup (Theme, Difficulty, and Game Mode Selection)
def setup_page():
    st.title("Multiplication Game by tarunratan🎮")
    st.write("Welcome! Please select your preferences to start the game.")

    # Theme selection
    st.session_state.theme = st.radio("Choose Theme", ["Light", "Dark"], index=0)
    set_theme()

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
    st.title("Multiplication Learning Game by tarunratan 🎮 lets connect at github.com/tarunratan ")
    st.write("Test your multiplication skills and improve your speed!")

    # Toggle for Plotly charts
    st.session_state.use_plotly = st.toggle("Use Interactive Charts (Plotly)", value=False)

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
            # Reset user_answer to None after each question
            if st.session_state.user_answer is not None:
                st.session_state.user_answer = None

            user_answer = st.number_input("Enter your answer:", min_value=0, step=1, value=None)
            if st.button("Submit"):
                st.session_state.user_answer = user_answer
                handle_answer(user_answer)

        # Progress bar (no fixed total number of questions)
        if st.session_state.response_times:
            progress = len(st.session_state.response_times) / (len(st.session_state.response_times) + 1)
            st.progress(min(progress, 1.0))  # Ensure progress does not exceed 1.0
            st.write(f"📊 Progress: {int(progress * 100)}%")

        # Display the score
        st.write(f"**Correct Answers:** {st.session_state.score}")

    # If the game is over, show statistics
    if st.session_state.game_over:
        st.write("### Game Over!")
        st.write(f"**Final Score (Correct Answers):** {st.session_state.score}")

        if st.session_state.response_times:
            # Create a DataFrame for the response times
            response_data = pd.DataFrame({
                "Question": range(1, len(st.session_state.response_times) + 1),
                "Response Time (seconds)": st.session_state.response_times
            })

            # Highlight fastest and slowest response times
            fastest_time = response_data["Response Time (seconds)"].min()
            slowest_time = response_data["Response Time (seconds)"].max()
            response_data["Highlight"] = response_data["Response Time (seconds)"].apply(
                lambda x: "Fastest" if x == fastest_time else ("Slowest" if x == slowest_time else "Normal")
            )

            # Display charts
            if st.session_state.use_plotly:
                # Use Plotly for interactive charts
                fig = px.bar(
                    response_data,
                    x="Question",
                    y="Response Time (seconds)",
                    color="Highlight",
                    color_discrete_map={"Fastest": "green", "Slowest": "red", "Normal": "blue"},
                    title="Response Times for Each Question"
                )
                st.plotly_chart(fig)
            else:
                # Use Streamlit's built-in charts
                col1, col2 = st.columns(2)
                with col1:
                    st.write("### Response Times (Bar Chart)")
                    st.bar_chart(response_data.set_index("Question"))

                with col2:
                    st.write("### Response Times (Line Chart)")
                    st.line_chart(response_data.set_index("Question"))

            # Display summary table
            st.write("### Summary Table")
            st.table(response_data)

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
            st.session_state.user_answer = None  # Reset user_answer
            st.session_state.page = "setup"  # Go back to setup page
            st.rerun()

# Handle user's answer
def handle_answer(user_answer):
    response_time = time.time() - st.session_state.start_time
    st.session_state.response_times.append(response_time)  # Record response time

    if user_answer == st.session_state.correct_answer:
        st.success(f"Correct! You answered in {response_time:.2f} seconds.")
        st.session_state.score += 1  # Increment score by 1 for each correct answer
        st.write(f"Correct answers: {st.session_state.score}")

        # Generate a new question
        st.session_state.question, st.session_state.options, st.session_state.correct_answer = generate_question()
        st.session_state.start_time = time.time()
        st.session_state.user_answer = None  # Reset user_answer
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