import pygame.font
class Button():

    def __init__(self, ai_settings, screen, msg):

        """Initialize button attributes."""
        #self.screen_width = 800
        #self.screen_height = 600
        #self.bg_color = (100, 200, 100)

        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Set the dimensions and properties of the button.
        self.width, self.height = 200,50
        self.button_color = (255,0, 0)
        self.text_color = (0, 0, 255)
        self.font = pygame.font.SysFont('italic', 25)
 
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # The button message needs to be prepped only once.
        self.prep_msg(msg)
        #self.draw_button()

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        # Draw blank button and then draw message.
        #print('disegna')
        self.screen.fill(self.button_color, self.rect)
        #print(self.screen.fill)
        self.screen.blit(self.msg_image, self.msg_image_rect)