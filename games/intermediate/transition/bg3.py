import pygame
import os
import sys

# ---------------- Typewriter Dialogue (Previous Up, Current Down) ----------------
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
        self.typed_sections = []  # sections already completed

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
        # Draw previously typed sections, stacked upward
        y_offset = screen_h - self.margin
        for section in self.typed_sections:
            lines = section.split("\n")
            for line in lines:
                line_surface = self.font.render(line, True, self.color)
                outline_surface = self.font.render(line, True, self.outline_color)
                text_rect = line_surface.get_rect(midbottom=(screen_w//2, y_offset))
                self.screen.blit(outline_surface, text_rect.move(2,2))
                self.screen.blit(line_surface, text_rect)
                y_offset -= self.font.get_height() + self.line_spacing

        # Draw current typing section below previous ones
        if not self.finished_section:
            lines = self.current_text.split("\n")
            for line in lines:
                line_surface = self.font.render(line, True, self.color)
                outline_surface = self.font.render(line, True, self.outline_color)
                text_rect = line_surface.get_rect(midbottom=(screen_w//2, y_offset))
                self.screen.blit(outline_surface, text_rect.move(2,2))
                self.screen.blit(line_surface, text_rect)
                y_offset -= self.font.get_height() + self.line_spacing

    def next_section(self):
        if self.current_section_index < len(self.sections)-1:
            self.current_section_index += 1
            self.start()
        else:
            self.active = False  # all sections done

# ---------------- BG4 Scene ----------------
class BG3Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load video frames
        self.frames = []
        frame_dir = os.path.join(base_dir, "assets", "vids", "stage1")
        for i in range(149):
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "wait_for_space":
                        self.dialogue.start()
                        self.state = "dialogue"
                    elif event.key == pygame.K_SPACE and self.state == "dialogue" and self.dialogue.finished_section:
                        self.dialogue.next_section()

            self.screen.fill((0,0,0))

            # Video phase
            if self.state == "video":
                if self.current_frame < self.total_frames:
                    self.screen.blit(self.frames[self.current_frame], (0,0))
                    self.current_frame += 1
                else:
                    self.state = "wait_for_space"
                    self.screen.blit(self.frames[-1], (0,0))

            # Dialogue phase
            elif self.state in ["wait_for_space", "dialogue"]:
                self.screen.blit(self.frames[-1], (0,0))
                self.dialogue.update()
                self.dialogue.draw()

            pygame.display.flip()
            self.clock.tick(30)

# ---------------- Run BG4Scene ----------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("BG4 Dialogue Stacked Upwards Example")

    scene = BG4Scene(screen)
    scene.run()
    pygame.quit()

