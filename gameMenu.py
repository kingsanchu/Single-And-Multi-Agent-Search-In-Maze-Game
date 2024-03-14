import tkinter as tk
from subprocess import Popen
from agent import Agent


class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.root = root
        self.root.geometry("500x300")
        self.root.configure(bg="#f0f0f0")

    def create_widgets(self):
        self.start_button = tk.Button(
            self, text="Start Game", command=self.show_maze_size_diff_page)
        self.start_button.pack(side="top")
        self.start_button.pack(side="top", pady=20)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit_game)
        self.quit_button.pack(side="bottom")
        self.quit_button.pack(side="bottom", pady=20)

    def show_maze_size_diff_page(self):
        self.destroy()  # Destroy the current frame (main menu)
        MazeSizeAndDifficultyPage(self.master)  # Pass master to DifficultyPage

    def quit_game(self):
        self.master.destroy()  # Close the application


class MazeSizeAndDifficultyPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_maze_size = tk.Label(self, text="Select Maze Size:")
        self.label_maze_size.pack(pady=10)

        self.maze_size_var = tk.StringVar()
        self.maze_size_var.set("Small")  # Default maze size

        sizes = ["Small", "Medium", "Large"]

        for size in sizes:
            tk.Radiobutton(self, text=size, variable=self.maze_size_var,
                           value=size).pack()

        self.label_algorithm = tk.Label(self, text="Select Algorithm:")
        self.label_algorithm.pack(pady=10)

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("BFS")  # Default algorithm

        # Add AStar and Dijkstra algorithms
        algorithms = ["BFS", "AStar", "Dijkstra", "DFS"]

        for algorithm in algorithms:
            tk.Radiobutton(self, text=algorithm,
                           variable=self.algorithm_var, value=algorithm).pack()

        self.start_button = tk.Button(
            self, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(
            self, text="Back", command=self.show_main_menu)
        self.back_button.pack(side="bottom")
        self.quit_button = tk.Button(
            self, text="Quit", command=self.quit_game)
        self.quit_button.pack(side="bottom")

    def start_game(self):
        selected_maze_size = self.maze_size_var.get()
        selected_algorithm = self.algorithm_var.get()
        print(f"Selected maze size: {selected_maze_size}")
        print(f"Game started with algorithm: {selected_algorithm}")

        if not selected_algorithm or not selected_maze_size:
            print("Invalid algorithm selected!")

        else:
            # Add your logic here to start the game based on the selected maze size and algorithm
            if selected_algorithm == "AStar":
                print("Starting game with A* algorithm...")
            # Example: game.start_with_astar(agent)
            elif selected_algorithm == "DFS":
                print("Starting game with Depth-First Search algorithm...")

            # Example: game.start_with_dfs(agent)
            elif selected_algorithm == "BFS":
                print("Starting game with Breadth-First Search algorithm...")
            # Example: game.start_with_bfs(agent)
            elif selected_algorithm == "Dijkstra":
                print("Starting game with Dijkstra's algorithm...")

            Popen(["python", "main.py", "--algorithm", selected_algorithm, "--size", selected_maze_size])


    def show_main_menu(self):
        self.destroy()  # Destroy the current frame
        MainMenu(self.master).pack()  # Navigate back to the main menu

    def quit_game(self):
        self.master.destroy()  # Close the application


# Create the main application window
root = tk.Tk()
root.title("Game Menu")

# Create the main menu frame
main_menu = MainMenu(master=root)

# Run the Tkinter event loop
root.mainloop()
