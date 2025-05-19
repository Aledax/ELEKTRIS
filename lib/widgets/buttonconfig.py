from lib.scenes.sceneconfig import *

from lib.utils.pygameplus import *


# Dimensions


BUTTON_BORDER_RATIO = 0.005 # As a portion of the screen width
BUTTON_TEXT_SIZE_RATIO = 0.5 # As a portion of the button height
BUTTON_TEXT_HIGHLIGHT_RATIO = 1 # As a portion of the defualt text size

BUTTON_BORDER = int(WINDOW_WIDTH * BUTTON_BORDER_RATIO)


# Colors


BUTTON_COLOR_BACKGROUND_DEFAULT = (*COLOR_BASE, 50)
BUTTON_COLOR_BACKGROUND_HIGHLIGHT = (*COLOR_BASE, 100)
BUTTON_COLOR_BORDER_DEFAULT = (*COLOR_BASE, 225)
BUTTON_COLOR_BORDER_HIGHLIGHT = (*COLOR_BASE, 255)

BUTTON_COLOR_TEXT_DEFAULT = color_lighten(COLOR_BASE, 0.3)
BUTTON_COLOR_TEXT_HIGHLIGHT = (255, 255, 225)