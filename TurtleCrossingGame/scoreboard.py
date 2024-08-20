import turtle

FONT = ("JetBrains Mono", 18, "normal")
SCOREBOARD_POSITION = (-275, 250)


class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.color("black")
        self.hideturtle()
        self.goto(SCOREBOARD_POSITION)
        self.player_level = 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.player_level += 1
        self.write(arg=f"Level {self.player_level:02}", font=FONT)

    def game_over_screen(self):
        self.clear()
        self.goto(0, 0)
        self.write(arg=f"Game over. You've reached level {self.player_level}", align="center")
