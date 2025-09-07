import pygame
import os
import sys


class TypewriterDialogue:
    def __init__(self, screen, font_size=24, color=(255, 255, 255), speed=3, margin=20):
        """
        :param screen: Pygame screen
        :param font_size: Text font size
        :param color: Text color
        :param speed: Characters per tick
        :param margin: Margin from bottom of screen
        """
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.speed = speed
        self.margin = margin

        self.dialogues = []
        self.current_index = 0
        self.current_text = ""
        self.char_index = 0
        self.active = False
        self.finished = False

    def set_dialogues(self, dialogues):
        """Set list of dialogue strings."""
        self.dialogues = dialogues
        self.current_index = 0
        self.current_text = ""
        self.char_index = 0
        self.active = True
        self.finished = False

    def update(self):
        """Update the typing effect each frame."""
        if not self.active or self.finished:
            return

        text = self.dialogues[self.current_index]
        if self.char_index < len(text):
            self.char_index += self.speed
            self.current_text = text[:self.char_index]
        else:
            # Finished current dialogue, move to next after delay
            self.current_text = text
            # Wait for a short delay (can be done outside or with event)

    def draw(self):
        """Draw the text at bottom of the screen."""
        if not self.active or self.finished:
            return

        text_surface = self.font.render(self.current_text, True, self.color)
        screen_width, screen_height = self.screen.get_size()
        text_rect = text_surface.get_rect(midbottom=(screen_width // 2, screen_height - self.margin))
        self.screen.blit(text_surface, text_rect)

    def next(self):
        """Move to next dialogue immediately."""
        if self.current_index < len(self.dialogues) - 1:
            self.current_index += 1
            self.char_index = 0
            self.current_text = ""
        else:
            self.active = False
            self.finished = True


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Typewriter Dialogue Test")

    dialogue = TypewriterDialogue(screen, font_size=28, speed=2)
    dialogue.set_dialogues([
        "Dora: ¡Hola! We’re exploring the DS Forest.",
        "To reach the Coding Cave, we need to build Linked Lists!"
    ])

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dialogue.next()

        dialogue.update()
        screen.fill((0, 0, 0))
        dialogue.draw()
        pygame.display.flip()

    pygame.quit()
