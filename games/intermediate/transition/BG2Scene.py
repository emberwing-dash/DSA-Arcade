import pygame
import os
import sys

# Dora animation class
class Dora:
    def __init__(self, screen, asset_dir, pos=(-300, 0)):
        self.screen = screen
        self.frames = []
        for i in range(3):
            path = os.path.join(asset_dir, f"tile{i:03}.png")
            if not os.path.exists(path):
                print(f"❌ File not found: {path}")
                sys.exit(1)
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            self.frames.append(pygame.transform.scale(img, (w*3, h*3)))
        self.current_frame = 0
        self.frame_delay = 15
        self.frame_counter = 0
        self.x, self.y = pos
        self.speed = 1
        self.final_y = self.screen.get_height() - self.frames[0].get_height()
        self.reached_center = False

    def update(self):
        screen_center_x = self.screen.get_width() // 2
        frame_w = self.frames[self.current_frame].get_width()
        target_x = screen_center_x - frame_w // 2
        if not self.reached_center:
            self.x = min(self.x + self.speed, target_x)
            self.reached_center = self.x == target_x
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay and self.current_frame < len(self.frames)-1:
                self.current_frame += 1
                self.frame_counter = 0
        else:
            self.current_frame = len(self.frames)-1
        self.y = self.final_y if self.reached_center else self.screen.get_height()//2 - self.frames[self.current_frame].get_height()//2

    def draw(self):
        self.screen.blit(self.frames[self.current_frame], (self.x, self.y))

# Typewriter dialogue
class TypewriterDialogue:
    def __init__(self, screen, font_size=28, color=(255,255,255), speed=0.2):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = color
        self.speed = speed
        self.dialogues = []
        self.current_index = 0
        self.char_index = 0.0
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
        surf = self.font.render(self.current_text, True, self.color)
        rect = surf.get_rect(midbottom=(screen_width//2, screen_height-40))
        self.screen.blit(surf, rect)

    def next(self):
        if self.current_index < len(self.dialogues)-1:
            self.current_index += 1
            self.char_index = 0.0
            self.current_text = ""
        else:
            self.active = False
            self.finished = True

# BG2Scene
class BG2Scene:
    def __init__(self, screen):
        self.screen = screen
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.bg_img = pygame.image.load(os.path.join(base_dir,"bg","bg2.jpg")).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
        self.dora = Dora(screen, os.path.join(base_dir,"dora","bg2"))
        self.dialogue = TypewriterDialogue(screen)
        self.dialogue.set_dialogues([
            "Dora: ¡Hola! We’re exploring the DS Forest.",
            "To reach the Coding Cave, we need to build Linked Lists!"
        ])
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT: self.running=False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: self.dialogue.next()
            self.dora.update()
            self.dialogue.update()
            self.screen.blit(self.bg_img,(0,0))
            self.dora.draw()
            self.dialogue.draw()
            pygame.display.flip()

            if self.dialogue.finished:
                self.running=False
                # Transition → BG3Scene
                from bg3 import BG3Scene
                bg3 = BG3Scene(self.screen)
                bg3.run()
