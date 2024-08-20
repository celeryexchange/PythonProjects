from question_model import Question
from data_api import get_quiz_questions
from quiz_brain import QuizBrain
from ui import QuizUI
import html

# generate new quiz questions from an external API
question_data = get_quiz_questions(size=5, category=18)

question_bank = []
for question in question_data:
    # decode HTML with html.unescape(), e.g. "Hello &amp; welcome" -> "Hello & welcome"
    question_text = html.unescape(question["question"])
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)


quiz_brain = QuizBrain(question_bank)
quiz_ui = QuizUI(quiz_brain)

# while quiz.still_has_questions():
#     quiz.next_question()
#
# print("You've completed the quiz")
# print(f"Your final score was: {quiz.score}/{quiz.question_counter}")
