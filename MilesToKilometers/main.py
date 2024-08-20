import tkinter
import customtkinter


# documentation: https://customtkinter.tomschimansky.com/
# tutorial: https://customtkinter.tomschimansky.com/tutorial/beginner/


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        def button_callback():
            miles = self.entry_miles.get()
            kilometers = float(miles)  * 1.60934
            self.entry_kilometers.configure(text=str(kilometers))

        self.title("Calculator")
        self.geometry("300x150")
        self.configure(padx=20, pady=20)

        self.text_1 = customtkinter.CTkLabel(self, text="Convert miles to kilometers.")
        self.text_1.grid(row=0, column=0)

        self.entry_miles = customtkinter.CTkEntry(self)
        self.entry_miles.grid(row=1, column=0, sticky="w")
        self.label_miles = customtkinter.CTkLabel(self, text="miles")
        self.label_miles.grid(row=1, column=1, padx=10)

        self.entry_kilometers = customtkinter.CTkLabel(self, text="0")
        self.entry_kilometers.grid(row=2, column=0, sticky="w")
        self.label_kilometers = customtkinter.CTkLabel(self, text="kilometers")
        self.label_kilometers.grid(row=2, column=1, padx=10)

        self.button = customtkinter.CTkButton(self, text="Calculate", command=button_callback)
        self.button.grid(row=3, sticky="ew")


# Run the app
app = App()
app.mainloop()
