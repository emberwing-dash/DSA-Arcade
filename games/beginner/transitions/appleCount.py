import pygame
import sys
import os

def load_image(path, scale=None):
    if not os.path.exists(path):
        print(f"❌ Missing: {path}")
        return None
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.smoothscale(img, scale)
    return img

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


class Apple:
    def __init__(self, image, pos, filename):
        self.image = image
        self.pos = pos
        # Remove extension from filename for display
        self.filename = os.path.splitext(filename)[0]
        self.rect = self.image.get_rect(center=pos)
        self.box_rect = pygame.Rect(self.rect.left - 10, self.rect.top - 10,
                                    self.rect.width + 20, self.rect.height + 40)  # box (+ space)

class AppleCountScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("Apple Count - Intro to Array")
        self.clock = pygame.time.Clock()

        base_path = os.path.join(os.path.dirname(__file__), "..", "assets")

        apples_path = os.path.join(base_path, "apples")
        filenames = sorted([f for f in os.listdir(apples_path) if f.lower().endswith((".png", ".jpeg", ".jpg"))])[:5]

        start_x = 150
        step_x = 140
        fixed_y = 350
        self.apples = []
        for i, filename in enumerate(filenames):
            img = load_image(os.path.join(apples_path, filename), scale=(100, 100))
            pos = (start_x + step_x * i, fixed_y)
            self.apples.append(Apple(img, pos, filename))

        self.header_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.header_text = self.header_font.render("Array Basics", True, (255, 255, 0))
        self.header_pos = (20, 20)

        self.address_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.show_addresses = False
        self.addresses = ['1001', '1002', '1003', '1004', '1005']

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

    def draw_apples(self):
        for apple in self.apples:
            pygame.draw.rect(self.screen, (255, 255, 255), apple.box_rect, 2)
            self.screen.blit(apple.image, apple.rect)
            filename_surf = self.address_font.render(apple.filename, True, (255, 255, 255))
            filename_rect = filename_surf.get_rect(midtop=(apple.rect.centerx, apple.rect.bottom + 5))
            self.screen.blit(filename_surf, filename_rect)

    def draw_addresses(self):
        if self.show_addresses:
            for i, apple in enumerate(self.apples):
                addr_surf = self.address_font.render(self.addresses[i], True, (255, 255, 0))
                addr_rect = addr_surf.get_rect(midbottom=(apple.box_rect.centerx, apple.box_rect.top - 5))
                self.screen.blit(addr_surf, addr_rect)

    def run(self):
        running = True
        while running:
            self.screen.fill((30, 30, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.dialogue.next()

            self.draw_apples()
            self.screen.blit(self.header_text, self.header_pos)

            self.dialogue.update()
            self.dialogue.draw()

            self.show_addresses = 3 <= self.dialogue.current_index <= 4
            self.draw_addresses()

            if self.dialogue.finished:
                running = False  # or trigger next scene

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    scene = AppleCountScene()
    scene.run()
