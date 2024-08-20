import turtle
import random


class Food(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("white")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        random_x = random.randint(-9, 9) * 20
        random_y = random.randint(-9, 9) * 20
        self.setpos(random_x, random_y)
