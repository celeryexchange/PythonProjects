import turtle

MOVE_DISTANCE = 10
STARTING_POSITIONS = [(-370, 0), (370, 0)]


class Paddle(turtle.Turtle):

    def __init__(self, player_side):
        super().__init__()
        self.player_side = player_side
        self.shape("square")
        self.color("white")
        self.shapesize(4, 1)
        self.penup()
        self.move_to_position()

    def move_to_position(self):
        if self.player_side == 'left':
            self.setpos(STARTING_POSITIONS[0])
        else:
            self.setpos(STARTING_POSITIONS[1])

    def up(self):
        self.sety(self.ycor() + MOVE_DISTANCE)

    def down(self):
        self.sety(self.ycor() - MOVE_DISTANCE)

