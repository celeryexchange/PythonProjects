# https://github.com/Akascape/CTkMessagebox
import customtkinter as tk
from PIL import Image
from password_generator import PasswordGenerator
import json

RED = "#e7305b"
DARK_GREY = "#313131"
LIGHT_GREY = "#D9D9D9"
DEFAULT_EMAIL = ""

tk.set_appearance_mode("system")  # default


class ToplevelWindow(tk.CTkToplevel):
    def __init__(self, message_text):
        super().__init__()
        # self.geometry("400x300")
        self.message_text = message_text

        # self.label = tk.CTkLabel(self, text="Your password has been saved.")
        self.label = tk.CTkLabel(self, text=self.message_text, justify="left")
        self.label.pack(padx=20, pady=20)


class App(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager")
        # self.geometry("400x400")
        self.configure(fg_color=(LIGHT_GREY, DARK_GREY))  # colour of frame's padding

        self.toplevel_window = None
        self.password_generator = None

        # Main frame
        self.main_frame = tk.CTkFrame(self, corner_radius=0)
        self.main_frame.configure(fg_color=(LIGHT_GREY, DARK_GREY))
        self.main_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        # Functions
        self.place_image()
        self.place_widgets()

    def place_image(self):
        # Load the image
        image_path = "logo.png"
        image = tk.CTkImage(dark_image=Image.open(image_path),
                            size=(200, 200))

        # Create a label to display the image
        label = tk.CTkLabel(self.main_frame, image=image, text="")
        label.grid(row=0, column=0, padx=20, pady=20, columnspan=3)

    def place_widgets(self):

        # text labels, left
        self.website_label = tk.CTkLabel(self.main_frame, text="Website")
        self.website_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="e")
        self.email_label = tk.CTkLabel(self.main_frame, text="Username/Email")
        self.email_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="e")
        self.password_label = tk.CTkLabel(self.main_frame, text="Password")
        self.password_label.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="e")

        # text entries
        self.website_entry = tk.CTkEntry(self.main_frame)
        self.website_entry.grid(row=1, column=1, columnspan=1, padx=(0, 10), pady=(0, 5), sticky="ew")
        self.website_entry.focus()
        self.email_entry = tk.CTkEntry(self.main_frame)
        self.email_entry.grid(row=2, column=1, columnspan=2, padx=(0, 10), pady=(0, 5), sticky="ew")
        self.email_entry.insert(0, DEFAULT_EMAIL)
        self.password_entry = tk.CTkEntry(self.main_frame)
        self.password_entry.grid(row=3, column=1, columnspan=1, padx=(0, 5), pady=(0, 5))

        # buttons
        self.search_button = tk.CTkButton(self.main_frame, text="Search", command=self.find_password)
        self.search_button.grid(row=1, column=2, padx=(0, 10), pady=(0, 5))
        self.generate_pass_button = tk.CTkButton(self.main_frame, text="Generate", command=self.generate_password)
        self.generate_pass_button.grid(row=3, column=2, padx=(0, 10), pady=(0, 5))
        self.add_button = tk.CTkButton(self.main_frame, text="Add", command=self.get_data_from_app)
        self.add_button.grid(row=4, column=1, columnspan=3, padx=(0, 10), pady=(0, 20), sticky="ew")

    def get_data_from_app(self):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # if all fields have values, save password
        if website and email and password:
            self.open_toplevel("Your password has been saved.")
            self.save_password(website, email, password)
            self.clear_app()
        else:
            self.open_toplevel("Nothing saved. Incomplete information.")

    def save_password(self, website: str, username: str, password: str):
        data_as_dict = {
            website: {
                "username": username,
                "password": password,
            }
        }
        try:
            with open("data.json", "r") as f:
                json_data = json.load(f)
                json_data.update(data_as_dict)
            with open("data.json", "w") as f:
                json.dump(json_data, f, indent=4)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(data_as_dict, f, indent=4)

    def clear_app(self):
        self.website_entry.delete(0, tk.END)
        # self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def open_toplevel(self, message_text):
        self.toplevel_window = ToplevelWindow(message_text)  # create window if its None or destroyed
        self.toplevel_window.focus()

    def generate_password(self):
        self.password_generator = PasswordGenerator()
        new_password = self.password_generator.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_password)

    def find_password(self):
        website = self.website_entry.get()
        if website:
            try:
                with open("data.json", "r") as f:
                    json_data = json.load(f)
                    username = json_data[website]["username"]
                    password = json_data[website]["password"]
            except FileNotFoundError:
                self.open_toplevel("You haven't saved any passwords yet.")
            except KeyError:
                self.open_toplevel(f"No saved password for website '{website}'.")
            else:
                display_message = f"""
                username: {username}
                password: {password}
                """
                self.open_toplevel(display_message)



if __name__ == "__main__":
    app = App()
    # pm = PasswordGenerator()
    # pm.generate_password()
    app.mainloop()

