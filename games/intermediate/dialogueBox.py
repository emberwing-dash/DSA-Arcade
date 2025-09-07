import pygame
import os
import sys

class DialogueBox:
    def __init__(self, screen, asset_dir="assets", font_size=24, typewriter=False, color=(0,0,0), speed=2, margin=20):
        """
        :param screen: Pygame screen
        :param asset_dir: Folder containing dial.png
        :param font_size: Font size
        :param typewriter: Use typewriting effect if True
        :param color: Text color for typewriter
        :param speed: Characters per frame for typewriter
        :param margin: Margin from bottom for typewriter text
        """
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", font_size)
        self.typewriter = typewriter
        self.color = color
        self.speed = speed
        self.margin = margin

        # Load dialogue box image if not using typewriter only
        self.box_img = None
        if not typewriter:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            asset_dir = os.path.join(base_dir, asset_dir)
            img_path = os.path.join(asset_dir, "dial.png")
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"❌ Could not find dialogue box image at {img_path}")

            self.box_img = pygame.image.load(img_path).convert_alpha()
            screen_width, screen_height = screen.get_size()
            self.box_img = pygame.transform.scale(self.box_img, (screen_width, screen_height // 3))
            self.box_rect = self.box_img.get_rect(midbottom=(screen_width // 2, screen_height))

        # Dialogue data
        self.dialogues = []
        self.current_index = 0
        self.active = False

        # Typewriter specific
        self.char_index = 0
        self.current_text = ""
        self.finished = False

    def set_dialogues(self, dialogues):
        self.dialogues = dialogues
        self.current_index = 0
        self.active = True if dialogues else False
        if self.typewriter:
            self.char_index = 0
            self.current_text = ""
            self.finished = False

    def update(self):
        """Update typewriter text if active."""
        if self.typewriter and self.active and not self.finished:
            text = self.dialogues[self.current_index]
            if self.char_index < len(text):
                self.char_index += self.speed
                self.current_text = text[:self.char_index]
            else:
                self.current_text = text

    def draw(self):
        """Draw dialogue box and/or typewriter text."""
        if not self.active:
            return

        if self.box_img:
            self.screen.blit(self.box_img, self.box_rect)

        if self.typewriter:
            text_surface = self.font.render(self.current_text, True, self.color)
            screen_width, screen_height = self.screen.get_size()
            text_rect = text_surface.get_rect(midbottom=(screen_width // 2, screen_height - self.margin))
            self.screen.blit(text_surface, text_rect)

    def next(self):
        """Advance to next dialogue."""
        if self.current_index < len(self.dialogues) - 1:
            self.current_index += 1
            if self.typewriter:
                self.char_index = 0
                self.current_text = ""
        else:
            self.active = False
            if self.typewriter:
                self.finished = True


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dialogue Box / Typewriter Test")

    # Use typewriter = True to enable typewriting effect
    dialogue = DialogueBox(screen, font_size=28, typewriter=True, speed=2)
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
