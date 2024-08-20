import turtle


class ScoreBoard(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.high_score = 0
        self.score = 0
        self.penup()
        self.hideturtle()
        self.setpos(0, 280)  # top of the screen, middle
        self.color("white")  # font colour
        self.get_previous_high_score()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align="center")

    def increase_score(self, points):
        self.score += points
        self.update_scoreboard()

    def reset_scoreboard(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.write_current_high_score_to_file()
        self.update_scoreboard()

    def get_previous_high_score(self):
        try:
            with open("data.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            pass

    def write_current_high_score_to_file(self):
        try:
            with open("data.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
