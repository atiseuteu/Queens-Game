# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:26:05 2024

@author: SHRUTI-NIDHI
"""

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk 
from pygame import mixer
mixer.init()

def show_instructions():
    root = tk.Tk()
    root.title("How to Play?")

    # Set window size and disable resizing
    root.geometry("400x500")
    root.resizable(False, False)

    # Create a frame for instructions
    frame = tk.Frame(root, bg="#023047", padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    # Title label
    title = tk.Label(frame, text="How to play?", font=("Arial", 16, "bold"), bg="#023047", fg="white")
    title.pack(pady=10)

    # Instruction text
    instructions = (
        "• Choose a grid size.\n\n"
        "• Click on grid cells to fill them with your chosen colors.\n\n"
        "• Press the Submit button to solve the puzzle.\n\n"
        "• The AI will display the solution, showing where queens can be placed.\n\n"
        "• If no solution exists, you will be notified.\n\n"
    )
    label = tk.Label(frame, text=instructions, font=("Arial", 12), bg="#023047", fg="white", justify="left", wraplength=380)
    label.pack(pady=10)

    # Button to close the popup
    btn = tk.Button(frame, text="Ok, Let's play! →", command=root.destroy, bg="#8ecae6", fg="#023047", font=("Arial", 14, "bold"))
    btn.pack(pady=20)


def is_safe(board, row, col, queens_pos):
    for i in range(col):
        if queens_pos[i] == row:
            return False
        if abs(queens_pos[i] - row) == abs(i - col):
            if abs(queens_pos[i] - row) == 1:
                return False
    return True

def solve_nqueens_util(board, col, queens_pos, region_count, regions_used):
    if col >= len(board):
        return True
    for i in range(len(board)):
        region = board[i][col]
        if region not in regions_used and is_safe(board, i, col, queens_pos):
            queens_pos[col] = i
            regions_used.add(region)
            if solve_nqueens_util(board, col + 1, queens_pos, region_count, regions_used):
                return True
            queens_pos[col] = -1
            regions_used.remove(region)
    return False

def solve_nqueens(board):
    n = len(board)
    queens_pos = [-1] * n
    region_count = len(set(num for row in board for num in row))
    if solve_nqueens_util(board, 0, queens_pos, region_count, set()):
        return queens_pos
    else:
        return None

def get_valid_sizes():
    valid_sizes = list(range(4, 11))  # Allow sizes from 4 to 10
    return valid_sizes

def create_board_input():
    n = int(selected_size.get())

    board_window = tk.Toplevel(root)
    board_window.title("N-Queens Board Configuration")
    board_window.configure(bg="#155e75")
    board_window.attributes("-fullscreen",True)
    # Add a scrollable canvas for the board
    canvas = tk.Canvas(board_window, bg="#155E75")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(board_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    board_frame = tk.Frame(canvas, bg="#F0F0F0")
    canvas.create_window((0, 0), window=board_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    board_frame.bind("<Configure>", on_configure)

    board_buttons = []
    board_colors = [["#FFFFFF"] * n for _ in range(n)]
    selected_color = None

    def select_color(color):
        nonlocal selected_color
        selected_color = color
        mixer.music.load('F:/AI/putting-on-a-marker-lid-84616.mp3')
        mixer.music.play()

    def colorize_square(row, col):
        if selected_color:
            board_buttons[row][col].config(bg=selected_color)
            board_colors[row][col] = selected_color
            mixer.music.load('F:/AI/tap-notification-180637.mp3')
            mixer.music.play()
    # Color Selection Frame
    color_frame = tk.Frame(board_window, bg="#2E3440")
    color_frame.pack(pady=20)

    tk.Label(
        color_frame,
        text="Select a color for regions:",
        font=("georgia", 16, "bold"),
        fg="#F0F0F0",
        bg="#155E75",
    ).pack()

    for i in range(1, n + 1):
        color = f"#{(i * 70) % 256:02x}{(i * 120) % 256:02x}{(i * 170) % 256:02x}"
        tk.Button(
            color_frame,
            bg=color,
            width=4,
            height=2,
            command=lambda color=color: select_color(color),
            relief="groove",
            bd=2,
        ).pack(side="left", padx=5)

    # Board Buttons
    for i in range(n):
        row_buttons = []
        for j in range(n):
            button = tk.Button(
                board_frame,
                bg="#155E75",
                width=6,
                height=3,
                font=("georgia", 14),
                text="",
                relief="ridge",
                bd=1,
                command=lambda i=i, j=j: colorize_square(i, j),
            )
            button.grid(row=i, column=j, padx=3, pady=3)
            row_buttons.append(button)
        board_buttons.append(row_buttons)

    def submit_board():
        clear_queens()
        board = []
        color_to_zone = {}
        zone_counter = 1

        for i in range(n):
            row = []
            for j in range(n):
                color = board_colors[i][j]
                if color not in color_to_zone:
                    color_to_zone[color] = zone_counter
                    zone_counter += 1
                row.append(color_to_zone[color])
            board.append(row)

        queens_positions = solve_nqueens(board)
        if queens_positions is not None:
            for col, row in enumerate(queens_positions):
                board_buttons[row][col].config(
                    text="Q",
                    fg="BLACK",
                    font=("georgia", 14, "bold"),
                )
                mixer.music.load('F:/AI/preview (mp3cut.net).mp3')
                mixer.music.play()
        else:
            messagebox.showinfo("No Solution", "No solution exists for the current board configuration.")
            mixer.music.load('F:/AI/WhatsApp Audio 2024-11-22 at 13 (mp3cut.net).mp3')
            mixer.music.play()

    def clear_queens():
        for i in range(n):
            for j in range(n):
                board_buttons[i][j].config(text="", font=("Arial", 14))
        mixer.music.load('F:/AI/mixkit-fairy-glitter-867.wav')
        mixer.music.play()

    def exit_page():
        board_window.destroy()

    tk.Button(board_window, text="Submit", command=submit_board, width=20, height=2, relief="raised", bg="#8DF88D", fg="white", font=("georgia", 14, "bold")).pack(pady=10)
    tk.Button(board_window, text="Clear Queens", command=clear_queens, width=20, height=2, relief="raised", bg="#FFA6A6", fg="white", font=("georgia", 14, "bold")).pack(pady=10)
    tk.Button(board_window, text="Exit", command=exit_page, width=20, height=2, relief="raised", bg="#9D9DFF", fg="white", font=("georgia", 14, "bold")).pack(pady=10)

def main_menu():
    global root, selected_size

    root = tk.Tk()
    root.title("N-Queens Puzzle Solver")
    root.configure(bg="#155E75")
    root.attributes("-fullscreen",True)
    header_frame = tk.Frame(root, bg="#155e75")
    header_frame.pack(fill=tk.X)

        # Add an Image to the Header
    try:
            # Using Pillow for .jpg, .jpeg, etc.
            pil_image = Image.open("F:/AI/updated_image-removebg-preview.png")  # Adjust path
            pil_image = pil_image.resize((300, 300))  # Resize if necessary
            logo_image = ImageTk.PhotoImage(pil_image)

            # Add image to a Label widget
            image_label = tk.Label(header_frame, image=logo_image, bg="#155e75")
            image_label.image = logo_image  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)

    except Exception as e:
            print(f"Error loading image: {e}")

    valid_sizes = get_valid_sizes()

    tk.Label(root, text="N-Queens Puzzle Solver", font=("georgia", 34, "bold"), fg="#ECEFF4", bg="#155E75").pack(pady=20)
    tk.Label(root, text="Select the size of the board (N):", font=("georgia", 20), fg="#ECEFF4", bg="#155E75").pack(pady=10)

    selected_size = tk.StringVar(root)
    selected_size.set(str(valid_sizes[0]))

    size_menu = tk.OptionMenu(root, selected_size, *valid_sizes)
    size_menu.config(font=("Helvetica", 14), bg="#ECEFF4", fg="#3B4252")
    size_menu.pack(pady=5)
    
    # Add a button to show instructions
    tk.Button(
       root,
       text="How to Play?",
       command=show_instructions,
       width=20,
       height=2,
       relief="raised",
       bg="#FFFF87",
       fg="black",
       font=("georgia", 14, "bold")
    ).pack(pady=10)


    tk.Button(root, text="Start Game", command=create_board_input, width=20, height=2, relief="raised", bg="#8DF88D", fg="BLACK", font=("georgia", 14, "bold")).pack(pady=20)
    tk.Button(root, text="Exit", command=root.destroy, width=20, height=2, relief="raised", bg="#FFA6A6", fg="BLACK", font=("georgia", 14, "bold")).pack(pady=10)

    root.mainloop()
