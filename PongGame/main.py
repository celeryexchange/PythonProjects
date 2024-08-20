import turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time


def game_over():
    global game_is_on
    game_is_on = False
    print("Game Over")


# general settings
turtle.speed("fastest")

# screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)  # allows us to control when the screen gets refreshed

# initialise objects
l_paddle = Paddle(player_side="left")
r_paddle = Paddle(player_side="right")
ball = Ball()
scoreboard = Scoreboard()
screen.update()

# user interaction
turtle.listen()
turtle.onkeypress(l_paddle.up, "w")
turtle.onkeypress(l_paddle.down, "s")
turtle.onkeypress(r_paddle.up, "Up")
turtle.onkeypress(r_paddle.down, "Down")
turtle.onkeypress(game_over, "q")

# game is on
game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()
    print(ball.ycor())

    # detect collision with wall
    if abs(ball.ycor()) > 280:
        ball.bounce_off_wall()

    # detect collision with paddles
    if r_paddle.distance(ball) < 50 and ball.xcor() > 340:
        ball.bounce_off_paddle()

    if l_paddle.distance(ball) < 50 and ball.xcor() < -340:
        ball.bounce_off_paddle()

    # detect miss (right)
    if ball.xcor() > 380:
        scoreboard.give_point_to_left_player()
        ball.reset_position()

    # detect miss (left)
    if ball.xcor() < -380:
        scoreboard.give_point_to_right_player()
        ball.reset_position()

turtle.done()
