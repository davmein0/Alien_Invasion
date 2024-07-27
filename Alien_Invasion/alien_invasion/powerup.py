import pygame

class Powerup:
    """A class to make powerups for the game."""
    
    def __init__(self, ai_game, type):
        """Initialize powerups and set the starting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.type = type
        
        # Load the image and get its rect
        self.pick_powerup_type()
        self.rect = self.image.get_rect()
        
        # Start powerups at the top left of the screen
        self.rect.x = -60
        self.rect.y = 70
        
        # Store a float for the powerup's exact horizontal position
        self.x = float(self.rect.x)
        
        # Start powerups stationary
        self.active = False
            
    def pick_powerup_type(self):
        """Shows appropriate image, based on powerup type."""
        if self.type == "ammo":
            self.image = pygame.image.load('images/ammo.bmp')
        elif self.type == "2score":
            self.image = pygame.image.load('images/X2_Multiplier.bmp')
        else:
            self.image = pygame.image.load('images/Smiley_face.bmp')
            
    def reset(self):
        """Hides powerup and initiates the powerup"""
        self.active = False
        self.x = -60
        self.rect.x = self.x

     
    def update(self):
        """Powerup moves across the screen."""
        if self.active:
            self.x += self.settings.powerup_speed
            self.rect.x = self.x
        
    def score_mult(self):
        """Doubles the points of each alien shot down."""

        
    def blitme(self):
        """Draw the powerup at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_offscreen(self):
        if self.rect.left > self.screen_rect.right:
            self.reset()