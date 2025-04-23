import pygame
from setting import *

pygame.font.init()

class tile(pygame.sprite.Sprite):
     def __init__(self,game, x, y, text):
          self.group = game.all_sprites
          pygame.sprite.Sprite.__init__(self, self.group)
          self.game = game
          self.image = pygame.Surface((tilesize, tilesize))
          self.x, self.y = x,y
          self.text = text
          self.rect = self.image.get_rect()
          if self.text != "empty":
               self.font = pygame.font.SysFont("Consolas", 50)
               font_surface = self.font.render(self.text, True, black)
               self.image.fill(white)
               self.font_size = self.font.size(self.text)
               draw_x = (tilesize/2) - self.font_size[0]/2
               draw_y = (tilesize/2) - self.font_size[1]/2
               self.image.blit(font_surface,(draw_x, draw_y))         

          else:               
               self.image.fill(bgcolour)
          

     def update(self):
          self.rect.x = self.x * tilesize
          self.rect.y = self.y * tilesize


     def click(self, mouse_x, mouse_y):
           return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
          

          
     def right(self):
          return self.rect.x + tilesize < gamesize * tilesize

     def left(self):
          return self.rect.x - tilesize >= 0

     def up(self):
          return self.rect.y - tilesize >= 0

     def dwon(self):
          return self.rect.y + tilesize < gamesize * tilesize


class uielement:
     def __init__(self,x,y,text):
          self.x, self.y = x,y       
          self.text = text
          
     def draw(self, screen):
          font = pygame.font.SysFont("Consolas", 50)
          text = font.render(self.text, True, white)
          screen.blit(text, (self.x, self.y))   

class button:
     def __init__(self, x, y, width, height, text, colour, text_colour):
          self.colour = colour
          self.width = width
          self.height = height          
          self.x = x
          self.y = y 
          self.text = text
          self.text_colour = text_colour


     def draw(self, screen):
          pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
          font = pygame.font.SysFont("Consolas", 30)          
          text = font.render(self.text, True, self.text_colour)
          self.font_size = font.size(self.text)
          draw_x = self.x + (self.width/2) - self.font_size[0]/2
          draw_y = self.y + (self.height/2) - self.font_size[1]/2
          screen.blit(text,(draw_x, draw_y))    

     def click(self, mouse_x, mouse_y):
           return self.x<= mouse_x <= self.x+ self.width and self.y <= mouse_y <= self.y + self.height



         
          