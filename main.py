import pygame
import random
import time
from behave import *
from setting import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
    #     self.running = True
    #     self.board = Board(gamesize, tilesize, bgcolour)
    #     self.sprites = pygame.sprite.Group()
    #     self.sprites.add(self.board)

    # def run(self):
    #     while self.running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 self.running = False
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_ESCAPE:
    #                     self.running = False
    #                 elif event.key == pygame.K_SPACE:
    #                     self.board.shuffle()

    #         self.screen.fill(bgcolour)
    #         self.sprites.update()
    #         self.sprites.draw(self.screen)
    #         pygame.display.flip()
    #         self.clock.tick(FPS)

    #     pygame.quit()

    def new(self):
        pass

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def draw_grid(self):
        for row in range(-1, gamesize*tilesize, tilesize):
            pygame.draw.line(self.screen, blue, (row,0), (row, gamesize*tilesize))

        for col in range(-1, gamesize*tilesize, tilesize):
            pygame.draw.line(self.screen,blue, (0, col), (gamesize*tilesize, col))


    def draw(self):
        self.screen.fill(bgcolour)
        self.draw_grid()
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

game = Game()
while True:
    game.new()
    game.run()