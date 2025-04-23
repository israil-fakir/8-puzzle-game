import pygame
import random
import time
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
                

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile_val in enumerate(x):
                if tile_val != 0:  
                    self.tiles[row].append(tile(self, col,row, str(tile_val)))
                else:
                    self.tiles[row].append(tile(self, col,row, "empty"))
                    
                
        # [
        #     [1,2,3],
        #     [4,5,6],
        #     [7,8,0]
        # ]


    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.button_list = []
        self.button_list.append(button(700, 100, 200, 50, "Random", white, black))
        self.button_list.append(button(700, 180, 200, 50, "Reset", white, black))
        self.draw_tiles()
        # self.test = uielement(1000,450,"test")
        # self.button = button(400,400, 200, 100, "test", white, black)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, gamesize*tilesize, tilesize):
            pygame.draw.line(self.screen, blue, (row,0), (row, gamesize*tilesize))

        for col in range(-1, gamesize*tilesize, tilesize):
            pygame.draw.line(self.screen,blue, (0, col), (gamesize*tilesize, col))


    def draw(self):
        self.screen.fill(bgcolour)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.button_list:
            button.draw(self.screen)

        # self.test.draw(self.screen)
        # self.button.draw(self.screen)
        pygame.display.flip()

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
                                self.tiles_grid[row][col], self.tiles_grid[row][col+1] =   self.tiles_grid[row][col+1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col-1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col-1] =   self.tiles_grid[row][col-1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] =   self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
                            
                            if tile.dwon() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] =   self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                            self.draw_tiles()
                                
                for button in self.button_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Random":
                            self.random_time = 0
                            self.start_random = True

                        if button.text == "Reset":
                            self.new()




game = Game()
while True:
    game.new()
    game.run()