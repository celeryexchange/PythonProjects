import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


class PasswordGenerator:
    def __init__(self):
        self.password_list = []
        self.nr_letters = random.randint(8, 10)
        self.nr_symbols = random.randint(2, 4)
        self.nr_numbers = random.randint(2, 4)

    def generate_password(self):
        pass_letters = [random.choice(letters) for _ in range(self.nr_letters)]
        pass_symbols = [random.choice(symbols) for _ in range(self.nr_symbols)]
        pass_numbers = [random.choice(numbers) for _ in range(self.nr_numbers)]
        self.password_list = pass_letters + pass_symbols + pass_numbers
        random.shuffle(self.password_list)
        password = "".join(self.password_list)

        return password
