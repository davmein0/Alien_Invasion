from pathlib import Path

class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.path = ai_game.path
        
        # High score should never be reset.
        self.set_highscore()
        
    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def set_highscore(self):
        """Reads highscore from file, converts to an int."""
        try:
            self.high_score = self.path.read_text()
        except FileNotFoundError:
            self.high_score = 0
        else:
            self.high_score = self.high_score.replace(",", "")
            self.high_score = int(self.high_score)