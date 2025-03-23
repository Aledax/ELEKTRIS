import sys
import os
import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
import itertools

from .infiniteconfig import *
from ..blockblast.board import BBBoard
from ..blockblast.infinitegame import BBInfiniteGame
from ..utils.npplus import *


class BBInfinitePygame:


    def __init__(self):

        self.clock = pygame.time.Clock()

        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)

        self.setup()
        self.loop()


    def quit(self):
        
        pygame.quit()
        sys.exit()


    def grab_block(self, mouse_position):

        for i in range(BBInfiniteGame.WAVE_SIZE):
            if distance(mouse_position, WAVE_POSITIONS[i]) <= PREVIEW_HOVER_RADIUS:
                self.selected_block = self.game.wave_blocks[i]
                SOUND_SELECT.play()
                break

        for i in range(BBInfiniteGame.HOLD_SIZE):
            if distance(mouse_position, HOLD_POSITIONS[i]) <= PREVIEW_HOVER_RADIUS:
                self.selected_block = self.game.hold_blocks[i]
                SOUND_SELECT.play()
                break

    
    def release_block(self, mouse_position, anchor_position):

        if self.selected_block is not None:

            if self.selected_block in self.game.wave_blocks:
                for i in range(len(HOLD_POSITIONS)):
                    if distance(mouse_position, HOLD_POSITIONS[i]) <= PREVIEW_HOVER_RADIUS:
                        result = self.game.hold_block(self.selected_block, i)
                        self.selected_block = None
                        if result:
                            SOUND_HOLD.play()
                        return
                
            previous_score = self.game.score

            place_wave_result = self.game.place_wave_block(self.selected_block, anchor_position)
            place_hold_result = self.game.place_hold_block(self.selected_block, anchor_position)

            if previous_score != self.game.score:
                self.update_score_label()
                SOUND_SCORE.play()
                self.flash_alpha = FLASH_INITIAL_ALPHA

            if place_wave_result or place_hold_result:
                SOUND_PLACE.play()

            if not self.lost and not self.game.alive:
                self.lost = True
                SOUND_LOSE.play()

            self.selected_block = None

    
    def setup(self):

        self.prepare_state()
        self.prepare_surfaces()


    def prepare_state(self):

        # Game state

        self.game = BBInfiniteGame(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'blocks.json'))
        self.selected_block = None
        self.lost = False

        # Animation state

        self.flash_alpha = 0


    def prepare_surfaces(self):

        self.score_label = None
        self.update_score_label()  

        self.background_surface = pygame.surface.Surface(WINDOW_SIZE).convert_alpha()
        self.background_surface.fill(COLOR_BG)
        pygame.draw.rect(self.background_surface, COLOR_BG_DARK, (0, WAVE_Y - WAVE_ROW_HEIGHT / 2, WINDOW_WIDTH, WAVE_ROW_HEIGHT))
        self.draw_cells(
            self.background_surface,
            BOARD_CENTER,
            [list(p) for p in itertools.product(range(BBBoard.BOARD_SIZE), range(BBBoard.BOARD_SIZE))],
            COLOR_CELL_BOARD,
            BOARD_CELL_WIDTH,
            BOARD_CELL_MARGIN,
            True)
        
        self.flash_surface = pygame.surface.Surface(WINDOW_SIZE).convert_alpha()
        self.flash_surface.fill(COLOR_FLASH)


    def loop(self):

        while True:

            # Mechanics

            mouse_position = pygame.mouse.get_pos()
            pressing_keys = pygame.key.get_pressed()
            pressing_ctrl = pressing_keys[K_LCTRL] or pressing_keys[K_RCTRL]

            selected_board_position = [-1, -1]

            if self.selected_block is not None:
                selected_max_x = max(position[0] for position in self.selected_block.relative_positions)
                selected_max_y = max(position[1] for position in self.selected_block.relative_positions)
                selected_mouse_offset = (
                    (BOARD_CELL_WIDTH * (selected_max_x + 1) + BOARD_CELL_MARGIN * selected_max_x) / 2,
                    (BOARD_CELL_WIDTH * (selected_max_y + 1) + BOARD_CELL_MARGIN * selected_max_y) / 2)
                selected_topleft = np.subtract(mouse_position, selected_mouse_offset).tolist()
                selected_board_position = [int(round(component)) for component in np.divide(np.subtract(selected_topleft, BOARD_TOPLEFT), BOARD_CELL_WIDTH + BOARD_CELL_MARGIN)]

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.grab_block(mouse_position)
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.release_block(mouse_position, selected_board_position)
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.grab_block(mouse_position)
                    elif event.key == K_r and pressing_ctrl:
                        SOUND_RESTART.play()
                        self.setup()
                    elif event.key == K_ESCAPE:
                        self.quit()
                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.release_block(mouse_position, selected_board_position)
                elif event.type == QUIT:
                    self.quit()

            # Animation

            self.flash_alpha *= 0.95
            self.flash_surface.set_alpha(self.flash_alpha)

            # Drawing

            self.window_surface.blit(self.background_surface, (0, 0))

            blit_plus(self.score_label, self.window_surface, (2, 0, 2, 2), (0.5, SCORE_Y, 0.5, 0.5))
            
            self.draw_cells(
                self.window_surface,
                BOARD_TOPLEFT,
                self.game.board.filled_positions(),
                COLOR_CELL_BOARD_FILLED,
                BOARD_CELL_WIDTH,
                BOARD_CELL_MARGIN)
            
            for i in range(BBInfiniteGame.WAVE_SIZE):
                block_center = WAVE_POSITIONS[i]

                if self.game.wave_blocks[i] is None or self.game.wave_blocks[i] == self.selected_block:
                    continue

                block_color = COLOR_CELL_PREVIEW
                if self.selected_block is None and distance(mouse_position, block_center) <= PREVIEW_HOVER_RADIUS:
                    block_color = COLOR_CELL_PREVIEW_HIGHLIGHT

                self.draw_cells(
                    self.window_surface,
                    block_center,
                    self.game.wave_blocks[i].relative_positions,
                    block_color,
                    PREVIEW_CELL_WIDTH,
                    PREVIEW_CELL_MARGIN,
                    True)
                
            for i in range(BBInfiniteGame.HOLD_SIZE):
                block_center = HOLD_POSITIONS[i]
                draw_regular_polygon(self.window_surface, block_center, HOLD_MARK_RADIUS, 4, 0, COLOR_BG_DARK)

                if self.game.hold_blocks[i] is None or self.game.hold_blocks[i] == self.selected_block:
                    continue

                block_color = COLOR_CELL_PREVIEW
                if self.selected_block is None and distance(mouse_position, block_center) <= PREVIEW_HOVER_RADIUS:
                    block_color = COLOR_CELL_PREVIEW_HIGHLIGHT

                self.draw_cells(
                    self.window_surface,
                    block_center,
                    self.game.hold_blocks[i].relative_positions,
                    block_color,
                    PREVIEW_CELL_WIDTH,
                    PREVIEW_CELL_MARGIN,
                    True)
                
            if self.selected_block is not None:
                
                if self.game.board.place_block(selected_board_position, self.selected_block.relative_positions) != None:
                    self.draw_cells(
                        self.window_surface,
                        np.add(BOARD_TOPLEFT, np.multiply(selected_board_position, (BOARD_CELL_WIDTH + BOARD_CELL_MARGIN))),
                        self.selected_block.relative_positions,
                        COLOR_CELL_BOARD_HIGHLIGHT,
                        BOARD_CELL_WIDTH,
                        BOARD_CELL_MARGIN)
                
                self.draw_cells(
                    self.window_surface,
                    mouse_position,
                    self.selected_block.relative_positions,
                    COLOR_CELL_PREVIEW_HIGHLIGHT,
                    BOARD_CELL_WIDTH,
                    BOARD_CELL_MARGIN,
                    True)
                
            self.window_surface.blit(self.flash_surface, (0, 0))

            pygame.display.update()
            self.clock.tick()

    
    def draw_cells(self, surface, anchor_position, relative_positions, color, cell_width, cell_margin, anchor_is_center=False):

        if anchor_is_center:
            max_x = max(position[0] for position in relative_positions)
            max_y = max(position[1] for position in relative_positions)
            cells_size = (cell_width * (max_x + 1) + cell_margin * max_x, cell_width * (max_y + 1) + cell_margin * max_y)
            anchor_position = np.subtract(anchor_position, np.multiply(cells_size, 0.5)).tolist()

        for relative_position in relative_positions:
            absolute_position = np.add(anchor_position, np.multiply(relative_position, cell_width + cell_margin)).tolist()
            pygame.draw.rect(surface, color, (*absolute_position, cell_width, cell_width))


    def update_score_label(self):

        self.score_label = FONT_SCORE.render(str(self.game.score), True, COLOR_TEXT_SCORE)