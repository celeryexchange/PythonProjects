letter_template_path = "Input/Letters/starting_letter.txt"
invited_people_path = "Input/Names/invited_names.txt"
finished_letters_folder = "Output/ReadyToSend/"

# find out who to send invitation letters to
with open(invited_people_path, "r") as f:
    people_to_invite = f.readlines()

for person in people_to_invite:
    person_name = person.strip()

    with open(letter_template_path, "r") as f:
        letter_template = f.read()

    letter = letter_template.replace("[name]", f"{person_name}")
    letter_path = finished_letters_folder + f"{person_name.replace(' ', '_')}_letter.txt"
    # print(finished_letter_path)

    with open(letter_path, "w") as f:
        f.write(letter)
