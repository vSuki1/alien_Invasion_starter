import pygame
from settings import Settings

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w, self.settings.ship_h)
        )

        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False
        self.arsenal = arsenal

        self.dashes_left = self.settings.max_dashes

        self.shield_active = False  
        self.shields_left = 1      
        

    def _center_ship(self) -> None:
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)


    def update(self) -> None:
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
        self.rect.x = self.x

    def draw(self) -> None:
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)


        if self.shield_active:
            pygame.draw.rect(self.screen, (0, 150, 255), (self.rect.x, self.rect.y - 15, self.rect.width, 10))
    
    
    def fire(self) -> bool:
        return self.arsenal.fire_bullet()

    def fire_charged(self) -> bool:
         return self.arsenal.fire_charged_bullet()

    def dash(self) -> None:
        """Moves the ship using dash."""
        if self.dashes_left <= 0:
            return
        if self.moving_right:
            self.x += self.settings.dash_distance
            if self.x + self.rect.width > self.boundaries.right:
                self.x = self.boundaries.right - self.rect.width

        elif self.moving_left:
            self.x -= self.settings.dash_distance
            if self.x < self.boundaries.left:
                self.x = self.boundaries.left
        else:
            return

        self.rect.x = int(self.x)
        self.dashes_left -= 1
        print(self.dashes_left)

    def activate_shield(self) -> None:
        """Acivate shield if one is available."""
        if self.shields_left > 0 and self.shield_active == False:
            self.shield_active = True
            self.shields_left -= 1
            

    def check_collisions(self, aliens) -> bool:
        return pygame.sprite.spritecollideany(self, aliens) is not None
