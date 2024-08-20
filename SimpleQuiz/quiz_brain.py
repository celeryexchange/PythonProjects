class QuizBrain:

    def __init__(self, question_list):
        self.question_number = 0
        self.question_list = question_list
        self.score = 0

    @property
    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        question = self.question_list[self.question_number]
        self.question_number += 1

        user_answer = input(f"{self.question_number}: {question.text} (True/False)?: ")
        self.check_answer(user_answer, question.answer)

    def check_answer(self, user_answer, correct_answer):
        # modify the answer string to a list to accept long and short answers
        correct_answer_list = []
        if correct_answer.lower() == "true":
            correct_answer_list = ["true", "t"]
        elif correct_answer.lower() == "false":
            correct_answer_list = ["false", "f"]
        else:
            pass

        if user_answer.lower() in correct_answer_list:
            print("You got it right!")
            self.score += 1
        else:
            print("No, that's wrong.")
        print(f"The correct answer was: {correct_answer}.")
        print(f"Your score is: {self.score}/{self.question_number}.")
        print()
