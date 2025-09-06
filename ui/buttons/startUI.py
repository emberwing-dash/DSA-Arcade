import tkinter as tk
from tkinter import messagebox
import subprocess  # We'll use this to open chooseLvlUI.py

def start_app():
    # Open chooseLvlUI.py in a new window
    subprocess.Popen(["python", "chooseLvlUI.py"])
    root.destroy()  # Close startUI window

def quit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

root = tk.Tk()
root.title("Start UI")
root.geometry("300x200")

tk.Label(root, text="Welcome to the Game!", font=("Arial", 16)).pack(pady=20)

tk.Button(root, text="Start", width=15, height=2, command=start_app).pack(pady=10)
tk.Button(root, text="Quit", width=15, height=2, command=quit_app).pack(pady=10)

root.mainloop()
