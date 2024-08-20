import turtle

STARTING_POSITION = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20


class SnakeBodySegment(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()


class Snake:
    def __init__(self):
        self.starting_positions = STARTING_POSITION
        self.snake_body = []
        self.create_snake()
        self.head = self.snake_body[0]
        # self.tail = self.snake_body[-1]

    def create_snake(self):
        for i in range(len(STARTING_POSITION)):
            self.add_snake_segment(STARTING_POSITION[i])

    def add_snake_segment(self, position):
        s = SnakeBodySegment()
        s.goto(position)
        self.snake_body.append(s)

    def extend_snake(self):
        self.add_snake_segment(self.snake_body[-1].position())

    def reset(self):
        for segment in self.snake_body:
            segment.goto(-500, 0)  # move old snake off screen
        self.snake_body.clear()  # remove all items from list
        self.create_snake()
        self.head = self.snake_body[0]

    def move(self):
        for i in range(len(self.snake_body)-1, 0, -1):
            next_pos = self.snake_body[i - 1].pos()
            self.snake_body[i].goto(next_pos)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        # if not facing down, orient up
        if self.head.heading() != 270:
            self.head.setheading(90)

    def down(self):
        # if not facing up, orient down
        if self.head.heading() != 90:
            self.head.setheading(270)

    def left(self):
        # if not facing right, turn left
        if self.head.heading() != 0:
            self.head.setheading(180)

    def right(self):
        # if not facing left, turn right
        if self.head.heading() != 180:
            self.head.setheading(0)
