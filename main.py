import pygame
import random
import time
from behave import *
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = Board(gamesize, tilesize, bgcolour)
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.board)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.board.shuffle()

            self.screen.fill(bgcolour)
            self.sprites.update()
            self.sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

