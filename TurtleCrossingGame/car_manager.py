import turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
SPAWN_Y = list(range(-230, 230, 20))
SPAWN_X = list(range(0, 300, 20))
DEFAULT_NUMBER_OF_CARS = 5


class CarManager:
    def __init__(self):
        self.player_level = 1
        self.number_of_cars = DEFAULT_NUMBER_OF_CARS
        self.active_cars = []

    def spawn_cars(self):
        for i in range(self.number_of_cars):
            c = Car(player_level=self.player_level, on_screen=True)
            self.active_cars.append(c)

    def add_new_car(self):
        c = Car(player_level=self.player_level, on_screen=False)
        self.active_cars.append(c)

    def move_cars(self):
        for car in self.active_cars:
            car.move()


class Car(turtle.Turtle):
    def __init__(self, player_level, on_screen=False):
        super().__init__()
        self.shape("square")
        self.shapesize(1, 2)
        self.penup()
        self.color(random.choice(COLORS))
        self.setheading(180)  # face left
        self.player_level = player_level  # influences move speed

        # random starting position within set limits
        x = 350  # off-screen spawn point
        y = random.choice(SPAWN_Y)
        if on_screen:
            x = random.choice(SPAWN_X)
        self.setpos(x, y)

    def move(self):
        self.forward(STARTING_MOVE_DISTANCE + MOVE_INCREMENT * self.player_level)
