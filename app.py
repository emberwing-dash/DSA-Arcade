import pygame
import sys
import os
import threading
import subprocess
import tkinter as tk
from ui.editor import CodeEditorUI


# ------------------- Button Class -------------------
class ImageButton:
    def __init__(self, image, x, y, callback):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                threading.Thread(target=self.callback).start()


# ------------------- App Class -------------------
class App:
    START_SIZE = (140, 50)
    LEVEL_SIZE = (220, 80)
    BACK_SIZE = (180, 60)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700), pygame.RESIZABLE)
        pygame.display.set_caption("Gamified Code Editor")
        self.clock = pygame.time.Clock()

        self.images = {}
        self.logo_original = None
        self.logo = None
        self.load_images()
        self.buttons = []

        self.show_start_ui()
        self.run()

    # ---------------- Load Images -----------------
    def load_images(self):
        base_buttons = os.path.join(os.path.dirname(__file__), "ui", "buttons", "assets")
        base_design = os.path.join(os.path.dirname(__file__), "ui", "design")

        def load(path, size=None):
            abs_path = os.path.abspath(path)
            print(f"🔍 Loading image from: {abs_path}")
            if not os.path.exists(abs_path):
                print(f"❌ File does not exist: {abs_path}")
                return None
            try:
                img = pygame.image.load(abs_path).convert_alpha()
                if size:
                    img = pygame.transform.smoothscale(img, size)
                return img
            except Exception as e:
                print(f"⚠️ Could not load image {abs_path}: {e}")
                return None

        # Buttons
        self.images["start"] = load(os.path.join(base_buttons, "start.png"), self.START_SIZE)
        self.images["quit"] = load(os.path.join(base_buttons, "quit.png"), self.START_SIZE)
        self.images["beginner"] = load(os.path.join(base_buttons, "beginner.png"), self.LEVEL_SIZE)
        self.images["intermediate"] = load(os.path.join(base_buttons, "intermediate.png"), self.LEVEL_SIZE)
        self.images["advanced"] = load(os.path.join(base_buttons, "advanced.png"), self.LEVEL_SIZE)
        self.images["back"] = load(os.path.join(base_buttons, "back.png"), self.BACK_SIZE)

        # Logo
        logo_path = os.path.join(base_design, "DSA_ARCADE.png")
        self.logo_original = load(logo_path)
        if self.logo_original is None:
            print("⚠️ Logo not found.")
        self.logo = self.logo_original

    # ---------------- UI States -----------------
    def show_start_ui(self):
        self.buttons = []
        width = self.screen.get_width()
        height = self.screen.get_height()
        x = (width - self.START_SIZE[0]) // 2
        y = height // 2
        self.buttons.append(ImageButton(self.images["start"], x, y + 100, self.show_choose_level_ui))
        self.buttons.append(ImageButton(self.images["quit"], x, y + self.START_SIZE[1] + 150, self.quit_game))

    def show_choose_level_ui(self):
        self.buttons = []
        width = self.screen.get_width()
        height = self.screen.get_height()
        x = (width - self.LEVEL_SIZE[0]) // 2
        start_y = height // 2 - (self.LEVEL_SIZE[1] * 3 + 30) // 2

        # Beginner button launches appleFall.py
        self.buttons.append(ImageButton(self.images["beginner"], x, start_y, self.launch_apple_fall))

        # Intermediate button launches bg1.py
        self.buttons.append(ImageButton(
            self.images["intermediate"],
            x,
            start_y + self.LEVEL_SIZE[1] + 15,
            self.launch_bg1
        ))

        # Advanced button launches BOTH editor and pacman game
        def open_advanced():
            self.launch_editor("Advanced")
            self.launch_pacman()

        self.buttons.append(ImageButton(self.images["advanced"], x, start_y + (self.LEVEL_SIZE[1] + 15) * 2,
                                        open_advanced))

        back_x = width - self.BACK_SIZE[0] - 20
        back_y = height - self.BACK_SIZE[1] - 20
        self.buttons.append(ImageButton(self.images["back"], back_x, back_y, self.show_start_ui))

    # ---------------- Launch Scripts / Apps -----------------
    def launch_apple_fall(self):
        apple_fall_path = os.path.join(os.path.dirname(__file__), "games", "beginner", "transitions", "appleFall.py")
        if os.path.exists(apple_fall_path):
            subprocess.Popen(["python", apple_fall_path])
            pygame.quit()
            sys.exit()
        else:
            print(f"❌ appleFall.py not found at {apple_fall_path}")

    def launch_bg1(self):
        bg1_path = os.path.join(os.path.dirname(__file__), "games", "intermediate", "transition", "bg1.py")
        if os.path.exists(bg1_path):
            subprocess.Popen(["python", bg1_path])
            pygame.quit()
            sys.exit()
        else:
            print(f"❌ bg1.py not found at {bg1_path}")

    def launch_editor(self, level):
        def run_editor():
            root = tk.Tk()
            root.title(f"{level} Editor")
            root.geometry("900x700")
            CodeEditorUI(root)
            root.mainloop()

        threading.Thread(target=run_editor).start()

    def launch_pacman(self):
        pacman_path = os.path.join(os.path.dirname(__file__), "games", "advanced", "pacman.py")
        if os.path.exists(pacman_path):
            subprocess.Popen(["python", pacman_path])
        else:
            print(f"❌ pacman.py not found at {pacman_path}")

    # ---------------- Utility -----------------
    def quit_game(self):
        pygame.quit()
        sys.exit()

    # ---------------- Main Loop -----------------
    def run(self):
        while True:
            self.screen.fill((30, 30, 30))
            width = self.screen.get_width()
            height = self.screen.get_height()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                for btn in self.buttons:
                    btn.handle_event(event)

            # Draw logo dynamically scaled
            if self.logo_original:
                max_width = int(width * 0.5)
                orig_w, orig_h = self.logo_original.get_size()
                scale_ratio = max_width / orig_w
                logo_w = max_width
                logo_h = int(orig_h * scale_ratio)
                self.logo = pygame.transform.smoothscale(self.logo_original, (logo_w, logo_h))
                logo_x = (width - logo_w) // 2
                logo_y = 50
                self.screen.blit(self.logo, (logo_x, logo_y))

            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    App()
