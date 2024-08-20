import turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE: int = 10
FINISH_LINE_Y: int = 280


class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()

        self.penup()
        self.shape("turtle")
        self.color("black")
        self.setheading(90)  # face up
        self.move_to_start()

    def move_up(self):
        self.forward(MOVE_DISTANCE)

    def move_to_start(self):
        self.goto(STARTING_POSITION)

    @property
    def reached_finish_line(self):
        return self.ycor() >= FINISH_LINE_Y
