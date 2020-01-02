import pygame
from pygame.locals import *
import sys
from players import *
from settings import *


def load_image(image, location):
    image = pygame.image.load(image).convert()
    rect = image.get_rect()
    rect.left, rect.top = location
    return image, rect


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global player_no
        if player_no == 1:
            x = 0
            player_no=2
        else:
            x = SCREEN_WIDTH - BAR_WIDTH - 9
            player_no=1
        y = int(SCREEN_HEIGHT / 2 - BAR_HEIGHT)
        location = (x, y)
        self.image, self.rect = load_image("bar.png", location)
        self.up = False
        self.down = False

    def update(self):
        if self.up:
            self.rect.top -= 13
            self.up = False
        if self.down:
            self.rect.top += 13
            self.down = False
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
    background_image, background_rect = load_image("bg.png", [0, 0])

    clock = pygame.time.Clock()
    player_bar = Bar()
    opponent_bar=Bar()
    allsprites = pygame.sprite.RenderPlain(player_bar,opponent_bar)

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_bar.up = True
        if keys[pygame.K_DOWN]:
            player_bar.down = True

        allsprites.update()
        screen.blit(background_image, background_rect)
        allsprites.draw(screen)
        pygame.display.flip()
