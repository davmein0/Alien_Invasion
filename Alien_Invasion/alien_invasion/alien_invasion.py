import sys
from time import sleep
from pathlib import Path

from random import randint

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from bomb import Bomby
from powerup import Powerup
#from character import Character

class AlienInvasion:
    """Overall class to manage game assets 
and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        #print(self.settings.screen_width) 
        
        # Create filehandle to the highscore text document.
        self.path = Path('high_score.txt')       

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        # Create an instance to store game statistics 
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        #self.character = Character(self)

        self._create_fleet()
        
        self.powerups = [Powerup(self, "2score"), Powerup(self, "ammo")]
        # self.score_buff = Powerup(self, "2score")
        # self.ammo_buff = Powerup(self, "ammo")
        self.set_bombs()
        
        
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        
        # Make the Play button.
        # self.play_button = Button(self, "Play")
        
        # Make difficulty buttons
        self._create_level_buttons()
        
        # Initialize sound effect handles 
        self.sfx = {"buffed": pygame.mixer.Sound("sounds/buffed.mp3"),
                    "shot": pygame.mixer.Sound("sounds/shot.wav"),
                    "alien_hit": pygame.mixer.Sound("sounds/alien_hit.mp3"),
                    "level_up": pygame.mixer.Sound("sounds/level_up.mp3"),
                    "lost_life": pygame.mixer.Sound("sounds/lost_life.wav")}

        # Load and play opening music
        self.music = pygame.mixer.music
        self.music.load("sounds/Intro_music.mp3")
        self.music.play(-1)
        
        self.just_started = True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_powerups()
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        """Respond to  keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.path.write_text(self.sb.high_score_str)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # self._check_play_button(mouse_pos)
                self._check_level_buttons(mouse_pos)
               

    def _create_level_buttons(self):
        """Create and position buttons that determine game's difficulty"""
        # Create buttons for easy, medium, and hard difficulties
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")
        
        # Reposition hard, easy buttons
        self.easy_button.rect.x -= 400
        self.easy_button.msg_image_rect.x -= 400
        self.hard_button.rect.x += 400
        self.hard_button.msg_image_rect.x += 400

    def display_difficulty_buttons(self):
        """Draw the easy, medium, and hard difficulty buttons"""
        self.easy_button.draw_button()
        self.medium_button.draw_button()
        self.hard_button.draw_button()
        
    def _check_level_buttons(self, mouse_pos):
        """Checks which difficulty player starts game at"""
        mode = "none"
        easyButton_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        midButton_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hardButton_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        
        if not self.game_active:
            if easyButton_clicked:
                mode = "Easy"
            elif midButton_clicked:
                mode = "Mid"
            elif hardButton_clicked:
                mode = "Hard"
                
        if mode != "none":
            self.settings.initialize_dynamic_settings(mode)
            self._start_game()
                
    # def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        #playbutton_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #if playbutton_clicked and not self.game_active:
            # Check if difficulty buttons clicked.

            # Reset the game settings.
            ##self.settings.initialize_dynamic_settings()
            #self._start_game()
            
    def _start_game(self):
        """Starts a new game by resetting aspects."""
        # Reset the game statistics
        self.stats.reset_stats()
        self.sb.prep_images()
        self.game_active = True
        
        # Determine when to start activating powerups
        self.activate_powerups()
        
        if self.just_started == False:
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            self.bombs.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.just_started = True
        self.ship.center_ship()
            
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Switch music
        pygame.mixer.music.load("sounds/main_music.mp3")
        pygame.mixer.music.play(-1)
        
    def activate_powerups(self):
        # Reset the clock's time passed
        self.start_time = pygame.time.get_ticks()
        
        
        # Adds some uncertainty to when powerup will activate
        time_variance = randint(-3, 3)
        self.time_buffer = 1000 * (self.settings.powerup_wait + time_variance)
        # print (self.time_buffer)
        
        # Determines which powerup will be activated
        #self.lot_num = randint(1, 100)
        
    def _update_powerups(self):
        """Updates position of powerups."""
        powerup_activated = False
        
        for powerup in self.powerups:
            
            if powerup.active == True:
                powerup_activated = True
                powerup.update()
                
            bullet = pygame.sprite.spritecollideany(powerup, self.bullets)
            if bullet:
                self.bullets.remove(bullet)
                powerup.reset()
                
                if powerup.type == "ammo" and self.settings.bullets_allowed > 1:
                    self.settings.bullets_allowed -= 1
                elif powerup.type == "2score" and self.settings.score_mult < 8:
                    self.settings.score_mult *= 2
                    
                # Add sound effects
                pygame.mixer.Sound.play(self.sfx["buffed"])
                
            powerup.check_offscreen()
            
        if pygame.time.get_ticks() - self.start_time > self.time_buffer and not powerup_activated:
            lot_num = randint(1, len(self.powerups))
            self.powerups[lot_num - 1].active = True
            self.activate_powerups()

        
        # Check whether either powerup has been hit.
        # if pygame.sprite.spritecollideany(self.ammo_buff, self.bullets):
            # self.ammo_buff.got_hit()
        # if pygame.sprite.spritecollideany(self.score_buff, self.bullets):
            # self.score_buff.got_hit()
        
                    
    def _check_keydown_events(self, event):
        """Responds to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.path.write_text(self.sb.high_score_str)
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_m:
            self.off_on_music()
        elif event.key == pygame.K_s:
            self.off_on_sfx()
        #elif event.key == pygame.K_p and self.game_active == False:
            #self._start_game()
            
    def _check_keyup_events(self, event):
        """Responds to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def off_on_music(self):
        """Turns the music on or off, depending on its current state."""
        if self.settings.play_music:
            self.music.set_volume(0)
            self.settings.play_music = False
        else:
            self.music.set_volume(100)
            self.settings.play_music = True
            
    def off_on_sfx(self):
        """Turns sound effects on or off"""
        if self.settings.sound_effects:
            for sound_effect in self.sfx.values():
                sound_effect.set_volume(0.0)
            self.settings.sound_effects = False
        else:
            for sound_effect in self.sfx.values():
                sound_effect.set_volume(1.0)
            self.settings.sound_effects = True
            
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
            # Add sound effect
            pygame.mixer.Sound.play(self.sfx["shot"])
            
    def _update_bullets(self):
        """Update position of bullets and get ride of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))

        self._check_bullet_alien_collisions()
        self._check_bullet_bomb_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Removate any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, False)
        
        
        # Update scores
        if collisions:
            for aliens in collisions.values():
                alien_points = self.settings.alien_points * self.settings.score_mult
                self.stats.score += len(aliens) * alien_points
                
                 
                # If alien is buff, downgrade
                for alien in aliens:
                    if alien.buff == True:
                        alien.demote()
                    else:
                        alien.remove(self.aliens)
                        
            # Add sound effect
            pygame.mixer.Sound.play(self.sfx["alien_hit"])

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.start_new_level()
            
    def _check_bullet_bomb_collisions(self):
        """Respond to bullet-bomb collisions."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.bombs, True, False)
        
        if collisions:
            for bombs in collisions.values():
                for bomb in bombs:
                    bomb.explode()
                    blast_zone = pygame.sprite.spritecollide(
                        bomb, self.aliens, True)
                    if blast_zone:
                        self.stats.score += self.settings.alien_points * len(blast_zone)
                        self.sb.prep_score()
                        self.sb.prep_high_score()
                    self.bombs.remove(bomb)
        

    def start_new_level(self):
        """Creates environment for next level."""
        # Add sound effect.
        pygame.mixer.Sound.play(self.sfx["level_up"])
        
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self.bombs.empty()
        self._create_fleet()
        self.settings.increase_speed()
            
        # Set mines
        self.set_bombs()
        
        # Reset clock and powerups
        self.activate_powerups()
        for powerup in self.powerups:
            powerup.reset()
            
        self.settings.nullify_powerups()
        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()
        

    def set_bombs(self):
        """Create __ many bombs."""
        for x in range (0, self.settings.num_bombs):
            bomb = Bomby(self)
            self.bombs.add(bomb)
        
    def _update_aliens(self):
        """Check if the fleet is at an edge, then Update the positions"""
        self._check_fleet_edges()
        self.aliens.update()
        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens"""
        """
        Make an alien and keep on adding aliens
        until there's no room left.
        """
        # Spacing between aliens is one alien width and one alien height.width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 3 * alien_width):
                # print("f")
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement ships_left, and update scoreboard.
        self.stats.ships_left -= 1;
        self.sb.prep_ships()
    
        if self.stats.ships_left > 0:
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            self.bombs.empty()
            
            for powerup in self.powerups:
                powerup.reset()
        
            self.settings.nullify_powerups()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.set_bombs()
            self.ship.center_ship()
        
            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mixer.music.load("sounds/Intro_music.mp3")
            pygame.mixer.music.play(-1)
            pygame.mouse.set_visible(True)
            
        # Add sounds effect
        pygame.mixer.Sound.play(self.sfx["lost_life"])

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.bombs.draw(self.screen)
        for powerup in self.powerups:
            powerup.blitme()
        #self.character.blitme()

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive and hasn't been clicked
        #if not (self.game_active and self.playbutton_clicked):
            #self.play_button.draw_button()
        # Draw difficulty buttons if playbutton clicked but game not active
        if not self.game_active:
            self.display_difficulty_buttons()
            
        pygame.display.flip()
         

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()