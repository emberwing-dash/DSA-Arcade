import pygame
import sys
import os
import random

# -------- TypewriterDialogue class --------
class TypewriterDialogue:
    def __init__(self, screen, font_size=24, color=(255, 255, 255), speed=3, margin=20):
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
        self.dialogues = dialogues
        self.current_index = 0
        self.current_text = ""
        self.char_index = 0
        self.active = True
        self.finished = False

    def update(self):
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
        if not self.active or self.finished:
            return
        text_surface = self.font.render(self.current_text, True, self.color)
        sw, sh = self.screen.get_size()
        text_rect = text_surface.get_rect(midbottom=(sw // 2, sh - self.margin))
        self.screen.blit(text_surface, text_rect)

    def next(self):
        if self.current_index >= len(self.dialogues):
            return
        text = self.dialogues[self.current_index]
        if self.char_index < len(text):
            self.char_index = len(text)
            self.current_text = text
        else:
            if self.current_index < len(self.dialogues) - 1:
                self.current_index += 1
                self.char_index = 0
                self.current_text = ""
            else:
                self.active = False
                self.finished = True


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


class Apple(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)


class BeginnerTransitionPart1:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("Gamified DSA - Apple Fall Transition")
        self.clock = pygame.time.Clock()

        base_path = os.path.join(os.path.dirname(__file__), "..", "assets")

        self.bg = load_image(os.path.join(base_path, "bg", "bg.png"), (900, 700))

        apples_path = os.path.join(base_path, "apples")
        self.apple_images = []
        for fname in os.listdir(apples_path):
            if fname.lower().endswith((".png", ".jpeg", ".jpg")):
                img = load_image(os.path.join(apples_path, fname))
                if img:
                    self.apple_images.append(img)
        self.apples = pygame.sprite.Group()

        princess_path = os.path.join(base_path, "princess")
        self.princess_idle = load_frames(os.path.join(princess_path, "idle"))
        self.princess_fall = load_frames(os.path.join(princess_path, "fall"))
        self.princess_frame = 0
        self.princess_timer = 0
        self.princess = self.princess_idle[0] if self.princess_idle else None
        self.princess_rect = self.princess.get_rect(midbottom=(720, 422)) if self.princess else pygame.Rect(0, 0, 0, 0)

        mario_path = os.path.join(base_path, "mario")
        self.mario_up = load_frames(os.path.join(mario_path, "up"))
        self.mario_frame = 0
        self.mario_timer = 0
        self.mario = None
        self.mario_rect = None

        self.dialogue_texts = [
            "Princess Peach: Hmm, uuu huuuu~ (happily walking with basket)",
            "Princess Peach: Aaaahhh!",
            "Princess Peach: Oh no, my apples!",
            "Mario: Ha-ha! It’s-a me, Mario!",
            "Mario: Don’t-a worry, Princess Peach! I help-a you pick them up!",
        ]
        self.dialogue_actions = [
            "princess_walk",
            "princess_fall",
            "princess_idle",
            "mario_walk",
            "mario_idle",
        ]

        self.dialogue = TypewriterDialogue(self.screen, font_size=26, speed=2, margin=70)
        self.dialogue.set_dialogues(self.dialogue_texts)

        self.apples_spawned = False

        self.billboard = load_image(os.path.join(base_path, "bg", "billboard.png"))
        self.billboard_pos = [0, -self.billboard.get_height()]
        self.billboard_speed = 4
        self.billboard_state = "waiting"  # waiting, coming_down, pause, going_up, done
        self.billboard_pause_timer = 0
        self.billboard_pause_duration = 60

    def spawn_apples(self):
        area_x1, area_y1, area_x2, area_y2 = 357, 304, 775, 513
        positions = []
        max_attempts = 100
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
                positions.append((x, y))
        for pos in positions:
            img = random.choice(self.apple_images)
            self.apples.add(Apple(img, pos))

    def animate_princess(self, action):
        if not self.princess:
            return
        if action == "princess_walk":
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

    def animate_mario(self, action):
        if action == "mario_walk":
            if self.mario is None and self.mario_up:
                self.mario_frame = 0
                self.mario_timer = 0
                self.mario = self.mario_up[0]
                self.mario_rect = self.mario.get_rect(midbottom=(450, 700))
            self.mario_timer += 1
            if self.mario_timer > 10:
                self.mario_frame = (self.mario_frame + 1) % len(self.mario_up)
                self.mario_timer = 0
            self.mario = self.mario_up[self.mario_frame]
            if self.mario_rect.y > 500:
                self.mario_rect.y -= 2
        elif action == "mario_idle" and self.mario:
            self.mario = self.mario_up[0]

    def fade_out(self, speed=5):
        fade = pygame.Surface(self.screen.get_size())
        fade.fill((0, 0, 0))
        for alpha in range(0, 255, speed):
            fade.set_alpha(alpha)
            self.screen.blit(self.bg, (0, 0))

            # Draw scene behind fade
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

            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        # Billboard initial state
        self.billboard_state = "waiting"
        self.billboard_pos = [0, -self.billboard.get_height()]
        self.billboard_pause_timer = 0

        running = True
        fade_done = False

        while running:
            self.screen.blit(self.bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.billboard_state == "waiting":
                        self.dialogue.next()

            if self.billboard_state == "waiting":
                self.dialogue.update()

            if self.dialogue.finished and self.billboard_state == "waiting":
                self.billboard_state = "coming_down"

            if self.billboard_state == "coming_down":
                self.billboard_pos[1] += 4
                center_y = self.screen.get_height() // 2 - self.billboard.get_height() // 2
                if self.billboard_pos[1] >= center_y:
                    self.billboard_pos[1] = center_y
                    self.billboard_state = "pause"
            elif self.billboard_state == "pause":
                self.billboard_pause_timer += 1
                if self.billboard_pause_timer >= 60:
                    self.billboard_state = "going_up"
            elif self.billboard_state == "going_up":
                self.billboard_pos[1] -= 4
                if self.billboard_pos[1] < -self.billboard.get_height():
                    self.billboard_state = "done"

            can_play = self.billboard_state == "waiting"

            if can_play:
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

            if self.billboard_state != "done":
                self.screen.blit(self.billboard, self.billboard_pos)

            if can_play:
                self.dialogue.draw()

            if self.billboard_state == "done" and not fade_done:
                self.fade_out()
                fade_done = True
                running = False

            pygame.display.flip()
            self.clock.tick(60)

        # Transition to Apple Count scene
        from appleCount import AppleCountScene
        AppleCountScene().run()


if __name__ == "__main__":
    BeginnerTransitionPart1().run()
