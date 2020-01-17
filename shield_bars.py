import pygame


def draw_shield_bar_demon(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 50
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, pygame.Color('red'), fill_rect)


def draw_shield_bar_mobs(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 6
    fill = (pct / 100) * BAR_LENGTH
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, pygame.Color('blue'), fill_rect)