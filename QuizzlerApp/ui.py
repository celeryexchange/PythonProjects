import customtkinter
from PIL import Image
import os
from quiz_brain import QuizBrain


# pip install customtkinter
# pip install pillow

THEME_COLOR = "#375362"
WHITE_COLOR = "#FFFFFF"
QUESTION_TEXT_COLOR = "#355b4c"
GREEN_COLOR = "#43da9e"
RED_COLOR = "#da5a43"


class QuizUI(customtkinter.CTk):
    def __init__(self, quiz_brain: QuizBrain):
        super().__init__()

        self.quiz = quiz_brain
        self.title("Quizzler")
        # self.geometry("500X700") # doesn't seem to be doing anything
        self.configure(padx=20, pady=20, fg_color=THEME_COLOR)

        # load icons from /images/
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        image_button_true = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "true.png")),
            size=(50, 50))
        image_button_false = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "false.png")),
            size=(50, 50))

        # place elements
        self.score_label = customtkinter.CTkLabel(self, text="Score: 0", font=("Aptos Display", 16))
        self.score_label.grid(row=0, column=1, columnspan=1, pady=(0, 20))

        self.question_label = customtkinter.CTkLabel(self, text="", font=("Aptos Display", 20),
                                                     bg_color=WHITE_COLOR, wraplength=260,
                                                     text_color=QUESTION_TEXT_COLOR,
                                                     width=300, height=250)
        self.question_label.grid(row=1, column=0, columnspan=2, pady=(0, 50), sticky="we")

        # place buttons
        self.true_button = customtkinter.CTkButton(self, image=image_button_true, text="",
                                                   fg_color="transparent", command=self.button_pressed_true)
        self.true_button.grid(row=2, column=0, padx=(0, 0))

        self.false_button = customtkinter.CTkButton(self, image=image_button_false, text="",
                                                    fg_color="transparent", command=self.button_pressed_false)
        self.false_button.grid(row=2, column=1, padx=(0, 0))

        # run loop when instantiated
        self.show_next_question()
        self.mainloop()

    def enable_buttons(self):
        self.true_button.configure(command=self.button_pressed_true)
        self.false_button.configure(command=self.button_pressed_false)

    def disable_buttons(self):
        self.true_button.configure(command=None)
        self.false_button.configure(command=None)

    def hide_buttons(self):
        self.true_button.grid_forget()
        self.false_button.grid_forget()

    def button_pressed_true(self):
        self.check_answer("True")

    def button_pressed_false(self):
        self.check_answer("False")

    def check_answer(self, user_answer):
        self.disable_buttons()
        if self.quiz.check_answer(user_answer):
            self.question_label.configure(bg_color=GREEN_COLOR)
        else:
            self.question_label.configure(bg_color=RED_COLOR)
        self.score_label.configure(text=f"Score: {self.quiz.score}/{self.quiz.question_counter}")
        self.after(2000, self.show_next_question)

    def show_next_question(self):
        if self.quiz.still_has_questions():
            self.enable_buttons()
            self.question_label.configure(text=self.quiz.next_question(), bg_color=WHITE_COLOR)
        else:
            self.score_label.configure(text="")
            self.question_label.configure(text=f"Final score: {self.quiz.score}/{self.quiz.question_counter}")
            self.question_label.configure(bg_color=THEME_COLOR, text_color=WHITE_COLOR, font=("Aptos Display", 36))
            self.hide_buttons()

# if __name__ == "__main__":
#     app = QuizUI()
#     app.mainloop()
