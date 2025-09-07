import pygame
import os
import sys

class MapScene:
    def __init__(self, screen):
        self.screen = screen
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(base_dir, "assets", "mappy")

        # Load frames tile000 -> tile015
        self.frames = []
        for i in range(0, 16):
            filename = f"tile{i:03}.png"
            path = os.path.join(asset_dir, filename)
            if not os.path.exists(path):
                print(f"❌ File not found: {path}")
                sys.exit(1)
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w*2, h*2))  # scale up
            self.frames.append(img)

        self.total_frames = len(self.frames)
        self.current_frame = 0
        self.frame_delay = 8   # controls speed of animation
        self.frame_counter = 0
        self.running = True

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.total_frames

    def draw(self):
        self.screen.fill((0, 0, 0))
        frame = self.frames[self.current_frame]
        frame_rect = frame.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(frame, frame_rect)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.update()
            self.draw()
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Map Scene")

    scene = MapScene(screen)
    scene.run()

    pygame.quit()
