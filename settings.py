class Settings():

    """A class to store all settings for Alien Invasion."""
    def __init__(self):

       """Initialize the game's settings."""
       # Screen settings
       self.screen_width = 800
       self.screen_height = 600
       self.bg_color = (102, 255, 102)
       #ship settings
       self.ship_limit = 3
       self.ship_speed_factor = 1
       # Bullet settings
       self.bullet_speed_factor = 3
       self.bullet_speed_factor2=1
       self.bullet_width = 3
       self.bullet_height = 20
       self.bullet_color = 60, 60, 60
       self.bullets_allowed = 20
       self.direzione=True
       self.direzione2=True
       # Alien settings
       self.alien_speed_factor = 0.2
       self.fleet_drop_speed = 10
       # fleet_direction of 1 represents right; -1 represents left.
       self.fleet_direction = 1
       # How quickly the game speeds up
       self.speedup_scale = 1.5
       # How quickly the alien point values increase
       self.score_scale = 1.5
       self.initialize_dynamic_settings()
       #Wall settings
       self.wall_width=150
       self.wall_height=10
       self.wall_color=255,0,0
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.2
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50
    

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
