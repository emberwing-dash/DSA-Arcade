import pygame
import sys
import os
import threading
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
                # run callback in a separate thread to allow Tkinter window
                threading.Thread(target=self.callback).start()

# ------------------- App Class -------------------
class App:
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700

    START_SIZE = (140, 50)
    LEVEL_SIZE = (220, 80)
    BACK_SIZE = (180, 60)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Gamified Code Editor")
        self.clock = pygame.time.Clock()

        self.images = {}
        self.load_images()
        self.buttons = []

        self.show_start_ui()
        self.run()

    # ---------------- Load Images -----------------
    def load_images(self):
        base = os.path.join(os.path.dirname(__file__), "ui", "buttons", "assets")

        def load(name, size):
            path = os.path.join(base, f"{name}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, size)
                return img
            except Exception as e:
                print(f"Could not load {name}: {e}")
                return None

        self.images["start"] = load("start", self.START_SIZE)
        self.images["quit"] = load("quit", self.START_SIZE)
        self.images["beginner"] = load("beginner", self.LEVEL_SIZE)
        self.images["intermediate"] = load("intermediate", self.LEVEL_SIZE)
        self.images["advanced"] = load("advanced", self.LEVEL_SIZE)
        self.images["back"] = load("back", self.BACK_SIZE)

    # ---------------- UI States -----------------
    def show_start_ui(self):
        self.buttons = []
        x = (self.SCREEN_WIDTH - self.START_SIZE[0]) // 2
        y = self.SCREEN_HEIGHT // 2 - 50
        self.buttons.append(ImageButton(self.images["start"], x, y, self.show_choose_level_ui))
        self.buttons.append(ImageButton(self.images["quit"], x, y + self.START_SIZE[1] + 20, self.quit_game))

    def show_choose_level_ui(self):
        self.buttons = []
        x = (self.SCREEN_WIDTH - self.LEVEL_SIZE[0]) // 2
        start_y = self.SCREEN_HEIGHT // 2 - (self.LEVEL_SIZE[1]*3 + 30) // 2

        # Level buttons open Tkinter editor
        self.buttons.append(ImageButton(self.images["beginner"], x, start_y, lambda: self.launch_editor("Beginner")))
        self.buttons.append(ImageButton(self.images["intermediate"], x, start_y + self.LEVEL_SIZE[1] + 15, lambda: self.launch_editor("Intermediate")))
        self.buttons.append(ImageButton(self.images["advanced"], x, start_y + (self.LEVEL_SIZE[1] + 15)*2, lambda: self.launch_editor("Advanced")))

        # Back button bottom-right
        back_x = self.SCREEN_WIDTH - self.BACK_SIZE[0] - 20
        back_y = self.SCREEN_HEIGHT - self.BACK_SIZE[1] - 20
        self.buttons.append(ImageButton(self.images["back"], back_x, back_y, self.show_start_ui))

    # ---------------- Launch Tkinter Editor -----------------
    def launch_editor(self, level):
        def run_editor():
            editor_root = tk.Tk()
            editor_root.title(f"{level} Code Editor")
            editor_root.geometry("900x700")
            app = CodeEditorUI(editor_root)
            editor_root.mainloop()

        threading.Thread(target=run_editor).start()

    # ---------------- Quit -----------------
    def quit_game(self):
        pygame.quit()
        sys.exit()

    # ---------------- Main Loop -----------------
    def run(self):
        while True:
            self.screen.fill((30, 30, 30))  # dark background
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                for btn in self.buttons:
                    btn.handle_event(event)

            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

# ------------------- Run App -------------------
if __name__ == "__main__":
    App()
