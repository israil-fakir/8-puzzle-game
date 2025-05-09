import pygame
import random
import time
from collections import deque
from sprite import *
from setting import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.random_time = 0
        self.start_random = False
        self.previous_move = ""
        self.start_game = False
        self.start_timer = False
        self.play_current_time = 0
        self.win = 0
        self.high_score = float(self.high_score()[0])

    def high_score(self):
        with open("highscore.txt", "r") as file:
            score = file.read().splitlines()
        return score

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str("%.3f" % self.high_score))

    def create_game(self):
        grid = []
        number = 1
        for x in range(gamesize):
            grid.append([])
            for y in range(gamesize):
                grid[x].append(number)
                number += 1

        grid[-1][-1] = 0
        return grid

    def random(self):
        possible_move = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_move.append("right")
                    if tile.left():
                        possible_move.append("left")
                    if tile.up():
                        possible_move.append("up")
                    if tile.dwon():
                        possible_move.append("down")
                    break
            if len(possible_move) > 0:
                break

        if self.previous_move == "right":
            if "left" in possible_move:
                possible_move.remove("left")
        elif self.previous_move == "left":
            if "right" in possible_move:
                possible_move.remove("right")
        elif self.previous_move == "up":
            if "down" in possible_move:
                possible_move.remove("down")
        elif self.previous_move == "down":
            if "up" in possible_move:
                possible_move.remove("up")

        choice = random.choice(possible_move)
        self.previous_move = choice

        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col+1] = self.tiles_grid[row][col+1], self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col-1] = self.tiles_grid[row][col-1], self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

    def draw_tiles(self): 
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile_val in enumerate(x):
                if tile_val != 0:
                    self.tiles[row].append(tile(self, col, row, str(tile_val)))
                else:
                    self.tiles[row].append(tile(self, col, row, "empty"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapesd_time = 0
        self.start_timer = False
        self.start_game = False
        self.win = False

        self.button_list = []
        self.button_list.append(button(750,130,300,50,"Clean High Score",white, black))
        self.button_list.append(button(800, 200, 200, 50, "Random", white, black))
        self.button_list.append(button(800, 270, 200, 50, "Reset", white, black))
        self.button_list.append(button(750, 340, 300, 50, "Automated (BFS)", white, black))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed and not self.win:
                self.start_game = False
                self.win = True
                if self.high_score > 0:
                    self.high_score = min(self.high_score, self.elapesd_time)
                else:
                    self.high_score = self.elapesd_time
                self.save_high_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapesd_time = time.time() - self.timer

        self.all_sprites.update()

        if self.start_random:
            self.random()
            self.draw_tiles()
            self.random_time += 1
            if self.random_time >= 60:
                self.start_random = False
                self.start_game = True
                self.start_timer = True

                

    def draw_grid(self):
        for row in range(-1, gamesize*tilesize, tilesize):
            pygame.draw.line(self.screen, blue, (row, 0), (row, gamesize*tilesize))

        for col in range(-1, gamesize*tilesize, tilesize):
            pygame.draw.line(self.screen, blue, (0, col), (gamesize*tilesize, col))

    def draw(self):
        self.screen.fill(bgcolour)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.button_list:
            button.draw(self.screen)

        # self.test.draw(self.screen)
        # self.button.draw(self.screen)

        uielement(600, 0, "High score: %0.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        uielement(925, 70, "%0.3f" % self.elapesd_time).draw(self.screen)
        if self.win:
            uielement(600, 70, "You win at:").draw(self.screen)          
            
        pygame.display.flip()

    def get_state_from_grid(self):
        return tuple(tuple(row) for row in self.tiles_grid)

    def animate_solution(self, solution_path):
        for state in solution_path:
            self.tiles_grid = [list(row) for row in state]
            self.draw_tiles()
            self.draw()
            pygame.time.delay(300)

    def bfs(self, start_state, goal_state):
        def get_neighbors(state):
            neighbors = []
            size = len(state)
            for r in range(size):
                for c in range(size):
                    if state[r][c] == 0:
                        empty_pos = (r, c)
                        break
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            for dr, dc in directions:
                nr, nc = empty_pos[0] + dr, empty_pos[1] + dc
                if 0 <= nr < size and 0 <= nc < size:
                    new_state = [list(row) for row in state]
                    new_state[empty_pos[0]][empty_pos[1]], new_state[nr][nc] = new_state[nr][nc], new_state[empty_pos[0]][empty_pos[1]]
                    neighbors.append(tuple(tuple(row) for row in new_state))
            return neighbors

        queue = deque()
        visited = set()
        parent = {}

        queue.append(start_state)
        visited.add(start_state)
        parent[start_state] = None

        while queue:
            current = queue.popleft()

            if current == goal_state:
                path = []
                while parent[current] is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path

            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        return []

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col+1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col+1] = self.tiles_grid[row][col+1], self.tiles_grid[row][col]
                            if tile.left() and self.tiles_grid[row][col-1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col-1] = self.tiles_grid[row][col-1], self.tiles_grid[row][col]
                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
                            if tile.dwon() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                            self.draw_tiles()

                for button in self.button_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Random":
                            self.random_time = 0
                            self.start_random = True
                            self.win = False

                        if button.text == "Reset":
                            self.new()
                        if button.text == "Automated (BFS)":
                            start = self.get_state_from_grid()
                            goal = tuple(tuple(row) for row in self.tiles_grid_completed)
                            solution_path = self.bfs(start, goal)
                            self.animate_solution(solution_path)
                        if button.text == "Clean High Score":
                            self.high_score = 0
                            self.save_high_score()


game = Game()
while True:
    game.new()
    game.run()
