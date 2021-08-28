import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from wall import Wall



def check_events(ai_settings, screen, stats,sb, play_button, ship,ship2,aliens, bullets,bullets2):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:    
                check_keydown_events(event, ai_settings, screen,stats, ship,ship2, bullets,bullets2)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship,ship2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button,ship, aliens, bullets, mouse_x, mouse_y)
            


            
def check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens,bullets, mouse_x, mouse_y):

    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if  button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        #print('ciao')
        stats.reset_stats()
        stats.game_active = True 
        #reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()  
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()       

def check_keydown_events(event, ai_settings, screen,stats, ship,ship2, bullets,bullets2):
    """Respond to keypresses."""
    if event.key == pygame.K_l:
        
        ship2.moving_right = True
        ai_settings.direzione2=True
    elif event.key == pygame.K_a:
        ship2.moving_left = True
        ai_settings.direzione2=True
    elif event.key == pygame.K_h and ai_settings.direzione2==True:
        fire_bullet(ai_settings, screen, ship2, bullets2)
        if stats.game_active:
            pygame.mixer.music.load('sparo.mp3')
            pygame.mixer.music.play(1)

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        ai_settings.direzione=True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        ai_settings.direzione=True
    elif event.key == pygame.K_SPACE and ai_settings.direzione==True:
        fire_bullet(ai_settings, screen, ship, bullets)
        if stats.game_active:
            pygame.mixer.music.load('sparo.mp3')
            pygame.mixer.music.play(1)
    elif event.key == pygame.K_q:
            sys.exit()


def check_keyup_events(event,ship,ship2):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_l:
        ship2.moving_right = False
    elif event.key == pygame.K_a:
        ship2.moving_left = False


def update_screen(ai_settings, screen,stats,sb, ship,ship2,aliens, bullets,bullets2,play_button,walls):
    """Update images on the screen and flip to the new screen."""
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in bullets2.sprites():
        bullet.draw_bullet()
    for wall in walls.sprites():
        wall.draw_wall()
    ship.blitme()
    ship2.blitme()
    aliens.draw(screen)
    # Draw the play button if the game is inactive.
    #print(stats.game_active)
    # Draw the score information.
    sb.show_score()
    if  not stats.game_active:
        #print('ciao')
        play_button.draw_button()
    
        
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship,ship2, aliens, bullets,bullets2,walls):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.


    bullets.update(ai_settings.direzione)
    bullets2.update(ai_settings.direzione2)
    if ai_settings.direzione2==False:
        for bullet in bullets2.copy():
            if bullet.rect.bottom >= 600:
                bullets2.remove(bullet)
                ai_settings.direzione2=True
    if ai_settings.direzione==False:
        for bullet in bullets.copy():
            if bullet.rect.bottom >= 600:
                bullets.remove(bullet)
                ai_settings.direzione=True
        

        # Get rid of bullets that have disappeared.
    if ai_settings.direzione==True:
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        for bullet in bullets2.copy():
            if bullet.rect.bottom <= 0:
                bullets2.remove(bullet)
        rebound1,rebound2=check_bullet_wall_collisions(ai_settings, screen, walls, bullets,bullets2)
        if rebound1:
            ai_settings.direzione=False
        else:
            ai_settings.direzione=True
    if ai_settings.direzione2==True:
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        for bullet in bullets2.copy():
            if bullet.rect.bottom <= 0:
                bullets2.remove(bullet)
        rebound1,rebound2=check_bullet_wall_collisions(ai_settings, screen, walls, bullets,bullets2)
        if rebound2:
            ai_settings.direzione2=False
        else:
            ai_settings.direzione2=True

        

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,ship2,aliens, bullets,bullets2)
    
    
def check_bullet_alien_collisions(ai_settings, screen,stats,sb, ship,ship2, aliens, bullets,bullets2):

    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisions2 = pygame.sprite.groupcollide(bullets2, aliens, True, True)
    if collisions:
        pygame.mixer.music.load('collisione.wav')
        pygame.mixer.music.play(1)
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        ai_settings.direzione=True
    
    if collisions2:
        pygame.mixer.music.load('collisione.wav')
        pygame.mixer.music.play(1)
        for aliens in collisions2.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        ai_settings.direzione2=True
    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_bullet_wall_collisions(ai_settings, screen, walls, bullets,bullets2):
    rebound1 = pygame.sprite.groupcollide(bullets,walls, False, False)
    rebound2= pygame.sprite.groupcollide(bullets2, walls, False, False)
    return rebound1,rebound2


   
def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""  
    if len(bullets) < ai_settings.bullets_allowed:
                # Create a new bullet and add it to the bullets group.
                new_bullet = Bullet(ai_settings, screen, ship)
                bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.height=50
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number+80
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):

    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    ship.rect.height=60
    alien.rect.height=50
    number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.height)
    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def create_wall(ai_settings,screen,walls):
    wall1=Wall(ai_settings,screen)
    walls.add(wall1)
    wall2=Wall(ai_settings,screen)
    wall2.rect.x=wall2.rect.x+300
    walls.add(wall2)






def get_number_rows(ai_settings, ship_height, alien_height):

    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -(3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings,screen, stats,sb, ship,ship2, aliens, bullets):
    """Check if the fleet is at an edge,and then update the postions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    """Update the postions of all aliens in the fleet."""
    aliens.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship,ship2, aliens, bullets)
    if pygame.sprite.spritecollideany(ship2, aliens):
        ship_hit(ai_settings, screen, stats, sb,ship, ship2, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship,ship2, aliens, bullets)

def ship_hit(ai_settings, screen,stats,sb, ship,ship2, aliens, bullets):

    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1 
        #print(stats.ships_left)
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty() 
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        ship2.center_ship()
        ship2.center=ship2.center+100
        # Pause.
        sleep(0.5)
        ai_settings.direzione=True
        ai_settings.direzione2=True
    else:
        stats.game_active = False
        pygame.mixer.music.load('trombone.wav')
        pygame.mixer.music.play(1)
        pygame.mouse.set_visible(True)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen,stats,sb, ship,ship2, aliens, bullets):

    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship,ship2, aliens, bullets)
            break

def check_high_score(stats, sb):

    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()