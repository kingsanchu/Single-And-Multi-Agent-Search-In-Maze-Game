import tkinter as tk


class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(
            self, text="Start Game", command=self.show_difficulty_page)
        self.start_button.pack(side="top")

        self.quit_button = tk.Button(self, text="Quit", command=self.quit_game)
        self.quit_button.pack(side="bottom")

    def show_difficulty_page(self):
        self.destroy()  # Destroy the current frame (main menu)
        DifficultyPage(self.master)  # Pass master to DifficultyPage

    def quit_game(self):
        self.master.destroy()  # Close the application


class DifficultyPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Select Difficulty:")
        self.label.pack(pady=10)

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Easy")  # Default difficulty

        difficulties = ["Easy", "Medium", "Hard"]

        for difficulty in difficulties:
            tk.Radiobutton(self, text=difficulty,
                           variable=self.difficulty_var, value=difficulty).pack()

        self.start_button = tk.Button(
            self, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(
            self, text="Back", command=self.show_main_menu)
        self.back_button.pack(side="bottom")

        self.quit_button = tk.Button(self, text="Quit", command=self.quit_game)
        self.quit_button.pack(side="bottom")

    def start_game(self):
        print(f"Game started with difficulty: {self.difficulty_var.get()}")
        # Add your game start logic here

    def show_main_menu(self):
        self.destroy()  # Destroy the current frame (difficulty page)
        MainMenu(self.master).pack()  # Recreate and pack the main menu

    def quit_game(self):
        self.master.destroy()  # Close the application


# Create the main application window
root = tk.Tk()
root.title("Game Menu")

# Create the main menu frame
main_menu = MainMenu(master=root)

# Run the Tkinter event loop
root.mainloop()
