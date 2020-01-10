import pygame


class Camera(object):
    def __int__(self, screen, player, level_w, level_h):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.center = self.player.center
        self.world_rect = pygame.Rect(0, 0, level_w, level_h)

    def update(self):
        if self.player.centerx > self.rect.centerx + 25:
            self.rect.centerx = self.player.centerx - 25
        if self.player.centerx < self.rect.centerx - 25:
            self.rect.centerx = self.player.centerx + 25
        if self.player.centery > self.rect.centery + 25:
            self.rect.centery = self.player.centery - 25
        if self.player.centery < self.rect.centery - 25:
            self.rect.centery = self.player.centery + 25
        self.rect.clamp_ip(self.world_rect)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, pygame.RelRect(s, self))
