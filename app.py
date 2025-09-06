import tkinter as tk
from tkinter import messagebox
from ui.editor import CodeEditorUI

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamified Code Editor")
        self.root.geometry("900x700")

        self.editor_app = None  # Will hold the CodeEditorUI instance
        self.show_start_ui()

    # ---------------- Start UI -----------------
    def show_start_ui(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to the Game!", font=("Arial", 20)).pack(pady=50)

        tk.Button(self.root, text="Start", width=20, height=2, command=self.show_choose_level_ui).pack(pady=20)
        tk.Button(self.root, text="Quit", width=20, height=2, command=self.root.quit).pack(pady=10)

    # ---------------- Choose Level UI -----------------
    def show_choose_level_ui(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Choose Level", font=("Arial", 20)).pack(pady=30)

        tk.Button(self.root, text="Beginner", width=20, height=2, command=lambda: self.launch_editor("Beginner")).pack(pady=5)
        tk.Button(self.root, text="Intermediate", width=20, height=2, command=lambda: self.launch_editor("Intermediate")).pack(pady=5)
        tk.Button(self.root, text="Advanced", width=20, height=2, command=lambda: self.launch_editor("Advanced")).pack(pady=5)
        tk.Button(self.root, text="Back", width=20, height=2, command=self.show_start_ui).pack(pady=20)

    # ---------------- Launch Editor -----------------
    def launch_editor(self, level):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Level: {level}", font=("Arial", 16)).pack(pady=5)

        # Launch the code editor
        self.editor_app = CodeEditorUI(self.root)

        # Optional: Print last output button
        def print_last_output():
            output = self.editor_app.get_last_output()
            print(f"=== Last Terminal Output ({level}) ===")
            print(output)
            print("============================")

        tk.Button(self.root, text="Print Last Output", command=print_last_output).pack(pady=5)
