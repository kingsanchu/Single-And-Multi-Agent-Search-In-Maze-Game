import tkinter as tk

def start_game():
    # Add your game start logic here
    print("Game started!")

def quit_game():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Game Menu")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add items to the "File" menu
file_menu.add_command(label="Start Game", command=start_game)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=quit_game)

# Create a "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Add items to the "Help" menu
help_menu.add_command(label="About")

# Create buttons for quick actions
start_button = tk.Button(root, text="Start Game", command=start_game)
quit_button = tk.Button(root, text="Quit", command=quit_game)

# Place buttons in the window
start_button.pack(pady=10)
quit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
