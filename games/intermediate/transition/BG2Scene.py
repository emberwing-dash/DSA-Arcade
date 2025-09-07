import pygame
import os
import sys
from bg3 import BG3Scene   # import BG3Scene for transition


# ---------------- Dora Animation ----------------
class Dora:
    def __init__(self, screen, asset_dir, pos=(-300, 0)):
        self.screen = screen
        self.asset_dir = asset_dir  # points to transition/dora/bg2 for tile000 -> tile002
        self.frames = []

        # Load frames tile000 -> tile002
        for i in range(0, 3):
            filename = f"tile{i:03}.png"
            path = os.path.join(self.asset_dir, filename)
            if not os.path.exists(path):
                print(f"❌ File not found: {path}")
                sys.exit(1)
            img = pygame.image.load(path).convert_alpha()
            # Scale 3x
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w * 3, h * 3))
            self.frames.append(img)

        self.total_frames = len(self.frames)
        self.current_frame = 0
        self.frame_delay = 15
        self.frame_counter = 0
        self.x, self.y = pos
        self.speed = 1  # horizontal slide speed
        self.final_y = self.screen.get_height() - self.frames[0].get_height()  # bottom

        self.reached_center = False

    def update(self):
        # Horizontal slide until center
        screen_center_x = self.screen.get_width() // 2
        frame_w = self.frames[self.current_frame].get_width()
        target_x = screen_center_x - frame_w // 2

        if not self.reached_center:
            if self.x + self.speed < target_x:
                self.x += self.speed
            else:
                self.x = target_x
                self.reached_center = True

        # Frame animation
        if not self.reached_center:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                if self.current_frame < self.total_frames - 1:
                    self.current_frame += 1
        else:
            self.current_frame = self.total_frames - 1  # freeze last frame

        # y position
        self.y = (
            self.final_y
            if self.reached_center
            else self.screen.get_height() // 2 - self.frames[self.current_frame].get_height() // 2
        )

    def draw(self):
        self.screen.blit(self.frames[self.current_frame], (self.x, self.y))


# ---------------- Typewriter Dialogue ----------------
class TypewriterDialogue:
    def __init__(self, screen, font_size=24, color=(255, 255, 255), speed=0.2, margin=20):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.speed = speed  # can be float now
        self.margin = margin

        self.dialogues = []
        self.current_index = 0
        self.char_index = 0.0   # float counter
        self.current_text = ""
        self.active = False
        self.finished = False

    def set_dialogues(self, dialogues):
        self.dialogues = dialogues
        self.current_index = 0
        self.char_index = 0.0
        self.current_text = ""
        self.active = True
        self.finished = False

    def update(self):
        if not self.active or self.finished:
            return

        text = self.dialogues[self.current_index]
        if self.char_index < len(text):
            self.char_index += self.speed
            self.current_text = text[:int(self.char_index)]
        else:
            self.current_text = text

    def draw(self):
        if not self.active:
            return
        screen_width, screen_height = self.screen.get_size()
        text_surface = self.font.render(self.current_text, True, self.color)
        text_rect = text_surface.get_rect(midbottom=(screen_width // 2, screen_height - self.margin))
        self.screen.blit(text_surface, text_rect)

    def next(self):
        if self.current_index < len(self.dialogues) - 1:
            self.current_index += 1
            self.char_index = 0.0
            self.current_text = ""
        else:
            self.active = False
            self.finished = True


# ---------------- BG2 Scene ----------------
class BG2Scene:
    def __init__(self, screen):
        self.screen = screen
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load BG2 background
        bg_path = os.path.join(base_dir, "bg", "bg2.jpg")
        if not os.path.exists(bg_path):
            print(f"❌ File not found: {bg_path}")
            sys.exit(1)
        self.bg_img = pygame.image.load(bg_path).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())

        # Dora animation
        dora_dir = os.path.join(base_dir, "dora", "bg2")
        self.dora = Dora(screen, asset_dir=dora_dir)

        # Typewriter dialogue
        self.dialogue = TypewriterDialogue(screen, font_size=28, speed=0.2)
        self.dialogue.set_dialogues([
            "Dora: ¡Hola! We’re exploring the DS Forest.",
            "To reach the Coding Cave, we need to build Linked Lists!"
        ])

        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dialogue.next()  # skip to next dialogue

            # Update Dora and typewriter
            self.dora.update()
            self.dialogue.update()

            # Draw everything
            self.screen.blit(self.bg_img, (0, 0))
            self.dora.draw()
            self.dialogue.draw()

            pygame.display.flip()

            # 🚀 Transition check
            if self.dialogue.finished:
                self.running = False
                # Call BG3 scene after dialogues end
                bg3 = BG3Scene(self.screen)
                bg3.fade_in_out(10)


# ---------------- Run BG2Scene ----------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("BG2 Scene Animation Typewriter")

    scene = BG2Scene(screen)
    scene.run()

    pygame.quit()
