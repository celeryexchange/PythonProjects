import turtle
import random

screen = turtle.Screen()
screen.setup(width=500, height=400)
screen.bgcolor('MistyRose')

# turtle colours
colours = ["Navy", "DeepPink", "DarkOliveGreen", "DarkOrange", "Firebrick"]
colour_mapping = {
    "Navy": "blue",
    "DeepPink": "pink",
    "DarkOliveGreen": "green",
    "DarkOrange": "orange",
    "Firebrick": "red",
}

# create five instances of the Turtle class
turtles = []
x_start = -200
y_start = -80
for i in range(5):
    t = turtle.Turtle(shape="turtle")
    t.color(colours[i])
    t.penup()
    turtles.append(t)
    # move the turtle to the starting position
    t.goto(x=x_start, y=y_start)
    y_start += 30

# time to make a bet
user_bet = screen.textinput(title="Make your bet",
                            prompt="Which turtle will win the race? Pick a colour: ")

# let's start the race
user_won = False
race_is_on = True

while race_is_on:
    for t in turtles:
        rand_distance = random.randint(1,10)
        t.forward(rand_distance)

        # check if turtle reached the finish line
        if t.pos()[0] >= 200:
            winning_turtle = t
            race_is_on = False

            # check if user won
            if user_bet.lower() == colour_mapping[winning_turtle.pencolor()]:
                user_won = True

print(f"The winner was {colour_mapping[winning_turtle.pencolor()]} or {winning_turtle.pencolor()}!")
if user_won:
    print("You've won!")

screen.exitonclick()
