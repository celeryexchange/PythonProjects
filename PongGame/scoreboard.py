import turtle

SCORE_POSITIONS = [(-100, 200), (100, 200)]


class Scoreboard(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_score()

    def update_score(self):
        self.clear()
        for i, score in enumerate([self.l_score, self.r_score]):
            self.goto(SCORE_POSITIONS[i])
            self.write(score, align="center", font=("Courier", 80, "normal"))

    def give_point_to_left_player(self):
        self.l_score += 1
        self.update_score()

    def give_point_to_right_player(self):
        self.r_score += 1
        self.update_score()


