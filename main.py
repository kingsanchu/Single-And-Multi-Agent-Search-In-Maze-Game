import argparse
import tkinter as tk
from window import Window

if __name__ == '__main__':
    # Create ArgumentParser object
    parser = argparse.ArgumentParser()
    # Add arguments
    parser.add_argument('--algorithm', help='Set algorithm')
    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the arguments
    if args.algorithm:
        root = tk.Tk()
        pacman = Window(root)
        pacman.set_algorithm(args.algorithm)
        pacman.run()
    else:
        print("Algorithm not found 898.")
