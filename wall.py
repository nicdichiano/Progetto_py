import pygame
from pygame.sprite import Sprite
class Wall(Sprite):

    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen):

        """Create a bullet object at the ship's current position."""
        super(Wall, self).__init__()
        self.screen = screen
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(200, 120, ai_settings.wall_width,ai_settings.wall_height)
        

 
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        #self.y = float(self.rect.y)
        self.color = ai_settings.wall_color
        #self.speed_factor = ai_settings.bullet_speed_factor
    def draw_wall(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)