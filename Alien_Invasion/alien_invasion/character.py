import pygame

from settings import Settings

class Character:
    """A class to manage the ship driver"""
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load character image and get its rect
        self.image = pygame.image.load('images/smiley-face-.bmp')
        self.image = pygame.transform.scale(self.image, (25.0,25.0))
        self.rect = self.image.get_rect()
        
        # Match background color
        self.bg_color = Settings().bg_color

        # Start cgharacter at the center of the screen
        self.rect.center = self.screen_rect.center
        
    def blitme(self):
        """Draw the character at its current location"""
        self.screen.blit(self.image, self.rect)



