import numpy as np

from ..blockblast.board import BBBoard
from ..blockblast.infinitegame import BBInfiniteGame
from ..utils.pygameplus import *


# Dimnsions


WINDOW_RATIO = [9, 16]
WINDOW_HEIGHT = 720

SCORE_Y_RATIO = 0.12 # As a portion of the window height
FONT_SCORE_SIZE_RATIO = 0.1 # As a portion of the window height

BOARD_CENTER_Y_RATIO = 0.42 # As a portion of the window height
BOARD_CELL_WIDTH_RATIO = 0.085 # As a portion of the window width
PREVIEW_CELL_WIDTH_RATIO = 0.05 # As a portion of the window width
CELL_MARGIN_RATIO = 0.2 # As a portion of the cell width

WAVE_Y_RATIO = 0.75 # As a portion of the window height
HOLD_Y_RATIO = 0.9 # As a portion of the window height
PREVIEW_SPACING_RATIO = 0.275 # As a portion of the window width
PREVIEW_HOVER_RADIUS_RATIO = 2.25 # As a portion of the preview cell width
WAVE_ROW_HEIGHT_RATIO = 5 # As a portion of the preview cell width
HOLD_MARK_RADIUS_RATIO = 1 # As a portion of the preview cell width

WINDOW_WIDTH = int(round(WINDOW_HEIGHT / WINDOW_RATIO[1] * WINDOW_RATIO[0]))
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CENTER_X = int(round(WINDOW_WIDTH / 2))
WINDOW_CENTER_Y = int(round(WINDOW_HEIGHT / 2))
WINDOW_CENTER = (WINDOW_CENTER_X, WINDOW_CENTER_Y)

BOARD_CELL_WIDTH = int(WINDOW_WIDTH * BOARD_CELL_WIDTH_RATIO)
BOARD_CELL_MARGIN = int(BOARD_CELL_WIDTH * CELL_MARGIN_RATIO)

BOARD_CENTER_Y = int(WINDOW_HEIGHT * BOARD_CENTER_Y_RATIO)
BOARD_CENTER = (WINDOW_CENTER_X, BOARD_CENTER_Y)
BOARD_TOPLEFT = np.subtract(BOARD_CENTER, (BOARD_CELL_WIDTH * BBBoard.BOARD_SIZE + BOARD_CELL_MARGIN * (BBBoard.BOARD_SIZE - 1)) / 2).tolist()

PREVIEW_CELL_WIDTH = int(WINDOW_WIDTH * PREVIEW_CELL_WIDTH_RATIO)
PREVIEW_CELL_MARGIN = int(PREVIEW_CELL_WIDTH * CELL_MARGIN_RATIO)
WAVE_Y = int(WINDOW_HEIGHT * WAVE_Y_RATIO)
HOLD_Y = int(WINDOW_HEIGHT * HOLD_Y_RATIO)
PREVIEW_SPACING = int(WINDOW_WIDTH * PREVIEW_SPACING_RATIO)
WAVE_POSITIONS = [(WINDOW_CENTER_X + PREVIEW_SPACING * (i - (BBInfiniteGame.WAVE_SIZE - 1) / 2), WAVE_Y) for i in range(BBInfiniteGame.WAVE_SIZE)]
HOLD_POSITIONS = [(WINDOW_CENTER_X + PREVIEW_SPACING * (i - (BBInfiniteGame.HOLD_SIZE - 1) / 2), HOLD_Y) for i in range(BBInfiniteGame.HOLD_SIZE)]
PREVIEW_HOVER_RADIUS = int(PREVIEW_CELL_WIDTH * PREVIEW_HOVER_RADIUS_RATIO)
WAVE_ROW_HEIGHT = int(PREVIEW_CELL_WIDTH * WAVE_ROW_HEIGHT_RATIO)
HOLD_MARK_RADIUS = int(PREVIEW_CELL_WIDTH * HOLD_MARK_RADIUS_RATIO)

SCORE_Y = int(WINDOW_HEIGHT * SCORE_Y_RATIO)
FONT_SCORE_SIZE = int(WINDOW_HEIGHT * FONT_SCORE_SIZE_RATIO)


# Colors


COLOR_BG = (50, 20, 200)
COLOR_BG_FLASH = color_lighten(COLOR_BG, 0.2)
COLOR_FLASH = (255, 255, 255)
FLASH_INITIAL_ALPHA = 50

COLOR_CELL_BOARD = color_multiply(COLOR_BG, 0.6)
COLOR_CELL_BOARD_HIGHLIGHT = color_lighten(COLOR_CELL_BOARD, 0.4)
COLOR_CELL_BOARD_FILLED = (255, 255, 210)
COLOR_CELL_PREVIEW = (100, 200, 255)
COLOR_CELL_PREVIEW_HIGHLIGHT = color_lighten(COLOR_CELL_PREVIEW, 0.7)
COLOR_BG_DARK = color_multiply(COLOR_BG, 0.8)

COLOR_TEXT_SCORE = COLOR_CELL_BOARD_FILLED


# Fonts


pygame.font.init()

FONT_SCORE = pygame.font.Font(asset_path(os.path.join('fonts', 'DAGGERSQUARE.otf')), FONT_SCORE_SIZE)


# Sounds


pygame.mixer.init()

SOUND_SELECT = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'flick1.ogg')))

SOUND_HOLD = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'crank1.wav')))

SOUND_PLACE = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'snap1.wav')))

SOUND_SCORE = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'ding3.wav')))
SOUND_SCORE.set_volume(0.3)

SOUND_LOSE = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'incorrect1.wav')))

SOUND_RESTART = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'wipe1.wav')))