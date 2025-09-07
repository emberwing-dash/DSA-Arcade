import pygame
import sys
import os
import random

# -------- TypewriterDialogue class with fix --------
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
            if self.char_index > len(text):
                self.char_index = len(text)
            self.current_text = text[:self.char_index]
        else:
            self.current_text = text

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
        if self.current_index >= len(self.dialogues):
            return

        text = self.dialogues[self.current_index]
        # If text partially typed, finish it first
        if self.char_index < len(text):
            self.char_index = len(text)
            self.current_text = text
        else:
            # Move to next dialogue or finish
            if self.current_index < len(self.dialogues) - 1:
                self.current_index += 1
                self.char_index = 0
                self.current_text = ""
            else:
                self.active = False
                self.finished = True


# -------- Helper functions to load assets --------
def load_image(path, scale=None):
    if not os.path.exists(path):
        print(f"❌ Missing: {path}")
        return None
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.smoothscale(img, scale)
    return img

def load_frames(folder):
    if not os.path.exists(folder):
        print(f"❌ Missing folder: {folder}")
        return []
    return [
        load_image(os.path.join(folder, f))
        for f in sorted(os.listdir(folder))
        if f.endswith(".png") or f.endswith(".jpeg") or f.endswith(".jpg")
    ]


# -------- Apple sprite --------
class Apple(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)


# -------- Main transition scene --------
class BeginnerTransitionPart1:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("Beginner Transition - Apple Fall 🍎")
        self.clock = pygame.time.Clock()

        # Path setup (assuming this script is in games/beginner/transitions)
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets")

        # Background
        self.bg = load_image(os.path.join(base_path, "bg", "bg.png"), (900, 700))

        # Apples: load all matching images (png/jpeg) from apples folder
        apples_path = os.path.join(base_path, "apples")
        self.apple_images = []
        for fname in os.listdir(apples_path):
            if fname.lower().endswith((".png", ".jpeg", ".jpg")):
                img = load_image(os.path.join(apples_path, fname))
                if img:
                    self.apple_images.append(img)
        self.apples = pygame.sprite.Group()

        # Princess animations (only fall + idle folders)
        princess_path = os.path.join(base_path, "princess")
        self.princess_idle = load_frames(os.path.join(princess_path, "idle"))
        self.princess_fall = load_frames(os.path.join(princess_path, "fall"))
        self.princess_frame = 0
        self.princess_timer = 0
        self.princess = self.princess_idle[0] if self.princess_idle else None
        self.princess_rect = self.princess.get_rect(midbottom=(720, 422)) if self.princess else pygame.Rect(0,0,0,0)

        # Mario animations (only load 'up' folder for this transition)
        mario_path = os.path.join(base_path, "mario")
        self.mario_up = load_frames(os.path.join(mario_path, "up"))
        self.mario_frame = 0
        self.mario_timer = 0
        self.mario = None
        self.mario_rect = None

        # Dialogue texts & synced animation actions
        self.dialogue_texts = [
            "Princess Peach: Hmm uuu huuuu~ (happily walking with basket)",
            "Princess Peach: Aaaahhh!",
            "Princess Peach: Oh no, my apples!",
            "Mario: Ha-ha! It’s-a me, Mario!",
            "Mario: Don’t-a worry, Princess Peach! I help-a you pick them up!",
        ]
        self.dialogue_actions = [
            "princess_walk",     # will use princess_idle animation frames
            "princess_fall",
            "princess_idle",
            "mario_walk",
            "mario_idle",
        ]

        # Initialize typewriter dialogue
        self.dialogue = TypewriterDialogue(self.screen, font_size=26, speed=2, margin=70)
        self.dialogue.set_dialogues(self.dialogue_texts)

        self.apples_spawned = False

    # Spawn scattered apples with attempt limit to prevent infinite loop
    def spawn_apples(self):
        area_x1, area_y1, area_x2, area_y2 = 357, 304, 775, 513
        positions = []
        max_attempts = 100  # max tries to find a spot for each apple
        for _ in range(5):
            attempts = 0
            while attempts < max_attempts:
                x = random.randint(area_x1, area_x2)
                y = random.randint(area_y1, area_y2)
                if all(abs(x - px) > 40 and abs(y - py) > 40 for px, py in positions):
                    positions.append((x, y))
                    break
                attempts += 1
            else:
                # If fails, accept last tried position anyway
                positions.append((x, y))
        for pos in positions:
            img = random.choice(self.apple_images)
            self.apples.add(Apple(img, pos))

    # Animate princess: use idle frames for princess_walk action
    def animate_princess(self, action):
        if not self.princess:
            return
        if action == "princess_walk":
            # Use idle frames also for walk
            self.princess_timer += 1
            if self.princess_timer > 10:
                self.princess_frame = (self.princess_frame + 1) % len(self.princess_idle)
                self.princess_timer = 0
            self.princess = self.princess_idle[self.princess_frame]
            self.princess_rect.x -= 2
        elif action == "princess_fall":
            if self.princess_frame < len(self.princess_fall) - 1:
                self.princess_timer += 1
                if self.princess_timer > 8:
                    self.princess_frame += 1
                    self.princess_timer = 0
            self.princess = self.princess_fall[self.princess_frame]
            if not self.apples_spawned:
                self.spawn_apples()
                self.apples_spawned = True
        elif action == "princess_idle":
            self.princess_timer += 1
            if self.princess_timer > 15:
                self.princess_frame = (self.princess_frame + 1) % len(self.princess_idle)
                self.princess_timer = 0
            self.princess = self.princess_idle[self.princess_frame]

    # Animate mario according to dialogue action
    def animate_mario(self, action):
        if action == "mario_walk":
            if self.mario is None and self.mario_up:
                self.mario_frame = 0
                self.mario_timer = 0
                self.mario = self.mario_up[0]
                self.mario_rect = self.mario.get_rect(midbottom=(450, 700))
            if self.mario:
                self.mario_timer += 1
                if self.mario_timer > 10:
                    self.mario_frame = (self.mario_frame + 1) % len(self.mario_up)
                    self.mario_timer = 0
                self.mario = self.mario_up[self.mario_frame]
                if self.mario_rect.y > 500:
                    self.mario_rect.y -= 2
        elif action == "mario_idle" and self.mario and self.mario_up:
            self.mario = self.mario_up[0]

    # Main run loop
    def run(self):
        running = True
        while running:
            self.screen.blit(self.bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.dialogue.next()

            self.dialogue.update()

            idx = self.dialogue.current_index
            action = self.dialogue_actions[idx] if idx < len(self.dialogue_actions) else None

            if action:
                self.animate_princess(action)
                if "mario" in action:
                    self.animate_mario(action)

            self.apples.draw(self.screen)

            if self.princess:
                self.screen.blit(self.princess, self.princess_rect)
            if self.mario:
                self.screen.blit(self.mario, self.mario_rect)

            self.dialogue.draw()

            pygame.display.flip()
            self.clock.tick(60)


# ---------------- Run ----------------
if __name__ == "__main__":
    BeginnerTransitionPart1().run()
