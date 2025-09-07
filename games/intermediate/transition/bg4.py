import pygame
import os
import sys

# ---------------- Typewriter Dialogue (Sequential Sections, stacked) ----------------
# ---------------- Typewriter Dialogue (Sequential Sections, stacked properly) ----------------
class TypewriterDialogue:
    def __init__(self, screen, sections, font_size=28, color=(255, 255, 255), speed=0.3, margin=40, line_spacing=8):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.color = color
        self.outline_color = (0, 0, 0)
        self.sections = sections
        self.margin = margin
        self.line_spacing = line_spacing
        self.speed = speed

        self.current_section_index = 0
        self.char_index = 0.0
        self.current_text = ""
        self.active = False
        self.finished_section = False
        self.typed_sections = []

    def start(self):
        self.active = True
        self.char_index = 0.0
        self.current_text = ""
        self.finished_section = False

    def update(self):
        if not self.active or self.finished_section:
            return

        section_text = self.sections[self.current_section_index]
        if self.char_index < len(section_text):
            self.char_index += self.speed
            self.current_text = section_text[:int(self.char_index)]
        else:
            self.current_text = section_text
            self.finished_section = True
            self.typed_sections.append(section_text)

    def next_section(self):
        if self.finished_section:
            if self.current_section_index < len(self.sections) - 1:
                self.current_section_index += 1
                self.char_index = 0.0
                self.current_text = ""
                self.finished_section = False
            else:
                self.active = False

    def draw(self):
        if not self.active:
            return

        screen_w, screen_h = self.screen.get_size()
        # Start with current typing line at bottom
        y_offset = screen_h - self.margin

        # Draw current typing line first
        if not self.finished_section:
            line_surface = self.font.render(self.current_text, True, self.color)
            outline_surface = self.font.render(self.current_text, True, self.outline_color)
            text_rect = line_surface.get_rect(midbottom=(screen_w // 2, y_offset))
            self.screen.blit(outline_surface, text_rect.move(2, 2))
            self.screen.blit(line_surface, text_rect)
            y_offset -= (self.font.get_height() + self.line_spacing)

        # Draw previously typed sections above current line
        for section in reversed(self.typed_sections):
            line_surface = self.font.render(section, True, self.color)
            outline_surface = self.font.render(section, True, self.outline_color)
            text_rect = line_surface.get_rect(midbottom=(screen_w // 2, y_offset))
            self.screen.blit(outline_surface, text_rect.move(2, 2))
            self.screen.blit(line_surface, text_rect)
            y_offset -= (self.font.get_height() + self.line_spacing)


# ---------------- BG4 Scene ----------------
class BG4Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load all frames tile000 → tile155
        self.frames = []
        frame_dir = os.path.join(base_dir, "assets", "vids", "stage1")
        for i in range(149):  # 0 → 155
            filename = f"tile{i:03}.png"
            path = os.path.join(frame_dir, filename)
            if not os.path.exists(path):
                print(f"❌ Missing frame: {path}")
                sys.exit(1)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, self.screen.get_size())
            self.frames.append(img)

        self.total_frames = len(self.frames)
        self.current_frame = 0

        # Dialogue sections
        sections = [
            "Boots: “Linked Lists are like paths of nodes,",
            "with arrows called pointers that tell us",
            "where to go next!”"
        ]
        self.dialogue = TypewriterDialogue(
            screen,
            sections=sections,
            font_size=28,
            speed=0.3,
            margin=40,
            line_spacing=-8
        )

        # State
        self.state = "video"  # video → dialogue

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "dialogue":
                        if not self.dialogue.active:
                            self.dialogue.start()
                        else:
                            self.dialogue.next_section()

            self.screen.fill((0, 0, 0))

            # --- Video phase ---
            if self.state == "video":
                if self.current_frame < self.total_frames:
                    frame_img = self.frames[self.current_frame]
                    self.screen.blit(frame_img, (0, 0))
                    self.current_frame += 1
                else:
                    self.state = "dialogue"  # last frame static, wait for dialogue

            # --- Dialogue phase ---
            elif self.state == "dialogue":
                last_frame = self.frames[-1]
                self.screen.blit(last_frame, (0, 0))
                self.dialogue.update()
                self.dialogue.draw()

            pygame.display.flip()
            self.clock.tick(30)

# ---------------- Run BG4Scene ----------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("BG4 Stage1 Animation + Sequential Typewriter Dialogue")

    scene = BG4Scene(screen)
    scene.run()

    pygame.quit()
