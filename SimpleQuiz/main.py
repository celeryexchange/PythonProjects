from data import question_data
from question_model import Question
from quiz_brain import QuizBrain
import os

# create a question bank using all available questions from data
question_bank = [Question(question["text"], question["answer"]) for question in question_data]

# clear the terminal
os.system('cls||clear')

quiz = QuizBrain(question_bank)
while quiz.still_has_questions:
    quiz.next_question()

print("You've completed the quiz.")
print(f"Your final score was: {quiz.score}/{quiz.question_number}.")