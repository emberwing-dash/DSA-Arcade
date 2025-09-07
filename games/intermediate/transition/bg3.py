import pygame
import os
import sys
from PIL import Image

# ---------------- Typewriter Dialogue ----------------
class TypewriterDialogue:
    def __init__(self, screen, sections, font_size=28, color=(255,255,255), speed=0.3, margin=40, line_spacing=8):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.color = color
        self.outline_color = (0,0,0)
        self.sections = sections
        self.margin = margin
        self.line_spacing = line_spacing
        self.current_section_index = 0
        self.char_index = 0.0
        self.current_text = ""
        self.speed = speed
        self.active = False
        self.finished_section = False
        self.typed_sections = []

    def start(self):
        if self.current_section_index >= len(self.sections):
            return
        self.active = True
        self.char_index = 0.0
        self.current_text = ""
        self.finished_section = False
        self.current_lines = self.sections[self.current_section_index].split("\n")

    def update(self):
        if not self.active or self.finished_section:
            return
        combined = "".join(self.current_lines)
        if self.char_index < len(combined):
            self.char_index += self.speed
            self.current_text = combined[:int(self.char_index)]
        else:
            self.finished_section = True
            self.typed_sections.append(self.sections[self.current_section_index])

    def draw(self):
        screen_w, screen_h = self.screen.get_size()
        # Draw previous sections stacked upwards
        y_offset = screen_h - self.margin
        for section in self.typed_sections:
            for line in section.split("\n"):
                surf = self.font.render(line, True, self.color)
                outline = self.font.render(line, True, self.outline_color)
                rect = surf.get_rect(midbottom=(screen_w//2, y_offset))
                self.screen.blit(outline, rect.move(2,2))
                self.screen.blit(surf, rect)
                y_offset -= self.font.get_height() + self.line_spacing

        # Draw current typing section
        if not self.finished_section:
            for line in self.current_text.split("\n"):
                surf = self.font.render(line, True, self.color)
                outline = self.font.render(line, True, self.outline_color)
                rect = surf.get_rect(midbottom=(screen_w//2, y_offset))
                self.screen.blit(outline, rect.move(2,2))
                self.screen.blit(surf, rect)
                y_offset -= self.font.get_height() + self.line_spacing

    def next_section(self):
        if self.current_section_index < len(self.sections)-1:
            self.current_section_index += 1
            self.start()
        else:
            self.active = False

# ---------------- BG3Scene using Stage1.gif ----------------
class BG3Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load GIF frames using PIL
        gif_path = os.path.join(base_dir, "assets", "Stage1.gif")
        if not os.path.exists(gif_path):
            print(f"❌ GIF not found: {gif_path}")
            sys.exit(1)

        pil_gif = Image.open(gif_path)
        self.frames = []
        try:
            while True:
                frame = pil_gif.convert("RGBA")
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                py_frame = pygame.image.fromstring(data, size, mode)
                py_frame = pygame.transform.scale(py_frame, self.screen.get_size())
                self.frames.append(py_frame)
                pil_gif.seek(pil_gif.tell()+1)
        except EOFError:
            pass  # finished reading GIF

        self.total_frames = len(self.frames)
        self.current_frame = 0

        # Dialogue sections
        dialogue_sections = [
            "Boots: “Linked Lists are like paths of nodes,",
            "with arrows called pointers that tell us",
            "where to go next!”"
        ]
        self.dialogue = TypewriterDialogue(screen, dialogue_sections, font_size=28, speed=0.3)
        self.state = "video"  # video -> wait_for_space -> dialogue

    def run(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: running=False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE and self.state=="wait_for_space":
                        self.dialogue.start()
                        self.state="dialogue"
                    elif e.key == pygame.K_SPACE and self.state=="dialogue" and self.dialogue.finished_section:
                        self.dialogue.next_section()

            self.screen.fill((0,0,0))

            # GIF phase
            if self.state=="video":
                if self.current_frame < self.total_frames:
                    self.screen.blit(self.frames[self.current_frame], (0,0))
                    self.current_frame += 1
                else:
                    self.state="wait_for_space"
                    self.screen.blit(self.frames[-1], (0,0))

            # Dialogue phase
            elif self.state in ["wait_for_space","dialogue"]:
                self.screen.blit(self.frames[-1], (0,0))
                self.dialogue.update()
                self.dialogue.draw()

            pygame.display.flip()
            self.clock.tick(30)

# ---------------- Run BG3Scene ----------------
if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("BG3 Scene GIF + Dialogue")
    scene = BG3Scene(screen)
    scene.run()
    pygame.quit()
