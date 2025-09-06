import pygame
import sys
import os
import subprocess

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
START_UI_PATH = os.path.join(BASE_DIR, "startUI.py")

# Init Pygame
pygame.init()
WIDTH, HEIGHT = 250, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Choose Level")
font = pygame.font.SysFont("Arial", 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Helper to load images
def load_image(filename, size=(200, 60)):
    path = os.path.join(ASSET_DIR, filename)
    if not os.path.exists(path):
        print(f"⚠️ Missing: {path}")
        return None
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# Buttons
beginner_btn = load_image("beginnerButton.png")
intermediate_btn = load_image("IntermediateButton.png")
advanced_btn = load_image("AdvancedButton.png")
back_btn = load_image("backButton.png")

# Rect positions
button_rects = {
    "Beginner": pygame.Rect(WIDTH//2 - 100, 150, 200, 60),
    "Intermediate": pygame.Rect(WIDTH//2 - 100, 230, 200, 60),
    "Advanced": pygame.Rect(WIDTH//2 - 100, 310, 200, 60),
    "Back": pygame.Rect(WIDTH//2 - 100, 400, 200, 60),
}

def open_start_ui():
    subprocess.Popen(["python", START_UI_PATH])
    pygame.quit()
    sys.exit()

def level_selected(level):
    print(f"You selected: {level}")  # shows in terminal
    # If you want popup like Tkinter, you can use pygame message box

def draw_button(img, rect, fallback_text):
    if img:
        screen.blit(img, rect.topleft)
    else:
        pygame.draw.rect(screen, (180, 180, 180), rect)
        text = font.render(fallback_text, True, BLACK)
        screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

# Main Loop
running = True
while running:
    screen.fill(WHITE)

    # Title
    title = font.render("Choose Level", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

    # Draw Buttons
    draw_button(beginner_btn, button_rects["Beginner"], "Beginner")
    draw_button(intermediate_btn, button_rects["Intermediate"], "Intermediate")
    draw_button(advanced_btn, button_rects["Advanced"], "Advanced")
    draw_button(back_btn, button_rects["Back"], "Back")

    pygame.display.flip()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, rect in button_rects.items():
                if rect.collidepoint(pos):
                    if name == "Back":
                        open_start_ui()
                    else:
                        level_selected(name)

pygame.quit()
sys.exit()
