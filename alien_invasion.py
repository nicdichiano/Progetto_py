import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from wall import Wall

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    
    #play_button.draw_button()
    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    play_button = Button(ai_settings, screen, "Play")
    #giocatore=1
    ship = Ship(ai_settings,screen)
    #giocatore=2
    ship2=Ship(ai_settings,screen)
    # Make a group to store bullets in.
    bullets = Group()
    bullets2=Group()
    walls=Group()
    # Make an alien.
    #alien = Alien(ai_settings, screen)
    aliens = Group() 
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen,ship, aliens)
    #create walls
    gf.create_wall(ai_settings,screen,walls)
    # Start the main loop for the game.
    gf.update_screen(ai_settings, screen, stats, sb, ship,ship2, aliens,bullets,bullets2, play_button,walls)
    stats.game_active=False
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,ship2,aliens, bullets,bullets2)
        
        if stats.game_active:
            ship.update()
            ship2.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship,ship2, aliens,bullets,bullets2,walls)
            gf.update_aliens(ai_settings, screen,stats,sb, ship,ship2, aliens, bullets)
            gf.update_screen(ai_settings, screen, stats, sb, ship,ship2, aliens,bullets,bullets2, play_button,walls)
  
run_game()
