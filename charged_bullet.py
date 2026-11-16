"""
Program Name: Alien Invasion - Charged Bullet
 Disukhi Ahmed
Purpose: Creates a larger bullet
"""

import pygame
from bullet import Bullet


class ChargedBullet(Bullet):
    """Represents a charged laser that inherits from Bullet."""

    def __init__(self, game) -> None:
        """Initialize a charged bullet."""
        super().__init__(game)

        self.image = pygame.transform.scale(
            self.image,
            (self.settings.charged_bullet_w, self.settings.charged_bullet_h)
        )

        self.rect = self.image.get_rect()
        self.rect.midbottom = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self) -> None:
        """Move the charged bullet upward."""
        self.y -= self.settings.charged_bullet_speed
        self.rect.y = int(self.y)