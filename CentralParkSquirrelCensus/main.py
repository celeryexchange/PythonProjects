import turtle
import pandas as pd


class Map(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()

    def add_label(self, name, position):
        self.goto(position)
        self.write(f"{name}", align="center")


# setup the screen
screen = turtle.Screen()
screen.title("U.S. States Game")
image = "data/blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

# get states' coordinates from .csv
us_states = pd.read_csv("data/50_states.csv")
state_names = us_states.state.to_list()

game_is_on = True
already_guessed = []

while game_is_on:
    # ask the player to enter the name of a U.S. state
    answer = screen.textinput(title=f"{len(already_guessed)}/50 States Guessed", prompt="What's another state's name?")
    # capitalize each word (new york -> New York)
    answer = answer.title()

    # check if the name is correct
    if answer in state_names:
        print("That's correct!")
        # check if not already guessed it before
        if answer not in already_guessed:
            already_guessed.append(answer)
            # look up map coordinates for state
            state = us_states.loc[us_states.state == answer]
            map_coordinates = (state.x.values[0], state.y.values[0])
            # add a label at the correct place on the map
            m = Map().add_label(name=answer, position=map_coordinates)

    # exit when all states have been guessed
    if len(already_guessed) == 50:
        game_is_on = False
        print("Congratulations!")

    if answer in ["Exit", "Quit"]:
        break

missed_states = set(state_names).difference(set(already_guessed))
pd.Series(list(missed_states)).to_csv("states_to_learn.csv", index=False)

turtle.done()

