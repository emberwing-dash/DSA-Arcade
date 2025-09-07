import pygame
import sys

# ---------------- Stage2Scene ----------------
class Stage2Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = "gameplay"  # "gameplay" or "ended"

        # Node positions
        self.nodes = ["Home", "Forest", "Bridge", "Castle", "Null"]
        self.node_positions = {
            "Home": (100, 300),
            "Forest": (250, 300),
            "Bridge": (400, 300),
            "Castle": (550, 300),
            "Null": (700, 300)
        }

        # Correct arrow connections
        self.correct_connections = [
            ("Home", "Forest"),
            ("Forest", "Bridge"),
            ("Bridge", "Castle"),
            ("Castle", "Null")
        ]

        # User connections
        self.user_connections = []

        # Dragging arrow
        self.dragging = False
        self.drag_start_node = None
        self.drag_end_pos = (0, 0)

        # Popup
        self.popup_message = ""
        self.popup_timer = 0

        # Fonts
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.popup_font = pygame.font.SysFont("Arial", 32, bold=True)

    def run(self):
        running = True
        while running:
            self.screen.fill((200, 200, 255))  # background color

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        for node, pos in self.node_positions.items():
                            x, y = pos
                            if (x-30 <= event.pos[0] <= x+30) and (y-30 <= event.pos[1] <= y+30):
                                self.dragging = True
                                self.drag_start_node = node
                                self.drag_end_pos = event.pos

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragging:
                        for node, pos in self.node_positions.items():
                            if node != self.drag_start_node:
                                x, y = pos
                                if (x-30 <= event.pos[0] <= x+30) and (y-30 <= event.pos[1] <= y+30):
                                    self.user_connections.append((self.drag_start_node, node))
                                    break
                        self.dragging = False
                        self.drag_start_node = None

            # Update dragging end position
            if self.dragging:
                self.drag_end_pos = pygame.mouse.get_pos()

            # --- Draw nodes ---
            for node, pos in self.node_positions.items():
                pygame.draw.circle(self.screen, (255, 255, 255), pos, 30)
                pygame.draw.circle(self.screen, (0, 0, 0), pos, 30, 3)
                text = self.font.render(node, True, (0, 0, 0))
                rect = text.get_rect(center=pos)
                self.screen.blit(text, rect)

            # --- Draw arrows ---
            for start, end in self.user_connections:
                start_pos = self.node_positions[start]
                end_pos = self.node_positions[end]
                color = (0, 255, 0) if (start, end) in self.correct_connections else (255, 0, 0)
                pygame.draw.line(self.screen, color, start_pos, end_pos, 5)
                # draw arrowhead
                self.draw_arrowhead(start_pos, end_pos, color)

            # Draw current dragging arrow
            if self.dragging:
                start_pos = self.node_positions[self.drag_start_node]
                pygame.draw.line(self.screen, (0, 0, 255), start_pos, self.drag_end_pos, 3)
                self.draw_arrowhead(start_pos, self.drag_end_pos, (0, 0, 255))

            # --- Check for popup ---
            if len(self.user_connections) == len(self.correct_connections) and not self.popup_message:
                all_correct = all(conn in self.correct_connections for conn in self.user_connections)
                if all_correct:
                    self.popup_message = "Success! All nodes linked correctly!"
                    self.popup_color = (0, 200, 0)
                else:
                    self.popup_message = "Incorrect! Some connections are wrong!"
                    self.popup_color = (200, 0, 0)
                self.popup_timer = 120  # show 2 seconds

            # --- Draw popup ---
            if self.popup_message:
                text_surface = self.popup_font.render(self.popup_message, True, self.popup_color)
                rect = text_surface.get_rect(center=(self.screen.get_width()//2, 100))
                pygame.draw.rect(self.screen, (0,0,0), rect.inflate(20,20))
                self.screen.blit(text_surface, rect)
                self.popup_timer -= 1
                if self.popup_timer <= 0:
                    self.popup_message = ""

            pygame.display.flip()
            self.clock.tick(60)

    def draw_arrowhead(self, start, end, color):
        # Draw simple arrowhead
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
    pygame.display.set_caption("Stage2 – Singly Linked List Gameplay")
    scene = Stage2Scene(screen)
    scene.run()
    pygame.quit()
