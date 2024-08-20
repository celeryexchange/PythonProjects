import turtle
import time
from snake import Snake
from food import Food
from scoreboard import ScoreBoard


def game_over():
    global game_is_on
    game_is_on = False


# screen properties
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0) # allows us to control when the screen gets refreshed

# instantiate all objects
snake = Snake()
food = Food()
scoreboard = ScoreBoard()

# controlling the snake
screen.listen()
screen.onkeypress(snake.up, "Up")
screen.onkeypress(snake.down, "Down")
screen.onkeypress(snake.left, "Left")
screen.onkeypress(snake.right, "Right")
screen.onkeypress(game_over, "q")

game_is_on = True
while game_is_on:
    screen.update() # refresh the screen
    time.sleep(0.1)
    snake.move()
    print(f"head: {snake.head.pos()}")

    # detect collision with food
    if snake.head.distance(food) <= 10:
        food.refresh()
        scoreboard.increase_score(1)
        snake.extend_snake()

    # detect collision with wall
    if snake.head.xcor() < -280 or snake.head.xcor() > 280 or snake.head.ycor() < -280 or snake.head.ycor() > 280:
        scoreboard.reset_scoreboard()
        snake.reset()

    # detect collision with tail
    for segment in snake.snake_body[1:]:
        if snake.head.distance(segment) <= 10:
            scoreboard.reset_scoreboard()
            snake.reset()

turtle.done()  # This keeps the window open until you close it
