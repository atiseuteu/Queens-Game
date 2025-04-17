# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:26:08 2024

@author: SHRUTI-NIDHI
"""

import tkinter as tk
from tkinter import messagebox,ttk
import importlib
from PIL import Image, ImageTk 
from pygame import mixer
mixer.init()

# Helper to dynamically load functions from files
def import_module_function(module_name, function_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, function_name)
    except (ImportError, AttributeError):
        messagebox.showerror("Error", f"Unable to load {function_name} from {module_name}")
        return None

def run_queens_solver():
    """Call the QueensSolver logic."""
    try:
        main_menu = import_module_function("solver", "main_menu")
        if main_menu:
            main_menu()  # Call the main_menu function in QueenGame_1.py
    except Exception as e:
        messagebox.showerror("Error", f"Unable to start the game: {e}")
   

def run_board_game():
    """Launch the Custom Board Game."""
    try:
        main_menu = import_module_function("QueenGame_1", "main_menu")
        if main_menu:
            main_menu()  # Call the main_menu function in QueenGame_1.py
    except Exception as e:
        messagebox.showerror("Error", f"Unable to start the game: {e}")

def clear_frame(frame):
    """
    Clears all widgets from the given frame.
    
    Parameters:
    frame (tk.Frame): The frame whose child widgets need to be cleared.
    """
    for widget in frame.winfo_children():
        widget.destroy()



def on_exit():
    """Prompt user before exiting."""
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.quit()  # Stop the main loop
        root.destroy()  # Destroy the root window


# Main Application


mixer.music.load('F:/AI/preview (mp3cut.net) (1).mp3')
mixer.music.play()
root = tk.Tk()
root.title("Queens")
root.attributes("-fullscreen",True)
root.update_idletasks()  # Ensures all widgets are rendered
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
root.minsize(600, 500)
root.config(bg="#155e75")

# Header
header_frame = tk.Frame(root, bg="#155E75")
header_frame.pack(fill=tk.X)


# Navigation Buttons
   # Header Frame
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

    # Navigation Frame
nav_frame = tk.Frame(root, bg="#EA9AB2")
nav_frame.pack(pady=20)
nav_frame = tk.Frame(root, bg="#155E75")
nav_frame.pack(pady=20)

style = ttk.Style()
style.theme_use("clam")  # Use a theme that supports customizations

# Configure the style for the button
style.configure(
    "Custom.TButton",
    font=("georgia", 28,'bold'),
    background="#ffa6a6",  # Background color
    foreground="white",    # Text color
    borderwidth=1
)

# Map the hover (active) background color
style.map(
    "Custom.TButton",
    background=[("active", "#FFA6A6")],  # Background when hovered
    foreground=[("active", "white")]    # Text color when hovered
)


solver_button = ttk.Button(nav_frame,style = 'Custom.TButton', text="Smart Solver: AI at Work", command=run_queens_solver)
solver_button.grid(row=0, column=0, padx=20, pady=30)

game_button = ttk.Button(nav_frame,style = 'Custom.TButton', text="Challenge Yourself: Human Mode", command=run_board_game)
game_button.grid(row=1, column=0, padx=20, pady=30)

exit_button = ttk.Button(nav_frame,style = 'Custom.TButton', text="Exit", command=on_exit)
exit_button.grid(row=2, column=0, padx=20, pady=30)

# Main Frame


# Tooltips (Optional)
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget, bg="#155E75", padx=5, pady=5)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    tooltip.withdraw()
    
    label = tk.Label(tooltip, text=text, fg="#155E75", bg="White", font=("georgia", 10,'bold'))
    label.pack()
    
    def show_tooltip(event):
        x, y = widget.winfo_pointerxy()
        tooltip.wm_geometry(f"+{x+10}+{y+10}")
        tooltip.deiconify()
    
    def hide_tooltip(event):
        tooltip.withdraw()
    
    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

create_tooltip(solver_button, "Start the Queens Solver Game")
create_tooltip(game_button, "Launch the Custom Board Game")
create_tooltip(exit_button, "Exit the Application")

# Run the Application
root.mainloop()
#root.protocol("WM_DELETE_WINDOW", on_exit)
