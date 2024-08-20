import customtkinter
from PIL import Image
import os
import pandas as pd
import random


# pip install customtkinter
# pip install pillow

PATH_TO_WORDS = "data/french_words.csv"
BACKGROUND_COLOR = "#B1DDC6"
WHITE_COLOR = "#FFFFFF"
DARK_GREY_COLOR = "#888888"
BLACK_COLOR = "#000000"
OLIVE_COLOR = "#91C2AF"


class Dictionary:
    def __init__(self, path_to_vocabulary):
        self.path_to_vocabulary = path_to_vocabulary
        # load the vocabulary
        path_to_vocabulary_folder = os.path.dirname(path_to_vocabulary)
        path_to_words_to_learn = os.path.join(path_to_vocabulary_folder, "words_to_learn.csv")
        try:
            df = pd.read_csv(path_to_words_to_learn)
        except FileNotFoundError:
            df = pd.read_csv(path_to_vocabulary)
        self.dict = df.to_dict(orient="records")
        # current word pair
        self.current_word_pair = {}
        # languages based on the first word pair in the dictionary
        self.languages_tuple = tuple(self.dict[0].keys())

    def return_first_word_pair(self):
        return self.dict[0]

    def return_random_word_pair(self):
        self.current_word_pair = random.choice(self.dict)
        return self.current_word_pair

    def generate_random_word_pair(self):
        self.current_word_pair = random.choice(self.dict)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Flash Card App")
        self.geometry("700X700")
        self.configure(padx=20, pady=20, fg_color=BACKGROUND_COLOR)
        self.is_flipped = False
        self.flip_timer = self.after(3000, self.flip_card)

        # load images from /images/
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image_card_back = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "card_back.png")),
            size=(600, 400))
        self.image_card_front = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "card_front.png")),
            size=(600, 400))
        self.image_button_correct = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "right.png")),
            size=(50, 50))
        self.image_button_wrong = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "wrong.png")),
            size=(50, 50))

        # place images
        self.label_card = customtkinter.CTkLabel(self, image=self.image_card_front, text="")
        self.label_card.grid(row=0, column=0, padx=20, pady=20, columnspan=2, rowspan=2)

        # place words
        self.language_name = customtkinter.CTkLabel(self, text="", font=("Aptos Display", 16, "italic"))
        self.language_name.grid(row=0, column=0, columnspan=2, pady=(50, 0))

        self.word = customtkinter.CTkLabel(self, text="", font=("Aptos Display", 48, "bold"))
        self.word.grid(row=1, column=0, columnspan=2, pady=(0, 50), sticky="n")

        # place buttons
        self.button_wrong = customtkinter.CTkButton(self, image=self.image_button_wrong, text="",
                                                    fg_color="transparent", command=self.button_pressed_wrong)
        self.button_wrong.grid(row=2, column=0, pady=(0, 20))
        self.button_correct = customtkinter.CTkButton(self, image=self.image_button_correct, text="",
                                                      fg_color="transparent", command=self.button_pressed_correct)
        self.button_correct.grid(row=2, column=1, pady=(0, 20))

        # show new word
        self.next_card()

    def next_card(self):
        # generate and show a new word
        fr_dict.generate_random_word_pair()
        self.show_foreign_word()
        # flip the card after 3 seconds but stop all previous timers first
        self.after_cancel(self.flip_timer)
        self.flip_timer = self.after(3000, self.flip_card)

    def button_pressed_correct(self):
        fr_dict.dict.remove(fr_dict.current_word_pair)
        print(len(fr_dict.dict))
        self.save_words_to_learn_to_csv()
        self.next_card()

    def button_pressed_wrong(self):
        self.next_card()

    def show_foreign_word(self):
        self.is_flipped = False
        self.label_card.configure(image=self.image_card_front)
        self.language_name.configure(text=fr_dict.languages_tuple[0],
                                     fg_color=WHITE_COLOR,
                                     text_color=DARK_GREY_COLOR)
        self.word.configure(text=fr_dict.current_word_pair["French"],
                            fg_color=WHITE_COLOR,
                            text_color=BLACK_COLOR)

    def show_translation(self):
        self.is_flipped = True
        self.label_card.configure(image=self.image_card_back)
        self.language_name.configure(text=fr_dict.languages_tuple[1],
                                     fg_color=OLIVE_COLOR,
                                     text_color=WHITE_COLOR)
        self.word.configure(text=fr_dict.current_word_pair["English"],
                            fg_color=OLIVE_COLOR,
                            text_color=WHITE_COLOR)

    def flip_card(self):
        if self.is_flipped:
            self.show_foreign_word()
        else:
            self.show_translation()

    @staticmethod
    def save_words_to_learn_to_csv():
        words_to_learn = pd.DataFrame(fr_dict.dict)
        words_to_learn.to_csv("data/words_to_learn.csv", index=False)


if __name__ == "__main__":
    # instantiate a new dictionary
    fr_dict = Dictionary(PATH_TO_WORDS)
    # run the flash card app
    app = App()
    app.mainloop()
