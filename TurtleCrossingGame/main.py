import turtle
import time
from player import Player
from car_manager import Car, CarManager
from scoreboard import Scoreboard


def game_over():
    global game_is_on
    game_is_on = False
    scoreboard.game_over_screen()
    print("Game Over")


def level_up():
    # move player back to starting position
    player.move_to_start()
    # show updated level
    scoreboard.update_score()
    # increase car speed
    car_manager.player_level += 1
    car_manager.spawn_cars()


# setup the screen
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.tracer(0)  # allows us to control when the screen gets refreshed
screen.title("Turtle Racing Game")

# instantiate all game objects
player = Player()
scoreboard = Scoreboard()
car_manager = CarManager()

# controls
turtle.listen()
screen.onkeypress(player.move_up, "Up")
screen.onkeypress(game_over, "q")

# start the game
game_is_on = True
car_manager.spawn_cars()
frames_played = 0
while game_is_on:

    # refresh screen
    time.sleep(0.1)
    screen.update()
    frames_played += 1

    # move cars
    car_manager.move_cars()

    # spawn a new car off-screen every 6 frames
    if frames_played % 6 == 0:
        car_manager.add_new_car()

    # level up game if player reaches the top
    if player.reached_finish_line:
        level_up()

    # detect collision with a car
    for car in car_manager.active_cars:
        if player.distance(car) < 30:
            # print("Collision detected.")
            game_over()

# stop execution
turtle.done()
