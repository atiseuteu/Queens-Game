# -- coding: utf-8 --
"""
Created on Wed Nov 20 10:32:19 2024

@author: SHRUTI-NIDHI
"""

import tkinter as tk
from tkinter import messagebox
import time
from PIL import Image, ImageTk 
from pygame import mixer
mixer.init()

# Fixed cell colors and section grid
CELL_COLORS = {
    1: "#FFA6A6",
    2: "#3EB1FE",
    3: "#FF9400",
    4: "#8DF88D",
    5: "#9D9DFF",
    6: "#FFFF87",
    7: "#C200FB",
    8: "#007B7A",
    9: "#D7263D", # Brown
    10: "#DFFF00", # Steel blue
    11: "#FFD700", # Lime green
    12: "#FFC0CB", # Pink
}

# Grids for different difficulty levels
EASY_GRID = [
   [1, 1, 2, 2, 2],
   [3, 2, 2, 2, 4],
   [3, 4, 4, 4, 4],
   [3, 4, 4, 5, 5],
   [3, 4, 5, 5, 5],
]
MEDIUM_GRID = [
    [1, 1, 2, 2, 2, 3, 3, 3],
    [1, 1, 2, 2, 2, 3, 3, 3],
    [4, 1, 2, 2, 2, 3, 3, 3],
    [4, 1, 5, 5, 5, 5, 3, 3],
    [4, 1, 5, 5, 5, 5, 6, 6],
    [4, 5, 5, 7, 7, 6, 6, 6],
    [4, 8, 7, 7, 7, 6, 6, 6],
    [8, 8, 8, 7, 7, 6, 6, 6],
]
HARD_GRID = [
    [1, 12, 12, 12, 12, 12, 12, 12, 12, 12, 6],
    [1, 1, 12, 12, 12, 12, 12, 9, 6, 6],
    [3, 1, 1, 4, 12, 12, 9, 9, 6, 5],
    [3, 3, 1, 4, 4, 12, 9, 8, 6, 5],
    [3, 3, 11, 11, 4, 12, 8, 8, 6, 5],
    [3, 3, 3, 11, 4, 12, 8, 7, 7, 5],
    [3, 3, 3, 11, 4, 12, 8, 7, 5, 5],
    [3, 3, 3, 11, 11, 12, 7, 7, 5, 5],
    [3, 3, 3, 3, 11, 12, 7, 5, 5, 5],
    [3, 3, 3, 3, 3, 5, 5, 5, 5, 5],
]

# Fixed positions for the solution for each difficulty level
EASY_QUEENS_POSITIONS = [2, 0, 3, 1, 4]
MEDIUM_QUEENS_POSITIONS = [
    [2, 0, 7, 5, 1, 4, 6, 3],
    [3, 0, 7, 5, 1, 4, 6, 2]
    ]
HARD_QUEENS_POSITIONS = [8, 0, 3, 7, 4, 9, 6, 2, 5, 1]


def show_instructions():
    root = tk.Tk()
    root.title("How to play?")

    # Set window size and disable resizing
    root.geometry("400x500")
    root.resizable(False, False)

    # Create a frame for instructions
    frame = tk.Frame(root, bg="#155e75", padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    # Title label
    title = tk.Label(frame, text="How to play?", font=("Arial", 16, "bold"), bg="#155e75", fg="white")
    title.pack(pady=10)

    # Instruction text
    instructions = (
        "• Single tap to place 'X' and tap again to place a queen 👑.\n\n"
        "• Use 'X' to mark cells where you think it can't have queen 👑 (optional step).\n\n"
        "• Each row has exactly one queen 👑.\n\n"
        "• Each column has exactly one queen 👑.\n\n"
        "• Each color (border region) has exactly one queen 👑.\n\n"
        "• No two queen 👑 can touch each other (not even diagonally).\n\n"
        "• You will see a message when you solve it; each move is validated automatically.\n\n"
        "Tip: Lookout for the hint button [✨] when available.\n\n"
        "Heads up! There is only one solution to each game... and only that will give you bragging rights. Good luck! ✌️"
    )
    label = tk.Label(frame, text=instructions, font=("Arial", 12), bg="#155e75", fg="white", justify="left", wraplength=380)
    label.pack(pady=10)

    # Button to close the popup
    btn = tk.Button(frame, text="Ok, Let's play! →", command=root.destroy, bg="#8ecae6", fg="#023047", font=("Arial", 14, "bold"))
    btn.pack(pady=20)
 



def create_board(grid, queens_positions):
    board = grid
    n = len(board)

    board_window = tk.Toplevel(root)
    board_window.title("Play N-Queens")
    board_window.config(bg="#155e75")

    board_buttons = []
    attempts = tk.IntVar(value=0)
    autoplay_active = tk.BooleanVar(value=False) 
    
    def toggle_autoplay():
       """Toggle autoplay mode on or off."""
       autoplay_active.set(not autoplay_active.get())
       if autoplay_active.get():
           autoplay_button.config(text="Autoplay: ON", bg="#4CAF50", fg="white")
           update_invalid_positions()  # Update positions when enabling autoplay
       else:
           autoplay_button.config(text="Autoplay: OFF", bg="#f44336", fg="white")
           # Clear invalid positions if autoplay is turned off
           for i in range(n):
               for j in range(n):
                   if board_buttons[i][j].cget('text') == 'X':
                       board_buttons[i][j].config(text='', relief="flat")
   
    def is_valid_placement(row, col):
        # Check if the column already has a queen
        for r in range(n):
            if board_buttons[r][col].cget('text') == 'Q' and r != row:
                return False

        # Check the row for duplicate queens
        for c in range(n):
            if board_buttons[row][c].cget('text') == 'Q' and c != col:
                return False

        # Check diagonals for conflicts (only nearest cells)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < n and 0 <= c < n and board_buttons[r][c].cget('text') == 'Q':
                return False

        # Check if the region already has a queen
        region = board[row][col]
        for r in range(n):
            for c in range(n):
                if board_buttons[r][c].cget('text') == 'Q' and board[r][c] == region and (r != row or c != col):
                    return False

        return True
    



    def update_invalid_positions():
        if not autoplay_active.get():
            return 
        for i in range(n):
            for j in range(n):
                if board_buttons[i][j].cget('text') == 'X':
                    board_buttons[i][j].config(text='', fg='white', font=('Arial', 8, 'bold'), relief="flat")

        # Mark invalid positions
        for col in range(n):
            for row in range(n):
                if board_buttons[row][col].cget('text') == '' and not is_valid_placement(row, col):
                    board_buttons[row][col].config(text='X', fg='white', font=('Arial', 8, 'bold'), relief="flat")
    def highlight_invalid(row, col):
        # Check if the position is invalid
        if board_buttons[row][col].cget('text') == 'X':
            # Save original background and foreground colors
            original_bg = board_buttons[row][col].cget('bg')
            original_fg = board_buttons[row][col].cget('fg')

            # Highlight the button in red with its queen
            board_buttons[row][col].config(bg='red', fg='white', text='Q')

            # Reset to its original state after 2 seconds
            board_buttons[row][col].after(2000, lambda: board_buttons[row][col].config(bg=original_bg, fg=original_fg, text='X'))

  
    def place_queen(row, col):
        # Toggle queen placement
        if board_buttons[row][col].cget('text') == 'Q':
            board_buttons[row][col].config(text='', relief="flat", bg=CELL_COLORS[board[row][col]])
        else:
            # Check if placing a queen is valid
            if is_valid_placement(row, col):
                board_buttons[row][col].config(text='Q', fg='black', font=('Arial', 8, 'bold'), relief="raised")
            else:
                mixer.music.load('F:/AI/WhatsApp Audio 2024-11-22 at 13 (mp3cut.net).mp3')
                mixer.music.play()
                
        update_invalid_positions()
    autoplay_button = tk.Button(
        board_window,
        text="Autoplay: OFF",
        bg="#f44336",
        fg="white",
        font=("Arial", 12, "bold"),
        command=toggle_autoplay
    )
    autoplay_button.grid(row=n, column=0, columnspan=n, pady=10)
    
    update_invalid_positions()

    def clear_board():
        for row_buttons in board_buttons:
            for button in row_buttons:
                button.config(text='', relief="flat", bg=CELL_COLORS[board[board_buttons.index(row_buttons)][row_buttons.index(button)]])
        update_invalid_positions()
        mixer.music.load('F:/AI/mixkit-fairy-glitter-867.wav')
        mixer.music.play()

    def validate_solution():
         user_solution = [-1] * n
         regions_used = set()

    # Collect the user's solution from the board
         for col in range(n):
             for row in range(n):
                 if board_buttons[row][col].cget('text') == 'Q':
                     if user_solution[col] != -1:
                         return False  # Multiple queens in the same column
                     user_solution[col] = row
                     region = grid[row][col]
                     if region in regions_used:
                         return False  # Same region used twice
                     regions_used.add(region)
                     break

    # Validate the solution
         if isinstance(queens_positions[0], list):  # Medium difficulty (multiple solutions)
              return user_solution in queens_positions  # Check if user solution matches any valid solution
         else:  # Easy or Hard difficulty (single solution)
             return user_solution == queens_positions  # Check if user solution matches the valid solution

     
    

   
            
    def submit_solution():
        """Check the solution and show an attractive result message."""
        attempts.set(attempts.get() + 1)
        if validate_solution():
            time_taken = int(time.time() - start_time)
            mixer.music.load('F:/AI/preview (mp3cut.net).mp3')
            mixer.music.play()
            win_message = tk.Toplevel(board_window)
            win_message.title("🎉 Congratulations!")
            win_message.geometry("400x200")
            win_message.config(bg="#f7f3e9")

            # Title Label
            tk.Label(win_message, text="🎉 You Win!", font=("Arial", 18, "bold"), bg="#f7f3e9", fg="#4CAF50").pack(pady=10)

            # Details
            tk.Label(
                win_message,
                text=f"You solved it in {attempts.get()} attempts and {time_taken} seconds!",
                font=("Arial", 14),
                bg="#f7f3e9",
                fg="#333"
            ).pack(pady=10)

            # Close Button
            tk.Button(
                win_message,
                text="Hooray! 🎊",
                font=("Arial", 14, "bold"),
                bg="#4CAF50",
                fg="white",
                command=lambda: (board_window.destroy(), win_message.destroy())
            ).pack(pady=20)

        else:
           
            try_again_message = tk.Toplevel(board_window)
            try_again_message.title("Try Again")
            try_again_message.geometry("400x150")
            try_again_message.config(bg="#ffe6e6")
            mixer.music.load('F:/AI/preview (1).mp3')
            mixer.music.play()

            # Title Label
            tk.Label(
                try_again_message,
                text="Oops! Try Again!",
                font=("Arial", 16, "bold"),
                bg="#ffe6e6",
                fg="#e63946"
            ).pack(pady=10)

            # Message
            tk.Label(
                try_again_message,
                text="Your solution is incorrect. Keep trying!",
                font=("Arial", 12),
                bg="#ffe6e6",
                fg="#333"
            ).pack(pady=10)
            
            tk.Button(
                try_again_message,
                text="Okay, I'll Try! 🙃",
                font=("Arial", 12, "bold"),
                bg="#e63946",
                fg="white",
                command=try_again_message.destroy
            ).pack(pady=10) 
            
            
    def back_to_main_menu():
        board_window.destroy()
    
    def give_hint():
     mixer.music.load('F:/AI/mixkit-clinking-coins-1993.wav')
     mixer.music.play()   
     try:
         # Determine if there are multiple solutions (Medium difficulty)
         if isinstance(queens_positions[0], list):  # List of solutions
             solutions = queens_positions
         else:  # Single solution (Easy or Hard)
             solutions = [queens_positions]

         # Highlight incorrect queen placements
         incorrect_positions = []
         for col in range(n):
             for row in range(n):
                 if board_buttons[row][col].cget('text') == 'Q':
                     # Check if this placement is valid in any solution
                     is_valid = any(solution[col] == row for solution in solutions)
                     if not is_valid:
                         incorrect_positions.append((row, col))
                         # Save the original background color
                         original_bg = board_buttons[row][col].cget('bg')
                         # Highlight incorrect positions in red
                         board_buttons[row][col].config(bg="red", fg="white")

                         # Reset the background color after 2 seconds
                         board_buttons[row][col].after(
                             2000, lambda r=row, c=col, orig_bg=original_bg: board_buttons[r][c].config(bg=orig_bg)
                         )

         # Display message if there are incorrect positions
         if incorrect_positions:
             # Remove any previous hint label if exists
             if hasattr(give_hint, 'hint_label'):
                 give_hint.hint_label.destroy()

             # Show the incorrect positions message
             incorrect_message = "You placed a queen in the wrong position!"
             give_hint.hint_label = tk.Label(
                 board_window, text=incorrect_message, font=('Arial', 10), fg="red", bg="#F0F0F0"
             )
             give_hint.hint_label.grid(row=n + 1, column=0, columnspan=2, pady=10)

             return

         # Track columns where queens are already placed
         placed_queens_columns = {
             col for col in range(n) if any(board_buttons[row][col].cget('text') == 'Q' for row in range(n))
         }

         # Filter solutions where the user’s placements are correct
         valid_solutions = []
         for solution in solutions:
             match = True
             for col in placed_queens_columns:
                 user_row = next(row for row in range(n) if board_buttons[row][col].cget('text') == 'Q')
                 if solution[col] != user_row:
                     match = False
                     break
             if match:
                 valid_solutions.append(solution)

         # Proceed with the hint if there are valid solutions
         if valid_solutions:
             # Find the next unfilled column
             for col in range(n):
                 if col not in placed_queens_columns:  # Check only unfilled columns
                     # Suggest the correct row for the next unfilled column in any valid solution
                     for solution in valid_solutions:
                         correct_row = solution[col]
                         board_buttons[correct_row][col].config(text='Q', fg='red', relief="raised")

                         # Remove any previous hint label if exists
                         if hasattr(give_hint, 'hint_label'):
                             give_hint.hint_label.destroy()

                         # Create a label to display the hint
                         hint_message = f"A queen can be placed in column {col + 1}, row {correct_row + 1}."
                         give_hint.hint_label = tk.Label(
                             board_window, text=hint_message, font=('Arial', 10), fg="blue", bg="#F0F0F0"
                         )
                         give_hint.hint_label.grid(row=n + 1, column=0, columnspan=2, pady=10)

                         update_invalid_positions()
                         return

         # If no valid solutions or no more unfilled columns, show "No more hints"
         if hasattr(give_hint, 'hint_label'):
             give_hint.hint_label.destroy()

         give_hint.hint_label = tk.Label(
             board_window, text="No more hints available.", font=('Arial', 10), fg="red", bg="#F0F0F0"
         )
         give_hint.hint_label.grid(row=n + 1, column=0, columnspan=2, pady=10)

     except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    board_frame = tk.Frame(board_window)
    board_frame.grid(row=0, column=0, padx=10, pady=10)

    for i in range(n):
        row_buttons = []
        for j in range(n):
            section_color = CELL_COLORS[board[i][j]]
            button = tk.Button(
                board_frame, bg=section_color, width=4, height=2,
                relief="flat", command=lambda i=i, j=j: place_queen(i, j)
            )
            button.grid(row=i, column=j, padx=2, pady=2)
            row_buttons.append(button)
        board_buttons.append(row_buttons)

    control_frame = tk.Frame(board_window, bg="#155e75")
    control_frame.grid(row=1, column=0, pady=10)

    tk.Button(control_frame, text="Submit Solution", command=submit_solution, width=20, height=2).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(control_frame, text="Hint", command=give_hint, width=20, height=2).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(control_frame, text="Clear Board", command=clear_board, width=20, height=2, bg="#FFff87", fg="black").grid(row=1, column=0, padx=5, pady=5)
    tk.Button(control_frame, text="Back to Main Menu", command=back_to_main_menu, width=20, height=2, bg="#ffa6a6", fg="black").grid(row=1, column=1, padx=5, pady=5)

    tk.Label(control_frame, text="Attempts:", bg="#155e75").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(control_frame, textvariable=attempts, bg="#155e75").grid(row=2, column=1, padx=5, pady=5)

    start_time = time.time()
    start_timer(board_window, start_time)

   
def start_timer(board_window, start_time):
    timer_label = tk.Label(board_window, text="Time: 0 seconds", font=('Arial', 10, 'bold'), bg="#155e75")
    timer_label.grid(row=2, column=0, columnspan=2)

    def update_timer():
        if board_window.winfo_exists():
            elapsed_time = int(time.time() - start_time)
            timer_label.config(text=f"Time: {elapsed_time} seconds")
            board_window.after(1000, update_timer)

    update_timer()


def start_game(grid, queens_positions):
    create_board(grid, queens_positions)

def main_menu():
    global root

    root = tk.Tk()
    root.title("Queens Puzzle Game")
    root.attributes("-fullscreen", True)
    root.config(bg="#155e75")

    main_frame = tk.Frame(root, bg="#155e75")
    main_frame.pack(padx=10, pady=10, expand=True)
    
    header_frame = tk.Frame(root, bg="#155e75")
    header_frame.pack(fill=tk.X)

        # Add an Image to the Header
    try:
    # Using Pillow for .jpg, .jpeg, etc.
        pil_image = Image.open("F:/AI/updated_image-removebg-preview.png")  # Adjust path
        pil_image = pil_image.resize((300, 300))  # Resize if necessary
        logo_image = ImageTk.PhotoImage(pil_image)
    
        # Add image to a Label widget and store the reference
        image_label = tk.Label(header_frame, image=logo_image, bg="#155e75")
        image_label.image = logo_image  # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)

    except Exception as e:
            print(f"Error loading image: {e}")

    nav_frame = tk.Frame(root, bg="#EA9AB2")
    nav_frame.pack(pady=20)
    nav_frame = tk.Frame(root, bg="#155E75")
    nav_frame.pack(pady=20)
    title_label = tk.Label(
        main_frame,
        text="Human Mode",
        font=('georgia', 42, 'bold'),
        bg="#155e75",
        fg="White"
    )
    title_label.pack(pady=20)

    description_label = tk.Label(
        main_frame,
        text="Place the queens on the board without attacking each other.",
        font=('georgia', 12),
        bg="#155e75",
        fg="white"
    )
    description_label.pack(pady=10)

    # Difficulty selection buttons
    def start_easy():
        create_board(EASY_GRID, EASY_QUEENS_POSITIONS)

    def start_medium():
        create_board(MEDIUM_GRID, MEDIUM_QUEENS_POSITIONS)

    def start_hard():
        create_board(HARD_GRID, HARD_QUEENS_POSITIONS)

    tk.Button(
        main_frame,
        text="Easy",
        command=start_easy,
        width=20,
        height=2,
        bg="#FFFF87",
        fg="black",
        font=('georgia', 12, 'bold')
    ).pack(pady=10)

    tk.Button(
        main_frame,
        text="Medium",
        command=start_medium,
        width=20,
        height=2,
        bg="#3EB1FE",
        fg="black",
        font=('georgia', 12, 'bold')
    ).pack(pady=10)

    tk.Button(
        main_frame,
        text="Hard",
        command=start_hard,
        width=20,
        height=2,
        bg="#FFA6A6",
        fg="black",
        font=('georgia', 12, 'bold')
    ).pack(pady=10)

    instructions_button = tk.Button(
        main_frame,
        text="Instructions",
        command=show_instructions,
        width=20,
        height=2,
        bg="#8DF88D",
        fg="black",
        font=('georgia', 12, 'bold')
    )
    instructions_button.pack(pady=5)

    exit_button = tk.Button(
        main_frame,
        text="Exit",
        command=root.destroy,
        width=20,
        height=2,
        bg="#9D9DFF",
        fg="black",
        font=('georgia', 12, 'bold')
    )
    exit_button.pack(pady=5)

    root.mainloop()