import numpy as np

from lib.blockblast.board import BBBoard
from lib.blockblast.infinitegame import BBInfiniteGame
from lib.utils.pygameplus import *

from lib.scenes.sceneconfig import *


# Dimensions


SCORE_Y_RATIO = 0.12 # As a portion of the window height
SCORE_GOAL_X_RATIO = 0.08 # As a portion of the window width
SCORE_GOAL_Y_RATIO = 0.14 # As a portion of the window height
FONT_SCORE_SIZE_RATIO = 0.1 # As a portion of the window height
FONT_SCORE_GOAL_SIZE_RATIO = 0.35 # As a portion of the score size
FONT_MESSAGE_SIZE_RATIO = 0.02 # As a portion of the window height

BOARD_CENTER_Y_RATIO = 0.42 # As a portion of the window height
BOARD_CELL_WIDTH_RATIO = 0.085 # As a portion of the window width
BOARD_CELL_FILL_WIDTH_RATIO = 0.85 # As a portion of the board cell width
BOARD_CELL_INNER_FILL_WIDTH_RATIO = 0.85 # As a portion of the board cell fill width
BOARD_MARKER_CELL_WIDTH_RATIO = 1 # As a portion of the board cell width
PREVIEW_CELL_WIDTH_RATIO = 0.05 # As a portion of the window width
CELL_MARGIN_RATIO = 0.2 # As a portion of the cell width

MESSAGE_Y_RATIO = 0.64 # As a portion of the window height
WAVE_Y_RATIO = 0.75 # As a portion of the window height
HOLD_Y_RATIO = 0.9 # As a portion of the window height
PREVIEW_SPACING_RATIO = 0.275 # As a portion of the window width
PREVIEW_HOVER_RADIUS_RATIO = 2.25 # As a portion of the preview cell width
WAVE_ROW_HEIGHT_RATIO = 6 # As a portion of the preview cell width
HOLD_MARK_RADIUS_RATIO = 0.5 # As a portion of the preview cell width

TIMER_RING_THICKNESS_RATIO = 0.11 # As a portion of the board cell width
TIMER_RING_MARGIN_RATIO = 0.3 # As a portion of the board cell width

BOARD_CELL_WIDTH = int(WINDOW_WIDTH * BOARD_CELL_WIDTH_RATIO)
BOARD_CELL_FILL_WIDTH = int(BOARD_CELL_WIDTH * BOARD_CELL_FILL_WIDTH_RATIO)
BOARD_MARKER_CELL_WIDTH = int(BOARD_CELL_WIDTH * BOARD_MARKER_CELL_WIDTH_RATIO)
BOARD_CELL_BORDER = int(BOARD_CELL_WIDTH / 17)
BOARD_CELL_MARGIN = int(BOARD_CELL_WIDTH * CELL_MARGIN_RATIO)

BOARD_CENTER_Y = int(WINDOW_HEIGHT * BOARD_CENTER_Y_RATIO)
BOARD_CENTER = (WINDOW_CENTER_X, BOARD_CENTER_Y)
BOARD_TOPLEFT = np.subtract(BOARD_CENTER, (BOARD_CELL_WIDTH * BBBoard.BOARD_SIZE + BOARD_CELL_MARGIN * (BBBoard.BOARD_SIZE - 1)) / 2).tolist()

PREVIEW_CELL_WIDTH = int(WINDOW_WIDTH * PREVIEW_CELL_WIDTH_RATIO)
PREVIEW_CELL_MARGIN = int(PREVIEW_CELL_WIDTH * CELL_MARGIN_RATIO)
MESSAGE_Y = int(WINDOW_HEIGHT * MESSAGE_Y_RATIO)
WAVE_Y = int(WINDOW_HEIGHT * WAVE_Y_RATIO)
HOLD_Y = int(WINDOW_HEIGHT * HOLD_Y_RATIO)
PREVIEW_SPACING = int(WINDOW_WIDTH * PREVIEW_SPACING_RATIO)
WAVE_POSITIONS = [(WINDOW_CENTER_X + PREVIEW_SPACING * (i - (BBInfiniteGame.WAVE_SIZE - 1) / 2), WAVE_Y) for i in range(BBInfiniteGame.WAVE_SIZE)]
HOLD_POSITIONS = [(WINDOW_CENTER_X + PREVIEW_SPACING * (i - (BBInfiniteGame.HOLD_SIZE - 1) / 2), HOLD_Y) for i in range(BBInfiniteGame.HOLD_SIZE)]
PREVIEW_HOVER_RADIUS = int(PREVIEW_CELL_WIDTH * PREVIEW_HOVER_RADIUS_RATIO)
WAVE_ROW_HEIGHT = int(PREVIEW_CELL_WIDTH * WAVE_ROW_HEIGHT_RATIO)
HOLD_MARK_RADIUS = int(PREVIEW_CELL_WIDTH * HOLD_MARK_RADIUS_RATIO)

TIMER_RING_THICKNESS = int(BOARD_CELL_WIDTH * TIMER_RING_THICKNESS_RATIO)
TIMER_RING_MARGIN = int(BOARD_CELL_WIDTH * TIMER_RING_MARGIN_RATIO)
TIMER_SIZE = BBBoard.BOARD_SIZE * BOARD_CELL_WIDTH + (BBBoard.BOARD_SIZE - 1) * BOARD_CELL_MARGIN + 2 * (TIMER_RING_MARGIN + TIMER_RING_THICKNESS)

SCORE_Y = int(WINDOW_HEIGHT * SCORE_Y_RATIO)
SCORE_GOAL_X = int(WINDOW_WIDTH * SCORE_GOAL_X_RATIO)
SCORE_GOAL_Y = int(WINDOW_HEIGHT * SCORE_GOAL_Y_RATIO)
FONT_SCORE_SIZE = int(WINDOW_HEIGHT * FONT_SCORE_SIZE_RATIO)
FONT_SCORE_GOAL_SIZE = int(FONT_SCORE_SIZE * FONT_SCORE_GOAL_SIZE_RATIO)
FONT_MESSAGE_SIZE = int(WINDOW_HEIGHT * FONT_MESSAGE_SIZE_RATIO)


# Animations


FLASH_ALPHA_LERP = 0.1
BOARD_CELL_SIZE_LERP = 0.3
PREVIEW_CELL_SIZE_LERP = 0.3
PREVIEW_CELL_POSITION_LERP = 0.5
TIMER_LERP = 0.1


# Colors


FLASH_INITIAL_ALPHA = 35


def generate_color_index(color_base):

    color_index = {}

    color_index['bg-flash'] = color_lighten(color_base, 0.5)
    color_index['flash'] = (255, 255, 255)

    color_index['cell-board'] = (*color_base, 15)
    color_index['cell-board-border'] = (*color_base, 75)
    color_index['cell-board-highlight'] = (*color_lighten(color_base, 0.2), 100)
    color_index['cell-board-filled'] = (*color_lighten(color_base, 0.2), 200)
    color_index['cell-board-inner-filled'] = (*color_lighten(color_base, 0.75), 225)
    color_index['cell-preview'] = (*color_multiply(color_base, 0.1), 240)
    color_index['cell-preview-border'] = color_lighten(color_base, 0.5)
    color_index['cell-preview-highlight'] = color_lighten(color_index['cell-preview'], 0.05)
    color_index['cell-preview-highlight-border'] = color_lighten(color_index['cell-preview-border'], 0.7)

    color_index['wave-row'] = (*color_base, 15)
    color_index['text-score'] = (*color_index['cell-board-filled'][:3], 255)
    color_index['text-score-goal'] = (*color_index['text-score'][:3], 200)
    color_index['text-message'] = color_index['text-score']
    color_index['timer'] = (*color_lighten(color_base, 0.2), 100)
    color_index['lerp-timer'] = (*color_lighten(color_base, 0.2), 225)
    color_index['hold-mark'] = (*color_lighten(color_base, 0.2), 200)

    return color_index
