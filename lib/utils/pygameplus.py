import os
import pygame
import math
from pygame.locals import *


from .npplus import *


pygame.font.init()


def asset_path(assets_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', assets_path)


def load_image(assets_path):
    return pygame.image.load(asset_path(assets_path)).convert_alpha()


# blitPlus

# How to use:
#
# Values is a 4-parameter tuple.
# Parameter 0: X value of the background surface to blit onto
# Parameter 1: Y value of the background surface to blit onto
# Parameter 2: X value of the image surface to blit from
# Parameter 3: Y value of the image surface to blit from
#
# Modes is a 4-parameter tuple. 
# Parameter 0: Mode for translating the background surface X value
# Parameter 1: Mode for translating the background surface Y value
# Parameter 2: Mode for translating the image surface X value
# Parameter 3: Mode for translating the image surface Y value
#
# Each of the modes can be 0, 1, or 2.
# Mode 0: The corresponding value is the distance in pixels from the left/top of the surface.
# Mode 1: The corresponding value is the distance in pixels from the right/bottom of the surface.
# Mode 2: The corresponding value is the percentage across the surfaces width/height span from which to blit.
#
# For example, if you wanted to blit a small box on the bottom right corner of a background with a padding of
# 10 pixels, your modes would be (1, 1, 2, 2), and your values would be (10, 10, 1, 1).
#
# If you wanted to blit an image in the center of a background, your modes would be (2, 2, 2, 2), and your
# values would be (0.5, 0.5, 0.5, 0.5).
#
# Fractional coordinates are rounded.
#
# In the rotated version, all values are still based on the unrotated image's size.

def blit_plus(image: pygame.Surface, background: pygame.Surface, modes: tuple = (0, 0, 0, 0), values: tuple = (0, 0, 0, 0)):
    
    left, top, right, bottom = blit_plus_helper(image, background, modes, values)

    background.blit(image, (round(left - right), round(top - bottom)))


def blit_plus_rotate(image: pygame.Surface, background: pygame.Surface, modes: tuple = (0, 0, 0, 0), values: tuple = (0, 0, 0, 0), rotation: float = 0):

    left, top, right, bottom = blit_plus_helper(image, background, modes, values)

    rotatedImage = pygame.transform.rotate(image, rotation * 180 / math.pi)

    left -= (rotatedImage.get_width() - image.get_width()) / 2
    top -= (rotatedImage.get_height() - image.get_height()) / 2

    background.blit(rotatedImage, (round(left - right), round(top - bottom)))


def blit_plus_helper(image: pygame.Surface, background: pygame.Surface, modes: tuple = (0, 0, 0, 0), values: tuple = (0, 0, 0, 0)):
    
    left, top, right, bottom = 0, 0, 0, 0

    if modes[0] == 0: left = values[0]
    elif modes[0] == 1: left = background.get_width() - values[0]
    elif modes[0] == 2: left = background.get_width() * values[0]

    if modes[1] == 0: top = values[1]
    elif modes[1] == 1: top = background.get_height() - values[1]
    elif modes[1] == 2: top = background.get_height() * values[1]

    if modes[2] == 0: right = values[2]
    elif modes[2] == 1: right = image.get_width() - values[2]
    elif modes[2] == 2: right = image.get_width() * values[2]

    if modes[3] == 0: bottom = values[3]
    elif modes[3] == 1: bottom = image.get_height() - values[3]
    elif modes[3] == 2: bottom = image.get_height() * values[3]

    return left, top, right, bottom


def color_multiply(color, factor):
    return [int(component * factor) for component in color]


def color_lighten(color, factor):
    return [int(component + (255 - component) * factor) for component in color]


def draw_regular_polygon(surface, center, radius, sides, angle, color, width=0):
    angle_interval = np.pi * 2 / sides
    points = [np.add(center, vector_2d(angle_interval * i + angle, radius)).tolist() for i in range(sides)]
    pygame.draw.polygon(surface, color, points, width)


def point_in_rect(point, rect):
    if point[0] < rect[0] or point[0] > rect[0] + rect[2]: return False
    if point[1] < rect[1] or point[1] > rect[1] + rect[3]: return False
    return True


def font_surface(font: pygame.font.Font, text, color):
    return font.render(text, True, color)


DEBUG_TEXT_COLOR = (255, 0, 0)
DEBUG_TEXT_SIZE = 24
DEBUG_TEXT_FONT = pygame.font.Font(None, DEBUG_TEXT_SIZE)


def debug(surface, position, text):
    surface.blit(font_surface(DEBUG_TEXT_FONT, text, DEBUG_TEXT_COLOR), position)