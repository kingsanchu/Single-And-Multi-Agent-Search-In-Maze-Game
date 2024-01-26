import tkinter as tk


def start_game():
    # Destroy the main menu
    root.destroy()

    # Create a new window for difficulty selection
    difficulty_window = tk.Tk()
    difficulty_window.title("Difficulty Selection")

    # Label for difficulty selection
    label = tk.Label(difficulty_window, text="Select Difficulty:")
    label.pack(pady=10)

    # Radio buttons for difficulty options
    difficulty_var = tk.StringVar()
    difficulty_var.set("Easy")  # Default difficulty

    difficulties = ["Easy", "Medium", "Hard"]

    for difficulty in difficulties:
        tk.Radiobutton(difficulty_window, text=difficulty,
                       variable=difficulty_var, value=difficulty).pack()

    # Button to start the game with the selected difficulty
    start_button = tk.Button(difficulty_window, text="Start Game",
                             command=lambda: start_game_logic(difficulty_var.get()))
    start_button.pack(pady=10)


def start_game_logic(difficulty):
    print(f"Game started with difficulty: {difficulty}")
    # Add your game start logic here


# Create the main menu
root = tk.Tk()
root.title("Game Menu")

# Button to start the game
start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=50)

# Run the Tkinter event loop
root.mainloop()
