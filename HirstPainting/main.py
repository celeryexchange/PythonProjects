from turtle import Turtle, Screen
import random


def random_colour():
    """ Returns a random colour as three values
    from 0.0 to 1.0 representing red, green and blue. """
    r = random.random()
    g = random.random()
    b = random.random()
    colour_tuple = (r, g, b)
    return colour_tuple


def draw_dots_in_line(n_dots, distance):
    for d in range(n_dots):
        timmy.dot(20, random_colour())
        timmy.up()
        timmy.forward(distance)


def draw_hirst_painting(n_dots, canvas_size):

    # set position to middle of screen
    timmy.up()
    starting_position = canvas_size/2 * -1
    timmy.setpos(starting_position, starting_position)

    # determine spacing between dots given canvas size
    spacing = canvas_size / n_dots

    # draw a square of dots starting from bottom left and moving up
    for d in range(n_dots):
        current_pos_x, current_pos_y = timmy.pos()
        draw_dots_in_line(n_dots, spacing)
        timmy.setpos(starting_position, current_pos_y + spacing)


# our buddy
timmy = Turtle()
timmy.speed("fast")

draw_hirst_painting(10, 500)

screen = Screen()
screen.exitonclick()


# for l in range(10):
#     draw_dots_in_line(10, 40)
#     timmy.setpos(0, 40)

#
# print(timmy.pos())
# timmy.setx(40)
# timmy.dot(20, random_colour())

# # draw a square
# for i in range(4):
#     timmy.forward(100)
#     timmy.right(90)

# # draw a dashed line
# for i in range(20):
#     # draw, pen down
#     timmy.pd()
#     timmy.forward(5)
#     # don't draw, pen up
#     timmy.pu()
#     timmy.forward(5)

# # draw geometrical objects
# for n in range(3, 9):
#     angle = 360 / n
#     r, g, b = random_colour()
#     timmy.pencolor((r, g, b))
#     # distance = 400 / n
#     for side in range(n):
#         # timmy.pencolor((0.1, 0, 1))
#         timmy.forward(100)
#         timmy.right(angle)


# def random_walk():
#     # new colour for each walk
#     # r, g, b = random_colour()
#     timmy.pencolor(random_colour())
#     # move 20 paces into a random direction
#     timmy.setheading(random.choice([0, 90, 180, 270]))
#     timmy.forward(20)
#
#
# for s in range(50):
#     random_walk()

# def draw_spirograph(circles):
#     heading_change = 360 / circles
#     for c in range(circles):
#         current_heading = timmy.heading()
#         timmy.pencolor(random_colour())
#         timmy.circle(50)
#         timmy.setheading(current_heading + heading_change)
#
#
# draw_spirograph(16)


