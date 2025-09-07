import pygame
import sys

# ---------------- Typewriter Dialogue for Stage2 ----------------
class TypewriterDialogue:
    def __init__(self, screen, sections, font_size=28, color=(0, 0, 0), speed=0.3, margin=40, line_spacing=8):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.color = color
        self.outline_color = (255, 255, 255)
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
                self.active = False  # all dialogue done

    def draw(self):
        if not self.active:
            return
        y_offset = self.margin
        for section in self.typed_sections:
            line_surface = self.font.render(section, True, self.color)
            outline_surface = self.font.render(section, True, self.outline_color)
            rect = line_surface.get_rect(topleft=(50, y_offset))
            self.screen.blit(outline_surface, rect.move(2, 2))
            self.screen.blit(line_surface, rect)
            y_offset += self.font.get_height() + self.line_spacing

        if not self.finished_section:
            line_surface = self.font.render(self.current_text, True, self.color)
            outline_surface = self.font.render(self.current_text, True, self.outline_color)
            rect = line_surface.get_rect(topleft=(50, y_offset))
            self.screen.blit(outline_surface, rect.move(2, 2))
            self.screen.blit(line_surface, rect)

# ---------------- Stage2Scene ----------------
class Stage2Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = "dialogue"  # dialogue → gameplay → popup

        # Node positions
        self.nodes = ["Home", "Forest", "Bridge", "Castle", "Null"]
        self.node_positions = {
            "Home": (100, 400),
            "Forest": (250, 400),
            "Bridge": (400, 400),
            "Castle": (550, 400),
            "Null": (700, 400)
        }
        self.correct_connections = [
            ("Home", "Forest"),
            ("Forest", "Bridge"),
            ("Bridge", "Castle"),
            ("Castle", "Null")
        ]
        self.user_connections = []
        self.dragging = False
        self.drag_start_node = None
        self.drag_end_pos = (0, 0)

        # Popup
        self.popup_message = ""
        self.popup_color = (0, 0, 0)
        self.show_popup = False

        # Fonts
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.popup_font = pygame.font.SysFont("Arial", 32, bold=True)

        # Dialogue sections
        sections = [
            "Dora: “This is the Singly Path. It goes one way, from the Head all the way to Null.”",
            "Boots: “Let’s link the nodes with arrows!”"
        ]
        self.dialogue = TypewriterDialogue(screen, sections, font_size=24, speed=0.3, margin=20)

    def reset_stage(self):
        self.user_connections = []
        self.dragging = False
        self.drag_start_node = None
        self.drag_end_pos = (0, 0)
        self.popup_message = ""
        self.show_popup = False
        self.state = "gameplay"

    def run(self):
        running = True
        while running:
            self.screen.fill((200, 200, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "dialogue":
                        if not self.dialogue.active:
                            self.dialogue.start()
                        else:
                            self.dialogue.next_section()
                            if not self.dialogue.active:
                                self.state = "gameplay"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.show_popup:
                            self.reset_stage()
                        elif self.state == "gameplay":
                            for node, pos in self.node_positions.items():
                                x, y = pos
                                if (x-30 <= event.pos[0] <= x+30) and (y-30 <= event.pos[1] <= y+30):
                                    self.dragging = True
                                    self.drag_start_node = node
                                    self.drag_end_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragging and self.state == "gameplay":
                        for node, pos in self.node_positions.items():
                            if node != self.drag_start_node:
                                x, y = pos
                                if (x-30 <= event.pos[0] <= x+30) and (y-30 <= event.pos[1] <= y+30):
                                    self.user_connections.append((self.drag_start_node, node))
                                    break
                        self.dragging = False
                        self.drag_start_node = None

            # Update dragging end
            if self.dragging and self.state == "gameplay":
                self.drag_end_pos = pygame.mouse.get_pos()

            # --- Draw dialogue ---
            if self.state == "dialogue":
                self.dialogue.update()
                self.dialogue.draw()

            # --- Draw nodes ---
            if self.state in ["gameplay", "popup"]:
                for node, pos in self.node_positions.items():
                    pygame.draw.circle(self.screen, (255, 255, 255), pos, 30)
                    pygame.draw.circle(self.screen, (0, 0, 0), pos, 3)
                    text = self.font.render(node, True, (0, 0, 0))
                    rect = text.get_rect(center=pos)
                    self.screen.blit(text, rect)

                # Draw arrows
                for start, end in self.user_connections:
                    start_pos = self.node_positions[start]
                    end_pos = self.node_positions[end]
                    color = (0, 255, 0) if (start, end) in self.correct_connections else (255, 0, 0)
                    pygame.draw.line(self.screen, color, start_pos, end_pos, 5)
                    self.draw_arrowhead(start_pos, end_pos, color)

                # Draw current dragging
                if self.dragging:
                    start_pos = self.node_positions[self.drag_start_node]
                    pygame.draw.line(self.screen, (0, 0, 255), start_pos, self.drag_end_pos, 3)
                    self.draw_arrowhead(start_pos, self.drag_end_pos, (0, 0, 255))

                # Check popup
                if not self.show_popup and len(self.user_connections) == len(self.correct_connections):
                    all_correct = all(conn in self.correct_connections for conn in self.user_connections)
                    if all_correct:
                        self.popup_message = "Success! All nodes linked correctly!"
                        self.popup_color = (0, 200, 0)
                    else:
                        self.popup_message = "Incorrect! Try again!"
                        self.popup_color = (200, 0, 0)
                    self.show_popup = True
                    self.state = "popup"

            # --- Draw popup ---
            if self.show_popup:
                popup_surface = pygame.Surface((600, 150))
                popup_surface.fill((50, 50, 50))
                pygame.draw.rect(popup_surface, (0, 0, 0), popup_surface.get_rect(), 3)
                text_surface = self.popup_font.render(self.popup_message, True, self.popup_color)
                text_rect = text_surface.get_rect(center=(300, 75))
                popup_surface.blit(text_surface, text_rect)
                self.screen.blit(popup_surface, (100, 200))

            pygame.display.flip()
            self.clock.tick(60)

    def draw_arrowhead(self, start, end, color):
        import math
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        angle = math.atan2(dy, dx)
        length = 15
        angle1 = angle + math.pi / 6
        angle2 = angle - math.pi / 6
        x1 = end[0] - length * math.cos(angle1)
        y1 = end[1] - length * math.sin(angle1)
        x2 = end[0] - length * math.cos(angle2)
        y2 = end[1] - length * math.sin(angle2)
        pygame.draw.polygon(self.screen, color, [end, (x1, y1), (x2, y2)])

# ---------------- Run Stage2Scene ----------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Stage2 – Singly Linked List Gameplay with Dialogue")
    scene = Stage2Scene(screen)
    scene.run()
    pygame.quit()
