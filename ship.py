import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #self.giocatore=giocatore
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship1.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.image= pygame.transform.scale(self.image, (60, 60)) 
        # Start each new ship at the bottom center of the screen.
        #self.rect.centery = self.screen_rect.centery
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.rect.bottom +=400
        #if self.giocatore==1:
        self.rect.centerx +=194.5
        #else:
            #self.rect.centerx+=294.5

        self.center = float(self.rect.centerx)
        
        

        # Movement flag
        self.moving_right = False
        self.moving_left= False
        #speed
        #self.ship_speed_factor = 1.5

    def update(self):
        """Update the ship's position based on the movement flag."""
        #print(self.screen_rect.right+925)
        #print(self.center)
        if self.moving_right and self.center<1023.5:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left  and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        self.rect.centerx = self.center



    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx+284.5-30