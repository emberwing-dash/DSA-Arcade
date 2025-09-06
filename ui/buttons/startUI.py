import pygame
import sys
import os
import subprocess

pygame.init()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHOOSELVL_PATH = os.path.join(BASE_DIR, "chooseLvlUI.py")

# Window setup
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Start UI")
font = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Button class
class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        label = font.render(self.text, True, BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Actions
def start_app():
    if not os.path.exists(CHOOSELVL_PATH):
        print(f"⚠️ Could not find {CHOOSELVL_PATH}")
        return
    # Run chooseLvlUI.py from the same folder
    subprocess.Popen([sys.executable, CHOOSELVL_PATH], cwd=BASE_DIR)
    pygame.quit()
    sys.exit()

def quit_app():
    pygame.quit()
    sys.exit()

# Buttons
start_button = Button("Start", 125, 100, 150, 50, start_app)
quit_button = Button("Quit", 125, 180, 150, 50, quit_app)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    start_button.draw(screen)
    quit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_clicked(event.pos):
                start_button.action()
            elif quit_button.is_clicked(event.pos):
                quit_button.action()

    pygame.display.flip()

pygame.quit()
