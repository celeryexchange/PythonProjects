import turtle

MOVE_DISTANCE = 10


class Ball(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_factor = 1
        self.y_factor = 1
        self.move_speed = 0.1  # smaller is faster

    def move(self):

        new_x = self.xcor() + MOVE_DISTANCE * self.x_factor
        new_y = self.ycor() + MOVE_DISTANCE * self.y_factor
        self.goto(new_x, new_y)

    def bounce_off_wall(self):
        self.y_factor *= -1
        self.move_speed *= 0.90

    def bounce_off_paddle(self):
        self.x_factor *= -1
        self.move_speed *= 0.90

    def reset_position(self):
        self.goto(0, 0)
        self.x_factor *= -1
        self.move_speed = 0.1

