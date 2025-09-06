import tkinter as tk
from tkinter import messagebox
import subprocess

def open_start_ui():
    # Go back to startUI
    subprocess.Popen(["python", "startUI.py"])
    root.destroy()

def level_selected(level):
    messagebox.showinfo("Level Selected", f"You selected: {level}")

root = tk.Tk()
root.title("Choose Level")
root.geometry("300x250")

tk.Label(root, text="Choose Level", font=("Arial", 16)).pack(pady=20)

tk.Button(root, text="Beginner", width=20, height=2, command=lambda: level_selected("Beginner")).pack(pady=5)
tk.Button(root, text="Intermediate", width=20, height=2, command=lambda: level_selected("Intermediate")).pack(pady=5)
tk.Button(root, text="Advanced", width=20, height=2, command=lambda: level_selected("Advanced")).pack(pady=5)
tk.Button(root, text="Back", width=20, height=2, command=open_start_ui).pack(pady=20)

root.mainloop()
