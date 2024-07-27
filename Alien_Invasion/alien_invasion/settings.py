class Settings:
    """A class to static settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60, 160)
        
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        
        # Probability of initializing a 'buff' alien (0 to 1)
        self.buff_chance = 0.2
        #self.initialize_dynamic_settings()

        # Number of bombs per round
        self.num_bombs = 3
        
    def initialize_dynamic_settings(self, difficulty):
        """Initialize the settings that change throughout the game."""
        if difficulty == "Easy":
            self.easymode_settings()
        elif difficulty == "Mid":
            self.midmode_settings()
        elif difficulty == "Hard":
            self.hardmode_settings()
            
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        self.powerup_speed = 2 * self.alien_speed

        # Scoring settings
        self.alien_points = 50
        self.score_mult = 1
        
        self.powerup_wait = 12.0
        
        # Music settings
        self.play_music = True
        self.sound_effects = True
        
    def easymode_settings(self):
        """Initialize settings for the lowest difficulty."""
        self.ship_speed = 1.5
        self.bullet_speed = 9
        self.alien_speed = 1.10
        
    def midmode_settings(self):
        """Initialize settings for medium difficulty"""
        self.ship_speed = 2.25
        self.bullet_speed = 10
        self.alien_speed = 2.32

        
    def hardmode_settings(self):
        """Initialize settings for the highest difficulty"""
        self.ship_speed = 3
        self.bullet_speed = 11
        self.alien_speed = 3.43
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= (self.speedup_scale)
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.mod_alien_points = self.alien_points
        # print(self.alien_points)

        if self.buff_chance < 0.75:
            self.buff_chance *= self.speedup_scale
            
    def nullify_powerups(self):
        """Undoes the "buffs" the powerups cause."""
        self.bullets_allowed = 3
        self.score_mult = 1