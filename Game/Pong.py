import pygame
from pygame.locals import *
import sys
from players import *
from settings import *


class Background(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("bg.png").convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Bar(pygame.sprite.Sprite):
    def __init__(self, no):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("bar.png").convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0,0)
        if no == 1:
            self.rect.left = 0
        else:
           self.rect.left = SCREEN_WIDTH-BAR_WIDTH-9
        self.rect.top = int(SCREEN_HEIGHT / 2 - BAR_HEIGHT)
        self.up=False
        self.down=False

    def update(self):
        if self.up:
            self.rect.top -= 13
            self.up=False
        if self.down:
            self.rect.top += 13
            self.down=False
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < PANEL_HEIGHT:
            self.rect.top = PANEL_HEIGHT


if __name__ == "__main__":
    player = Player()
    player.connect_to_server()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    background = Background([0, 0])

    clock = pygame.time.Clock()
    bar = Bar(player_no)
    allsprites = pygame.sprite.RenderPlain(bar)


    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            bar.up=True
        if keys[pygame.K_DOWN]:
            bar.down=True

        allsprites.update()
        screen.blit(background.image, background.rect)
        allsprites.draw(screen)
        pygame.display.flip()
                

