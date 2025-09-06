import pygame
import os
import heapq

# --- Settings ---
TILE_SIZE = 32
FPS = 10

ASSET_DIR = os.path.dirname(__file__)
BLOCK_IMG = os.path.join(ASSET_DIR, "blocks", "block.png")

PACMAN_DIR = os.path.join(ASSET_DIR, "pacman")
DIRECTIONS = ["up", "down", "left", "right"]

# --- Dijkstra Algorithm ---
def dijkstra(graph, start, goal):
    pq = [(0, start)]
    distances = {start: 0}
    parent = {start: None}

    while pq:
        dist, node = heapq.heappop(pq)
        if node == goal:
            break
        for neighbor, cost in graph[node]:
            new_dist = dist + cost
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    # Reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent.get(node)
    return path[::-1]

# --- Pacman Game ---
class PacmanGame:
    def __init__(self, grid, start, goal):
        pygame.init()
        self.grid = grid
        self.rows, self.cols = len(grid), len(grid[0])
        self.start = start
        self.goal = goal

        self.screen = pygame.display.set_mode((self.cols*TILE_SIZE, self.rows*TILE_SIZE))
        pygame.display.set_caption("Pacman Dijkstra - Advanced Level")

        self.clock = pygame.time.Clock()

        # Load block image
        self.block_img = pygame.image.load(BLOCK_IMG).convert_alpha()
        self.block_img = pygame.transform.scale(self.block_img, (TILE_SIZE, TILE_SIZE))

        # Load Pacman sprites
        self.pacman_sprites = {d: [] for d in DIRECTIONS}
        for d in DIRECTIONS:
            folder = os.path.join(PACMAN_DIR, f"pacman-{d}")
            for i in range(1, 4):
                img = pygame.image.load(os.path.join(folder, f"{i}.png")).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.pacman_sprites[d].append(img)

        # Path
        self.graph = self.make_graph()
        self.path = dijkstra(self.graph, self.start, self.goal)
        self.current_index = 0
        self.anim_frame = 0
        self.direction = "right"

    def make_graph(self):
        graph = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:  # wall
                    continue
                neighbors = []
                for dr, dc, d in [(0,1,"right"),(0,-1,"left"),(1,0,"down"),(-1,0,"up")]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                        neighbors.append(((nr, nc), 1))
                graph[(r,c)] = neighbors
        return graph

    def get_direction(self, curr, nxt):
        r1, c1 = curr
        r2, c2 = nxt
        if r2 > r1: return "down"
        if r2 < r1: return "up"
        if c2 > c1: return "right"
        if c2 < c1: return "left"
        return self.direction

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw grid
            self.screen.fill((0,0,0))
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == 1:
                        self.screen.blit(self.block_img, (c*TILE_SIZE, r*TILE_SIZE))

            # Move Pacman along path
            if self.current_index < len(self.path)-1:
                curr = self.path[self.current_index]
                nxt = self.path[self.current_index+1]
                self.direction = self.get_direction(curr, nxt)
                pacman_sprite = self.pacman_sprites[self.direction][self.anim_frame//3 % 3]
                self.screen.blit(pacman_sprite, (curr[1]*TILE_SIZE, curr[0]*TILE_SIZE))

                self.anim_frame += 1
                if self.anim_frame % 6 == 0:  # move to next step every few frames
                    self.current_index += 1
            else:
                # Goal reached
                r, c = self.goal
                pacman_sprite = self.pacman_sprites[self.direction][self.anim_frame//3 % 3]
                self.screen.blit(pacman_sprite, (c*TILE_SIZE, r*TILE_SIZE))

            pygame.display.flip()

        pygame.quit()

# --- Run directly for testing ---
if __name__ == "__main__":
    grid = [
        [0,0,0,0,0,0],
        [0,1,1,1,1,0],
        [0,0,0,1,0,0],
        [0,1,0,0,0,1],
        [0,0,0,1,0,0],
        [0,0,0,0,0,0],
    ]
    start = (0,0)
    goal = (5,5)

    game = PacmanGame(grid, start, goal)
    game.run()
