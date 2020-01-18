import pygame

GREEN = pygame.Color('green')
WHITE = pygame.Color('white')


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


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 30
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
