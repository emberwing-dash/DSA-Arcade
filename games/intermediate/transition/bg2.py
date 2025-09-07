import pygame
import os
import sys

class DoraAnimation:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.frames = []
        self.load_frames()
        self.x = -300  # start completely offscreen
        self.speed = 1  # very slow horizontal movement
        self.frame_delay = 20  # ticks per frame to slow animation
        self.frame_counter = 0

    def load_frames(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        frames_dir = os.path.join(base_dir, "dora", "bg2")  # path to Dora frames

        for i in range(0, 3):  # tile000 -> tile008
            filename = f"tile{i:03}.png"
            path = os.path.join(frames_dir, filename)
            if not os.path.exists(path):
                print(f"❌ File not found: {path}")
                sys.exit(1)
            img = pygame.image.load(path).convert_alpha()
            # Scale image 3x
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w*3, h*3))
            self.frames.append(img)

        self.total_frames = len(self.frames)
        self.current_frame = 0
        self.final_y = self.screen.get_height() - self.frames[0].get_height()  # bottom of screen

    def run_once(self, bg_img=None):
        """Slide Dora once from left to bottom-middle"""
        running = True
        reached_center = False
        screen_center_x = self.screen.get_width() // 2

        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw background
            if bg_img:
                self.screen.blit(bg_img, (0,0))
            else:
                self.screen.fill((0,0,0))

            # Horizontal slide
            frame_w = self.frames[self.current_frame].get_width()
            target_x = screen_center_x - frame_w // 2
            if not reached_center:
                if self.x + self.speed < target_x:
                    self.x += self.speed
                else:
                    self.x = target_x
                    reached_center = True

            # Vertical position
            y = self.final_y if reached_center else self.screen.get_height()//2 - self.frames[self.current_frame].get_height()//2

            # Draw current frame
            self.screen.blit(self.frames[self.current_frame], (self.x, y))

            # Advance frame slowly
            if not reached_center:
                self.frame_counter += 1
                if self.frame_counter >= self.frame_delay:
                    self.frame_counter = 0
                    if self.current_frame < self.total_frames - 1:
                        self.current_frame += 1
            else:
                self.current_frame = self.total_frames - 1  # freeze last frame

            pygame.display.flip()

        pygame.quit()


class BackgroundTransition2:
    def __init__(self, screen):
        self.screen = screen
        # Load static background
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, "bg", "bg2.jpg")
        if not os.path.exists(bg_path):
            print(f"❌ File not found: {bg_path}")
            sys.exit(1)
        self.bg_img = pygame.image.load(bg_path).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())
        self.dora = DoraAnimation(screen)

    def run(self):
        self.dora.run_once(bg_img=self.bg_img)


# --- Standalone test ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("BG2 Dora Slide Animation")

    bg2 = BackgroundTransition2(screen)
    bg2.run()

    pygame.quit()
