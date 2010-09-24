# INTIALISATION
import pygame, math, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
pygame.display.set_caption("Dive")

def clamp (x, min, max):
  if x > max:
    return max
  if x < min:
    return min
  return x

class DiverSprite(pygame.sprite.Sprite):
    MAX_SPEED = 100
    NOP = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.x_speed = 0
        self.y_speed = 0
        self.xdir = self.NOP;
        self.ydir = self.NOP;

    def update(self, deltat):
        # SIMULATION
        self.rect = self.image.get_rect()

        if self.xdir == self.RIGHT:
          self.addXSpeed(4)
        elif self.xdir == self.LEFT:
          self.addXSpeed(-4)
        else:
          self.xFriction(2)

        if self.ydir == self.UP:
          self.addYSpeed(-4)
        elif self.ydir == self.DOWN:
          self.addYSpeed(4)
        else:
          self.yFriction(2)

#disable this below for HARD

        self.move(self.x_speed/10, self.y_speed/10)

        self.rect.center = self.position

    def addXSpeed(self, xdiff):
        self.x_speed += xdiff
        self.x = clamp(self.x_speed, -self.MAX_SPEED, self.MAX_SPEED)

    def addYSpeed(self, ydiff):
        self.y_speed += ydiff
        self.y = clamp(self.y_speed, -self.MAX_SPEED, self.MAX_SPEED)

    def setXDir(self, xdir):
        self.xdir = xdir

    def setYDir(self, ydir):
        self.ydir = ydir

    def xFriction(self, diff):
        if self.x_speed > 0:
          self.addXSpeed(- min(2, self.x_speed))
        elif self.x_speed < 0:
          self.addXSpeed(min(2, -self.x_speed))
    def yFriction(self, diff):
        if self.y_speed > 0:
          self.addYSpeed(- min(2, self.y_speed))
        elif self.y_speed < 0:
          self.addYSpeed(min(2, -self.y_speed))

    def move(self, xdiff, ydiff):
        x = self.position[0] + xdiff
        y = self.position[1] + ydiff
        self.position = (x,y)

rect = screen.get_rect()
car = DiverSprite('triangle.png', rect.center)
car_group = pygame.sprite.RenderPlain(car)
while 1:
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        if event.type == KEYDOWN:
          if event.key == K_RIGHT: car.setXDir(DiverSprite.RIGHT)
          elif event.key == K_LEFT: car.setXDir(DiverSprite.LEFT)
          elif event.key == K_UP: car.setYDir(DiverSprite.UP)
          elif event.key == K_DOWN: car.setYDir(DiverSprite.DOWN)
          elif event.key == K_ESCAPE: sys.exit(0)
        elif event.type == KEYUP:
          if event.key == K_RIGHT: car.setXDir(DiverSprite.NOP)
          elif event.key == K_LEFT: car.setXDir(DiverSprite.NOP)
          elif event.key == K_UP: car.setYDir(DiverSprite.NOP)
          elif event.key == K_DOWN: car.setYDir(DiverSprite.NOP)
    # RENDERING
    screen.fill((127,127,127))
    car_group.update(deltat)
    car_group.draw(screen)
    pygame.display.flip()

