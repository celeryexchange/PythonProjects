import turtle

screen = turtle.Screen()
screen.bgcolor('dark salmon')
# screen.exitonclick()

t = turtle.Turtle()
t.shape('turtle')
# t.color('turquoise')


def turn_left():
    t.left(10)


def turn_right():
    t.right(10)


def move_forward():
    t.fd(20)


def move_backward():
    t.bk(20)


def clear_screen():
    t.clear()
    t.up()
    t.home()
    t.down()


screen.onkeypress(move_forward, "w")
screen.onkeypress(move_backward, "s")
screen.onkeypress(turn_left, "a")
screen.onkeypress(turn_right, "d")
screen.onkeypress(clear_screen, "c")
screen.listen()

turtle.done()
