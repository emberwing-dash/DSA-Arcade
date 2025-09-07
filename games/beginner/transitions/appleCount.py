import pygame
import sys
import os

# -------- Helper to load images --------
def load_image(path, scale=None):
    if not os.path.exists(path):
        print(f"❌ Missing: {path}")
        return None
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.smoothscale(img, scale)
    return img


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
        screen_width, screen_height = self.screen.get_size()
        text_rect = text_surface.get_rect(midbottom=(screen_width // 2, screen_height - self.margin))
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


# -------- Apple sprite (simple container) --------
class Apple:
    def __init__(self, image, pos, filename):
        self.image = image
        self.pos = pos
        self.filename = filename
        self.rect = self.image.get_rect(center=pos)
        self.box_rect = pygame.Rect(self.rect.left - 10, self.rect.top - 10,
                                    self.rect.width + 20, self.rect.height + 40)  # Box with padding and space below for filename


class AppleCountScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("Apple Count - Intro to Array")
        self.clock = pygame.time.Clock()

        base_path = os.path.join(os.path.dirname(__file__), "..", "assets")

        # Load billboard image
        self.billboard = load_image(os.path.join(base_path, "bg", "billboard.png"))
        self.billboard_pos = [0, -self.billboard.get_height()]  # start above screen top left
        self.billboard_speed = 4  # pixels per frame
        self.billboard_state = "coming_down"  # states: coming_down, pause, going_up, done
        self.billboard_pause_timer = 0
        self.billboard_pause_duration = 60  # frames to pause at middle

        # Load apples (5 apples with filenames)
        apples_path = os.path.join(base_path, "apples")
        # We'll pick exactly 5 apples, sorted alphabetically
        filenames = sorted(
            [f for f in os.listdir(apples_path) if f.lower().endswith((".png", ".jpeg", ".jpg"))]
        )[:5]

        # Positions - spaced horizontally in middle screen area
        start_x = 150
        step_x = 140
        fixed_y = 350
        self.apples = []
        for i, filename in enumerate(filenames):
            img = load_image(os.path.join(apples_path, filename), scale=(100, 100))
            pos = (start_x + step_x * i, fixed_y)
            self.apples.append(Apple(img, pos, filename))

        # Header text
        self.header_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.header_text = self.header_font.render("Intro to Array", True, (255, 255, 255))
        self.header_pos = (20, 20)

        # Address font for numbers above boxes
        self.address_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.show_addresses = False  # control when to show addresses (1001..1005)
        self.addresses = ['1001', '1002', '1003', '1004', '1005']

        # Dialogue lines from Mario
        self.dialogue_lines = [
            "Let's learn Array Basics",
            "First, array consist of elements of same data type",
            "It allows us to store multiple elements in one variable name",
            "The catch is it has different address location",
            "You see the addresses of each array element here?",
            "They are not same but yet have sequential memory locations",
        ]
        self.dialogue = TypewriterDialogue(self.screen, font_size=26, speed=2, margin=70)
        self.dialogue.set_dialogues(self.dialogue_lines)

        self.transition_to_next = False

    def update_billboard(self):
        if self.billboard_state == "coming_down":
            self.billboard_pos[1] += self.billboard_speed
            if self.billboard_pos[1] >= (self.screen.get_height() // 2 - self.billboard.get_height() // 2):
                self.billboard_pos[1] = self.screen.get_height() // 2 - self.billboard.get_height() // 2
                self.billboard_state = "pause"
        elif self.billboard_state == "pause":
            self.billboard_pause_timer += 1
            if self.billboard_pause_timer >= self.billboard_pause_duration:
                self.billboard_state = "going_up"
        elif self.billboard_state == "going_up":
            self.billboard_pos[1] -= self.billboard_speed
            if self.billboard_pos[1] < -self.billboard.get_height():
                self.billboard_state = "done"
                self.transition_to_next = True

    def draw_billboard(self):
        if self.billboard_state != "done" and self.billboard:
            self.screen.blit(self.billboard, self.billboard_pos)

    def draw_apples(self):
        for apple in self.apples:
            # Draw bounding box
            pygame.draw.rect(self.screen, (255, 255, 255), apple.box_rect, 2)
            # Draw apple image
            self.screen.blit(apple.image, apple.rect)
            # Draw filename under apple inside box
            filename_surface = self.address_font.render(apple.filename, True, (255, 255, 255))
            filename_rect = filename_surface.get_rect(midtop=(apple.rect.centerx, apple.rect.bottom + 5))
            self.screen.blit(filename_surface, filename_rect)

    def draw_addresses(self):
        # Above each apple box, draw address string if enabled
        if self.show_addresses:
            for i, apple in enumerate(self.apples):
                addr_surface = self.address_font.render(self.addresses[i], True, (255, 255, 0))
                addr_rect = addr_surface.get_rect(midbottom=(apple.box_rect.centerx, apple.box_rect.top - 5))
                self.screen.blit(addr_surface, addr_rect)

    def run(self):
        running = True
        while running:
            self.screen.fill((30, 30, 50))  # dark background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Only allow advancing dialogue after billboard is done
                    if self.billboard_state == "done":
                        self.dialogue.next()

            # Animate billboard until done
            if self.billboard_state != "done":
                self.update_billboard()
                self.draw_billboard()
            else:
                # Billboard done, show rest of scene
                # Draw header
                self.screen.blit(self.header_text, self.header_pos)

                # Draw apples with filename boxes
                self.draw_apples()

                # Update and draw dialogue (Mario speaking)
                self.dialogue.update()
                self.dialogue.draw()

                # Logic to show addresses during specific dialogue lines
                # Show addresses when dialogue on lines 3 and 4 (0-indexed)
                if 3 <= self.dialogue.current_index <= 4:
                    self.show_addresses = True
                else:
                    self.show_addresses = False

                # Draw addresses if enabled
                self.draw_addresses()

                # After last dialogue line finishes, transition (just exit here)
                if self.dialogue.finished:
                    # Simple example: quit or could load next scene
                    running = False

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    AppleCountScene = AppleCountScene()
    AppleCountScene.run()
