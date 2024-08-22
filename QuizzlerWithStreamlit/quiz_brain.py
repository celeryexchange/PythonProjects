class QuizBrain:

    def __init__(self, q_list):
        self.question_counter = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_counter < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_counter]
        self.question_counter += 1

    def show_question(self):
        return f"Question {self.question_counter}: {self.current_question.text}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if str(user_answer).lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False