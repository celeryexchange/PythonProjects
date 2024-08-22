import streamlit as st
from time import sleep
from data import get_quiz_questions, parse_questions, quiz_categories
from quiz_brain import QuizBrain


# Initialize session state variables
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'final_score_screen' not in st.session_state:
    st.session_state.final_score_screen = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_brain' not in st.session_state:
    st.session_state.quiz_brain = None


def start_quiz(topic, num_questions):
    questions = get_quiz_questions(size=num_questions, category=quiz_categories[topic])
    question_bank = parse_questions(questions)
    st.session_state.quiz_brain = QuizBrain(question_bank)
    st.session_state.quiz_brain.next_question()
    # st.session_state.selected_questions = random.sample(questions, k=num_questions)
    st.session_state.quiz_started = True
    st.session_state.score = 0
    st.rerun()


def show_question():
    # Show question text
    st.write(st.session_state.quiz_brain.show_question())
    # Show answer options
    with st.form("answer-form"):
        user_choice = st.radio("Choose an answer:", ["True", "False"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            check_answer(user_choice)


def check_answer(user_answer):
    # question = st.session_state.selected_questions[st.session_state.current_question]
    if st.session_state.quiz_brain.check_answer(user_answer):
        st.success("Correct!")
        st.session_state.score += 1
        sleep(1)
    else:
        st.error("Incorrect!")
        sleep(1)
    if st.session_state.quiz_brain.still_has_questions():
        st.session_state.quiz_brain.next_question()
        st.rerun()
    else:
        st.session_state.final_score_screen = True
        st.rerun()


def show_score():
    st.write("---")
    st.write(f"**Quiz Completed!**")
    st.write(f"Your Score: {st.session_state.score} / {len(st.session_state.quiz_brain.question_list)}")
    if st.button("Take Another Quiz"):
        st.session_state.quiz_started = False
        st.rerun()


def main():
    st.title("📚 Quizzler Quiz App")

    if not st.session_state.quiz_started:
        st.write("### Select Quiz Options")
        topic = st.selectbox("Choose a topic:", list(quiz_categories.keys()))
        num_questions = st.slider("Number of questions:", 3, 10, 5)
        if st.button("Start Quiz"):
            start_quiz(topic, num_questions)
    elif st.session_state.final_score_screen:
        show_score()
    else:
        show_question()


if __name__ == "__main__":
    main()
