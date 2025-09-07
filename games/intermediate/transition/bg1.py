import pygame
import os
import sys
from BG2Scene import BG2Scene  # Import your BG2Scene file

class BackgroundTransition:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Directories
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(base_dir, "bg")
        audio_dir = os.path.join(base_dir, "audio")

        # Load BG1 image
        bg_path = os.path.join(asset_dir, "bg1.png")
        if not os.path.exists(bg_path):
            print(f"❌ File not found: {bg_path}")
            sys.exit(1)
        self.bg_img = pygame.image.load(bg_path).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.screen.get_size())

        # Load audio
        audio_path = os.path.join(audio_dir, "op.mp3")
        if os.path.exists(audio_path):
            self.audio_loaded = True
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
        else:
            self.audio_loaded = False
            print(f"⚠️ Audio not found: {audio_path}")

    def fade_in_out(self, duration=7):
        total_frames = duration * 60  # 60 FPS
        half_frames = total_frames // 2

        if self.audio_loaded:
            pygame.mixer.music.play()

        running = True
        frame = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Calculate alpha
            if frame < half_frames:
                alpha = int((frame / half_frames) * 255)  # Fade in
            else:
                alpha = int(((total_frames - frame) / half_frames) * 255)  # Fade out

            # Draw
            self.screen.fill((0, 0, 0))
            temp_img = self.bg_img.copy()
            temp_img.set_alpha(alpha)
            self.screen.blit(temp_img, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)
            frame += 1
            if frame > total_frames:
                running = False

        if self.audio_loaded:
            pygame.mixer.music.stop()

        # After BG1 fade finishes, launch BG2Scene
        bg2_scene = BG2Scene(self.screen)
        bg2_scene.run()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("BG1 -> BG2 Transition with Dora")

    bg1 = BackgroundTransition(screen)
    bg1.fade_in_out(10)

    pygame.quit()
