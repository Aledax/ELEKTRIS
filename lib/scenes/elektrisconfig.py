import numpy as np

from lib.scenes.sceneconfig import *


# Animation


TRANSITION_TIME = 0.33
TRANSITION_PROGRESS_FUNCTION = lambda t: -0.5 * np.cos(t / TRANSITION_TIME * np.pi) + 0.5


# Colors


TRANSITION_COLOR = (0, 0, 0)
