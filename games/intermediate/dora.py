import pygame
import os

class Dora:
    def __init__(self, screen, asset_dir, pos=(100, 400)):
        self.screen = screen
        self.asset_dir = os.path.join(asset_dir, "dora")

        # Load idle (just 1.png)
        self.idle_img = pygame.image.load(os.path.join(self.asset_dir, "1.png")).convert_alpha()

        # Load walking frames (2,3,4)
        self.walk_frames = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join(self.asset_dir, f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (64, 64))  # resize if needed
            self.walk_frames.append(img)

        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 8  # lower = slower animation

        self.pos = list(pos)
        self.is_walking = False
        self.direction = "right"  # could add "left" later

    def update(self):
        if self.is_walking:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
        else:
            self.frame_index = 0  # reset to idle

    def draw(self):
        if self.is_walking:
            frame = self.walk_frames[self.frame_index]
        else:
            frame = self.idle_img
        self.screen.blit(frame, self.pos)

    def walk(self, direction="right"):
        self.is_walking = True
        self.direction = direction
        speed = 4
        if direction == "right":
            self.pos[0] += speed
        elif direction == "left":
            self.pos[0] -= speed

    def idle(self):
        self.is_walking = False
