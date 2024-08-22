import streamlit as st
import random
from time import sleep
from data import get_quiz_questions, parse_questions, quiz_categories
from quiz_brain import QuizBrain

# Define quiz questions for different topics
quiz_data = {
    "Science": [
        {"question": "The Earth is the fourth planet from the Sun.", "answer": False},
        {"question": "Water boils at 100 degrees Celsius.", "answer": True},
        {"question": "Lightning never strikes in the same place twice.", "answer": False},
        {"question": "Humans have more than five senses.", "answer": True},
        {"question": "Gold is the most conductive metal.", "answer": False},
    ],
    "History": [
        {"question": "The Great Wall of China is visible from space.", "answer": False},
        {"question": "The Roman Empire fell in 476 AD.", "answer": True},
        {"question": "Albert Einstein was awarded the Nobel Prize for his theory of relativity.", "answer": False},
        {"question": "The first successful airplane flight was in 1903.", "answer": True},
        {"question": "The Titanic sank on its maiden voyage in 1912.", "answer": True},
    ],
    "Geography": [
        {"question": "Africa is the largest continent by land area.", "answer": False},
        {"question": "The Amazon River is the longest river in the world.", "answer": False},
        {"question": "Mount Everest is located in the Himalayas.", "answer": True},
        {"question": "Australia is both a country and a continent.", "answer": True},
        {"question": "The Sahara is the largest desert in the world.", "answer": True},
    ],
    "Sports": [
        {"question": "The Olympics are held every 2 years.", "answer": False},
        {"question": "Michael Jordan has won six NBA championships.", "answer": True},
        {"question": "The FIFA World Cup is held every 5 years.", "answer": False},
        {"question": "Tennis originated in France.", "answer": False},
        {"question": "The Super Bowl is the championship game of the NBA.", "answer": False},
    ],
    "Entertainment": [
        {"question": "The movie 'Avatar' was directed by James Cameron.", "answer": True},
        {"question": "'The Beatles' were a famous rock band from Australia.", "answer": False},
        {"question": "'Game of Thrones' is based on a book series by J.K. Rowling.", "answer": False},
        {"question": "Leonardo DiCaprio won his first Oscar for 'The Revenant'.", "answer": True},
        {"question": "'Friends' is a popular TV show that aired in the 1990s.", "answer": True},
    ],
}

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
