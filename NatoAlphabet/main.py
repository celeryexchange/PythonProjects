import pandas as pd

nato_alphabet = pd.read_csv("nato_phonetic_alphabet.csv")
nato_dict = {row.letter: row.code for (index, row) in nato_alphabet.iterrows()}


def spell_word_using_nato_alphabet():
    try:
        word = input("Enter a word: ")
        word_spelled_out = [nato_dict[letter.upper()] for letter in word]
    except KeyError:
        # raise KeyError("Only words containing letters, please.")
        print("Only words containing letters, please.")
        spell_word_using_nato_alphabet()
    else:
        print(word_spelled_out)


spell_word_using_nato_alphabet()
