import pygame
from pygame.sprite import Sprite

from random import randint

class Bomby(Sprite):
    """A class to manage explosives."""
    
    def __init__(self, ai_game):
        """Initialize explosive and its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load the bomb image 
        self.image = pygame.image.load("images/bomb.bmp")
        
        # Resize image and get its rect.
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
        # Position bomb in upper half of screen (random)
        rightBound = self.screen_rect.right - self.rect.width
        self.rect.x = randint(10, rightBound)
        lowBound = self.screen_rect.height / 2
        self.rect.y = randint(10, lowBound + 10)
        
    def blitme(self):
        """Draw the bomb at its current location."""
        self.screen.blit(self.image, self.rect)
        
    def explode(self):
        """Bomb blows up neighboring aliens."""
        centerx, centery = self.rect.centerx, self.rect.centery
        self.image = pygame.image.load("images/explosion.bmp")
        self.image = pygame.transform.scale(self.image, (150, 200))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery