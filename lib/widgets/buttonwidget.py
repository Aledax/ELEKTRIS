import pygame
from pygame.locals import *
import numpy as np

from lib.widgets.buttonconfig import *
from lib.widgets.buttonassets import *


class ButtonWidget:


    STATE_IDLE = 0
    STATE_HOVERING = 1
    STATE_HOLDING = 2

    
    def __init__(self, position, centered, width_ratio, height_ratio, text, callbacks, args):

        
        self.width = WINDOW_WIDTH * width_ratio
        self.height = WINDOW_HEIGHT * height_ratio
        self.topleft = position if not centered else np.subtract(position, np.multiply(self.size, 0.5)).tolist()
        self.rect = (*self.topleft, *self.size)

        # Preparing the surfaces

        text_default_size = self.height * BUTTON_TEXT_SIZE_RATIO
        text_highlight_size = text_default_size * BUTTON_TEXT_HIGHLIGHT_RATIO
        default_font = pygame.font.Font(BUTTON_FONT_PATH, int(round(text_default_size)))
        highlight_font = pygame.font.Font(BUTTON_FONT_PATH, int(round(text_highlight_size)))
        text_default_surface = default_font.render(text, True, BUTTON_COLOR_TEXT_DEFAULT)
        text_highlight_surface = highlight_font.render(text, True, BUTTON_COLOR_TEXT_HIGHLIGHT)
        
        self.default_surface = pygame.surface.Surface(self.size).convert_alpha()
        self.highlight_surface = pygame.surface.Surface(self.size).convert_alpha()
        self._prepare_surface(self.default_surface, BUTTON_COLOR_BACKGROUND_DEFAULT, BUTTON_COLOR_BORDER_DEFAULT, text_default_surface)
        self._prepare_surface(self.highlight_surface, BUTTON_COLOR_BACKGROUND_HIGHLIGHT, BUTTON_COLOR_BORDER_HIGHLIGHT, text_highlight_surface)

        self.callbacks = callbacks
        self.args = args

        self.state = ButtonWidget.STATE_IDLE


    @property
    def size(self):
        return (self.width, self.height)
    

    def _prepare_surface(self, surface, background_color, border_color, text_surface):

        pygame.draw.rect(surface, border_color, (0, 0, self.width, BUTTON_BORDER))
        pygame.draw.rect(surface, border_color, (0, self.height - BUTTON_BORDER, self.width, BUTTON_BORDER))
        pygame.draw.rect(surface, border_color, (0, BUTTON_BORDER, BUTTON_BORDER, self.height - 2 * BUTTON_BORDER))
        pygame.draw.rect(surface, border_color, (self.width - BUTTON_BORDER, BUTTON_BORDER, BUTTON_BORDER, self.height - 2 * BUTTON_BORDER))
        pygame.draw.rect(surface, background_color, (BUTTON_BORDER, BUTTON_BORDER, self.width - 2 * BUTTON_BORDER, self.height - 2 * BUTTON_BORDER))
        
        blit_plus(text_surface, surface, (2, 2, 2, 2), (0.5, 0.5, 0.5, 0.5))


    def trigger(self):

        for i in range(len(self.callbacks)):
            self.callbacks[i](*self.args[i])


    def update(self, mouse_position, mouse_clicked):

        previous_state = self.state

        if point_in_rect(mouse_position, self.rect):
            if mouse_clicked:
                if previous_state == ButtonWidget.STATE_HOVERING:
                    self.trigger()
                    self.state = ButtonWidget.STATE_HOLDING
            else:
                self.state = ButtonWidget.STATE_HOVERING
        else:
            self.state = ButtonWidget.STATE_IDLE


    def render(self, parent_surface):

        surface = self.highlight_surface if self.state == ButtonWidget.STATE_HOVERING else self.default_surface
        parent_surface.blit(surface, self.topleft)