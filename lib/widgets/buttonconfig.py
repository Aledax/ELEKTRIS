from lib.scenes.sceneconfig import *

from lib.utils.pygameplus import *


# Dimensions


BUTTON_BORDER_RATIO = 0.005 # As a portion of the screen width
BUTTON_TEXT_SIZE_RATIO = 0.5 # As a portion of the button height
BUTTON_TEXT_HIGHLIGHT_RATIO = 1 # As a portion of the defualt text size

BUTTON_BORDER = int(WINDOW_WIDTH * BUTTON_BORDER_RATIO)


# Colors


def generate_color_index(color_base):

    color_index = {}

    color_index['background-default'] = (*color_base, 50)
    color_index['background-highlight'] = (*color_base, 100)
    color_index['border-default'] = (*color_base, 225)
    color_index['border-highlight'] = (*color_base, 255)

    color_index['text-default'] = color_lighten(color_base, 0.3)
    color_index['text-highlight'] = (255, 255, 225)

    return color_index