import pygame
from pygame.locals import *
import sys
import threading
import players
from settings import *


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if players.player_no == 1:
            x = 0
            players.player_no = 2
        else:
            x = SCREEN_WIDTH - BAR_WIDTH
            players.player_no = 1
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
        if players.player_game_state_update:
            players.player_game_state = OP_CODES[0] + "," + str((self.rect.top))


def load_image(image, location):
    image = pygame.image.load(image).convert()
    rect = image.get_rect()
    rect.left, rect.top = location
    return image, rect

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    background_image, background_rect = load_image("bg.png", [0, 0])

    clock = pygame.time.Clock()
    player_bar = Bar()
    opponent_bar = Bar()
    to_update_sprites = pygame.sprite.RenderPlain(player_bar)
    to_draw_sprites = pygame.sprite.RenderPlain(player_bar, opponent_bar)

    while players.going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                players.going = False
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            player_bar.up = True
            players.player_game_state_update = True
        if keys[K_DOWN]:
            player_bar.down = True
            players.player_game_state_update = True
        if players.opponent_game_state_update:
            opcode, data = players.opponent_game_state.split(",")
            data = int(data)
            if opcode == OP_CODES[0]:
                opponent_bar.rect.top = data
            players.opponent_game_state_update = False

        to_update_sprites.update()
        screen.blit(background_image, background_rect)
        to_draw_sprites.draw(screen)
        pygame.display.flip()
