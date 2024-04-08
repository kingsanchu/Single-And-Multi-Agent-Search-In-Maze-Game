import argparse
import tkinter as tk
from window import Window

'''This file calls Tkinter related with the choosen algorithm and board size'''

if __name__ == '__main__':
    # Create ArgumentParser object
    parser = argparse.ArgumentParser()
    # Add arguments
    parser.add_argument('--algorithm', help='Set algorithm')
    parser.add_argument('--size', help='Set maze size')
    # Parse the command-line arguments
    args = parser.parse_args()

    print(args.size)

    # Access the arguments
    if args.algorithm and args.size:
        root = tk.Tk()
        pacman = Window(root, args.algorithm, args.size)
        pacman.run()
    else:
        print("Algorithm not found.")
