import customtkinter

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
DARK_RED = "#921E39"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
GREY = "#9BB0C1"
VIOLET = "#6420AA"
FONT_NAME = "JetBrains Mono"
WORK_MIN = 5
SHORT_BREAK_MIN = 2
LONG_BREAK_MIN = 20

completed_pomos = 0
take_a_break_next = False
is_work_pomo = False
timer = None

customtkinter.set_appearance_mode("system")  # default


class App(customtkinter.CTk):
    width = 260
    height = 440

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("PomodoroApp")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.configure(fg_color=PINK)
        # self.columnconfigure(0, weight=1)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.configure(fg_color=RED)
        self.main_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = customtkinter.CTkLabel(self.main_frame,
                                                  text="Pomodoro Timer",
                                                  font=customtkinter.CTkFont(size=14),
                                                  text_color=YELLOW)
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        self.countdown_label = customtkinter.CTkLabel(self.main_frame,
                                                      text="00:00",
                                                      font=customtkinter.CTkFont(family=FONT_NAME, size=60,
                                                                                 weight="bold"))
        self.countdown_label.grid(row=1, column=0, padx=30, pady=60)

        self.pomo_count_label = customtkinter.CTkLabel(self.main_frame,
                                                       text="",
                                                       text_color=GREEN)
        self.pomo_count_label.grid(row=2, column=0, padx=30, pady=10)

        self.start_button = customtkinter.CTkButton(self.main_frame,
                                                    text="Start",
                                                    command=self.start_countdown,
                                                    width=200,
                                                    fg_color=VIOLET,
                                                    hover_color=DARK_RED)
        self.start_button.grid(row=3, column=0, padx=30, pady=(30, 10))

        self.reset_button = customtkinter.CTkButton(self.main_frame,
                                                    text="Reset",
                                                    command=self.reset_app,
                                                    width=100,
                                                    fg_color=PINK,
                                                    hover_color=DARK_RED)
        self.reset_button.grid(row=4, column=0, padx=30, pady=(10, 20))

    def start_countdown(self):
        global completed_pomos
        global is_work_pomo
        is_work_pomo = False
        print(f"completed_pomos: {completed_pomos}")
        if take_a_break_next and completed_pomos < 4:
            print("Taking a short break.")
            self.count_down(SHORT_BREAK_MIN * 60)
            self.main_frame.configure(fg_color=GREY)
        elif take_a_break_next and completed_pomos == 4:
            print("Taking a long break.")
            self.count_down(LONG_BREAK_MIN * 60)
            self.main_frame.configure(fg_color=GREY)
        elif completed_pomos < 4:
            print("Work session.")
            is_work_pomo = True
            self.count_down(WORK_MIN * 60)
            self.main_frame.configure(fg_color=RED)

    def count_down(self, seconds: int = 0):
        global timer
        if seconds > 0:
            minutes_remaining = seconds // 60
            seconds_remaining = seconds % 60
            time_remaining = f"{minutes_remaining:02}:{seconds_remaining:02}"
            self.countdown_label.configure(text=time_remaining)
            timer = self.after(10, self.count_down, seconds - 1)
        else:
            global completed_pomos
            global take_a_break_next
            global is_work_pomo

            if is_work_pomo:
                completed_pomos += 1
                take_a_break_next = True
                self.update_icon_completed_pomos()
            else:
                take_a_break_next = False
            self.start_countdown()

    def update_icon_completed_pomos(self):
        global completed_pomos
        text = "✔" * completed_pomos
        self.pomo_count_label.configure(text=text)

    def reset_app(self):
        global timer
        global completed_pomos
        global take_a_break_next
        global is_work_pomo
        completed_pomos = 0
        self.after_cancel(timer)
        self.countdown_label.configure(text="00:00")
        self.update_icon_completed_pomos()
        self.main_frame.configure(fg_color=RED)
        timer = None
        take_a_break_next = False
        is_work_pomo = False


if __name__ == "__main__":
    app = App()
    app.mainloop()
