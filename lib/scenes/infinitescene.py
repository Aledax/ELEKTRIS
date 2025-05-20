import sys
import os
import time
import pygame
from pygame.locals import *
import numpy as np
import itertools

from lib.scenes.pygamescene import PygameScene
from lib.scenes.sceneconfig import *
from lib.scenes.infiniteconfig import *
from lib.scenes.infiniteassets import *

from lib.blockblast.board import BBBoard
from lib.blockblast.infinitegame import BBInfiniteGame

from lib.utils.npplus import *


class InfiniteScene(PygameScene):


    def __init__(self, scene_runner, stage):

        super().__init__(scene_runner, WINDOW_SIZE)

        pygame.mixer.music.load(BGM_PATH)
        pygame.mixer.music.set_volume(0.02)

        # Animation state (one-time)

        self.background_scroll = 0
        self.flash_alpha = 0
        self.lerp_timer = 0

        self.wave_block_widths = [PREVIEW_CELL_WIDTH for _ in range(BBInfiniteGame.WAVE_SIZE)]
        self.wave_block_positions = [WAVE_POSITIONS[i] for i in range(BBInfiniteGame.WAVE_SIZE)]
        self.hold_block_widths = [PREVIEW_CELL_WIDTH for _ in range(BBInfiniteGame.HOLD_SIZE)]
        self.hold_block_positions = [HOLD_POSITIONS[i] for i in range(BBInfiniteGame.HOLD_SIZE)]
        self.selected_block_width = PREVIEW_CELL_WIDTH
        self.selected_block_position = (0, 0)
        self.released_block_width = BOARD_CELL_WIDTH
        self.released_block_position = (0, 0) # Not actually lineraly interpolated

        # Game config

        self.stage = stage
        self.score_goal = stage * 10
        self.max_life_multiplier = max(0.5, 0.9 ** (self.stage - 1))
        self.replenish_multiplier = max(0.5, 0.9 ** (self.stage - 1))
        
        self.theme_id = (stage - 1) % THEME_COUNT
        self.color_index = generate_color_index(COLOR_BASES[self.theme_id])

        self.setup()


    def grab_block(self, mouse_position):

        for i in range(BBInfiniteGame.WAVE_SIZE):
            if distance(mouse_position, WAVE_POSITIONS[i]) <= PREVIEW_HOVER_RADIUS:
                self.selected_block = self.game.wave_blocks[i]
                self.selected_block_width = PREVIEW_CELL_WIDTH
                self.selected_block_position = WAVE_POSITIONS[i]
                SOUND_SELECT.play()
                break

        for i in range(BBInfiniteGame.HOLD_SIZE):
            if distance(mouse_position, HOLD_POSITIONS[i]) <= PREVIEW_HOVER_RADIUS:
                self.selected_block = self.game.hold_blocks[i]
                self.selected_block_width = PREVIEW_CELL_WIDTH
                self.selected_block_position = HOLD_POSITIONS[i]
                SOUND_SELECT.play()
                break

    
    def release_block(self, mouse_position, anchor_position):

        if self.selected_block is not None and self.game.alive:

            if self.selected_block in self.game.wave_blocks:
                for i in range(len(HOLD_POSITIONS)):
                    if distance(mouse_position, HOLD_POSITIONS[i]) <= PREVIEW_HOVER_RADIUS:
                        result = self.game.hold_block(self.selected_block, i)
                        self.selected_block = None
                        self.hold_block_widths[i] = self.selected_block_width
                        self.hold_block_positions[i] = self.selected_block_position
                        if result:
                            SOUND_HOLD.play()
                        return
                
            previous_score = self.game.score

            place_wave_result = self.game.place_wave_block(self.selected_block, anchor_position)
            place_hold_result = self.game.place_hold_block(self.selected_block, anchor_position)

            if previous_score != self.game.score:
                self.update_score_label(self.game.score)
                SOUND_SCORE.play()
                self.flash_alpha = FLASH_INITIAL_ALPHA
                if self.game.won:
                    self.update_message_label('Good job! Press Space to continue')

            if place_wave_result or place_hold_result:
                SOUND_PLACE.play()
                self.released_block = self.selected_block
                self.released_block_width = self.selected_block_width
                self.released_block_position = self.selected_block_position
            else:
                if self.selected_block in self.game.wave_blocks:
                    wave_index = self.game.wave_blocks.index(self.selected_block)
                    self.wave_block_widths[wave_index] = self.selected_block_width
                    self.wave_block_positions[wave_index] = self.selected_block_position
                else:
                    hold_index = self.game.hold_blocks.index(self.selected_block)
                    self.hold_block_widths[hold_index] = self.selected_block_width
                    self.hold_block_positions[hold_index] = self.selected_block_position

            if not self.game.alive:
                SOUND_LOSE.play()
                pygame.mixer.music.stop()
                self.update_message_label('No more moves! Press Space to return')

        self.selected_block = None


    def start_game(self):

        pygame.mixer.music.play(-1)

        # Game state

        self.game = BBInfiniteGame(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'blocks.json'), [], self.score_goal, self.max_life_multiplier, self.replenish_multiplier)
        self.game.start()
        self.update_message_label('')

        self.started = True
        self.selected_block = None
        self.released_block = None
        self.lerp_timer = 0

        # Animation state (per reset)

        self.board_cell_sizes = [[0 for _ in range(BBBoard.BOARD_SIZE)] for _ in range(BBBoard.BOARD_SIZE)]


    def setup(self):

        self.started = False

        self.selected_block = None
        self.released_block = None

        self.score_label = None
        self.score_goal_label = None if self.score_goal == 0 else FONT_SCORE_GOAL.render(f'/ {self.score_goal}', True, self.color_index['text-score-goal'])
        self.message_label = None
        self.update_score_label(0)
        self.update_message_label('Press Space to start')
        self.score_goal_label.set_alpha(self.color_index['text-score-goal'][3])

        # Background, board, and wave row

        self.image_bg = pygame.transform.smoothscale(IMAGE_BG(self.theme_id), (WINDOW_WIDTH, WINDOW_WIDTH))
        
        wave_row_surface = pygame.surface.Surface((WINDOW_WIDTH, WAVE_ROW_HEIGHT)).convert_alpha()
        wave_row_surface.fill(self.color_index['wave-row'])

        self.midground_surface = pygame.surface.Surface(WINDOW_SIZE).convert_alpha()
        self.midground_surface.fill((0, 0, 0, 0))
        self.midground_surface.blit(wave_row_surface, (0, WAVE_Y - WAVE_ROW_HEIGHT / 2))

        cell_board_surface = pygame.surface.Surface((BOARD_CELL_WIDTH, BOARD_CELL_WIDTH)).convert_alpha()
        cell_board_surface.fill(self.color_index['cell-board-border'])
        pygame.draw.rect(cell_board_surface, self.color_index['cell-board'], (BOARD_CELL_BORDER, BOARD_CELL_BORDER, BOARD_CELL_WIDTH - BOARD_CELL_BORDER * 2, BOARD_CELL_WIDTH - BOARD_CELL_BORDER * 2))
        cell_board_surface_mipmap = {BOARD_CELL_WIDTH: cell_board_surface}
        self.draw_cell_surfaces(
            self.midground_surface,
            cell_board_surface_mipmap,
            BOARD_CENTER,
            {tuple(p): BOARD_CELL_WIDTH for p in itertools.product(range(BBBoard.BOARD_SIZE), range(BBBoard.BOARD_SIZE))},
            BOARD_CELL_WIDTH,
            BOARD_CELL_MARGIN,
            True
        )
        
        for center in HOLD_POSITIONS:
            draw_regular_polygon(self.midground_surface, center, HOLD_MARK_RADIUS, 4, 0, self.color_index['hold-mark'])
        
        # Block previews

        cell_preview_base_surface = pygame.surface.Surface((BOARD_CELL_WIDTH, BOARD_CELL_WIDTH)).convert_alpha()
        cell_preview_base_surface.fill(self.color_index['cell-preview-border'])
        pygame.draw.rect(cell_preview_base_surface, self.color_index['cell-preview'], (BOARD_CELL_BORDER, BOARD_CELL_BORDER, BOARD_CELL_WIDTH - BOARD_CELL_BORDER * 2, BOARD_CELL_WIDTH - BOARD_CELL_BORDER * 2))
        self.cell_preview_surface_mipmap = {BOARD_CELL_WIDTH: cell_preview_base_surface}
        for i in range(BOARD_CELL_WIDTH):
            self.cell_preview_surface_mipmap[i] = pygame.transform.smoothscale(cell_preview_base_surface, (i, i))

        cell_preview_highlight_base_surface = pygame.surface.Surface((BOARD_CELL_WIDTH, BOARD_CELL_WIDTH)).convert_alpha()
        cell_preview_highlight_base_surface.fill(self.color_index['cell-preview-highlight-border'])
        pygame.draw.rect(cell_preview_highlight_base_surface, self.color_index['cell-preview-highlight'], (BOARD_CELL_BORDER, BOARD_CELL_BORDER, BOARD_CELL_WIDTH - BOARD_CELL_BORDER * 2, BOARD_CELL_WIDTH - BOARD_CELL_BORDER * 2))
        self.cell_preview_highlight_surface_mipmap = {BOARD_CELL_WIDTH: cell_preview_highlight_base_surface}
        for i in range(BOARD_CELL_WIDTH):
            self.cell_preview_highlight_surface_mipmap[i] = pygame.transform.smoothscale(cell_preview_highlight_base_surface, (i, i))

        # Board fill

        self.board_filled_surface_mipmap = {}
        for i in range(BOARD_CELL_FILL_WIDTH + 1):
            board_filled_surface = pygame.surface.Surface((i, i)).convert_alpha()
            board_filled_inner_border = int(round(i * (1 - BOARD_CELL_INNER_FILL_WIDTH_RATIO) / 2))
            board_filled_inner_width = i - 2 * board_filled_inner_border
            board_filled_surface.fill(self.color_index['cell-board-filled'])
            pygame.draw.rect(board_filled_surface, self.color_index['cell-board-inner-filled'], (board_filled_inner_border, board_filled_inner_border, board_filled_inner_width, board_filled_inner_width))
            self.board_filled_surface_mipmap[i] = board_filled_surface

        # Board marker

        board_marker_surface = pygame.surface.Surface((BOARD_CELL_WIDTH, BOARD_CELL_WIDTH)).convert_alpha()
        pygame.draw.rect(board_marker_surface, self.color_index['cell-board-highlight'], ((BOARD_CELL_WIDTH - BOARD_MARKER_CELL_WIDTH) / 2, (BOARD_CELL_WIDTH - BOARD_MARKER_CELL_WIDTH) / 2, BOARD_MARKER_CELL_WIDTH, BOARD_MARKER_CELL_WIDTH))
        self.board_marker_surface_mipmap = {BOARD_CELL_WIDTH: board_marker_surface}

        # Flash

        self.flash_surface = pygame.surface.Surface(WINDOW_SIZE).convert_alpha()
        self.flash_surface.fill(self.color_index['flash'])


    def _update_frame(self, dt, mouse_position, mouse_pressed, keys_pressed, events):

        if self.started and self.game.alive and not self.game.won:
            self.game.update(dt)
            if self.game.alive == False:
                SOUND_LOSE.play()
                pygame.mixer.music.stop()
                self.update_message_label('Ran out of time! Press Space to return')

        # MECHANICS

        pressing_ctrl = keys_pressed[K_LCTRL] or keys_pressed[K_RCTRL]

        if self.started:
            selected_board_position = [-1, -1]

            if self.selected_block is not None:
                selected_max_x = max(position[0] for position in self.selected_block.relative_positions)
                selected_max_y = max(position[1] for position in self.selected_block.relative_positions)
                selected_mouse_offset = (
                    (BOARD_CELL_WIDTH * (selected_max_x + 1) + BOARD_CELL_MARGIN * selected_max_x) / 2,
                    (BOARD_CELL_WIDTH * (selected_max_y + 1) + BOARD_CELL_MARGIN * selected_max_y) / 2)
                selected_topleft = np.subtract(mouse_position, selected_mouse_offset).tolist()
                selected_board_position = [int(round(component)) for component in np.divide(np.subtract(selected_topleft, BOARD_TOPLEFT), BOARD_CELL_WIDTH + BOARD_CELL_MARGIN)]

        for event in events:

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit()

            if self.started:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.grab_block(mouse_position)
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.release_block(mouse_position, selected_board_position)
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    if self.game.won:
                        self.scene_runner.switch_to_infinite_scene(True, self.stage + 1)
                    elif not self.game.alive:
                        self.scene_runner.switch_to_main_scene(True)
            else:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if not self.started:
                        self.start_game()
                    
            
        # ANIMATION

        self.flash_alpha = lerp_float(self.flash_alpha, 0, FLASH_ALPHA_LERP, dt * self.scene_runner.fps)
        self.flash_surface.set_alpha(self.flash_alpha)

        self.background_scroll = (self.background_scroll - BACKGROUND_SCROLL_SPEED * dt) % self.image_bg.get_height()

        if self.started:
            filled_positions = self.game.board.filled_positions()
            for x in range(BBBoard.BOARD_SIZE):
                for y in range(BBBoard.BOARD_SIZE):
                    filled = (x, y) in filled_positions
                    self.board_cell_sizes[x][y] = lerp_float(self.board_cell_sizes[x][y], (BOARD_CELL_FILL_WIDTH if filled else 0), BOARD_CELL_SIZE_LERP, dt * self.scene_runner.fps)
        
            for i in range(BBInfiniteGame.WAVE_SIZE):
                self.wave_block_widths[i] = lerp_float(self.wave_block_widths[i], PREVIEW_CELL_WIDTH, PREVIEW_CELL_SIZE_LERP, dt * self.scene_runner.fps)
                self.wave_block_positions[i] = lerp_array(self.wave_block_positions[i], WAVE_POSITIONS[i], PREVIEW_CELL_POSITION_LERP, dt * self.scene_runner.fps)
            for i in range(BBInfiniteGame.HOLD_SIZE):
                self.hold_block_widths[i] = lerp_float(self.hold_block_widths[i], PREVIEW_CELL_WIDTH, PREVIEW_CELL_SIZE_LERP, dt * self.scene_runner.fps)
                self.hold_block_positions[i] = lerp_array(self.hold_block_positions[i], HOLD_POSITIONS[i], PREVIEW_CELL_POSITION_LERP, dt * self.scene_runner.fps)

            if self.selected_block is not None:
                self.selected_block_width = lerp_float(self.selected_block_width, BOARD_CELL_WIDTH, PREVIEW_CELL_SIZE_LERP, dt * self.scene_runner.fps)
                self.selected_block_position = lerp_array(self.selected_block_position, mouse_position, PREVIEW_CELL_POSITION_LERP, dt * self.scene_runner.fps)
            if self.released_block is not None:
                self.released_block_width = lerp_float(self.released_block_width, 0, BOARD_CELL_SIZE_LERP, dt * self.scene_runner.fps)

            self.lerp_timer = lerp_float(self.lerp_timer, self.game.life, TIMER_LERP, dt * self.scene_runner.fps)

        # DRAWING

        # Background and midground

        for i in range(-1, int(WINDOW_HEIGHT / self.image_bg.get_height()) + 1):
            self.scene_surface.blit(self.image_bg, (0, self.background_scroll + i * self.image_bg.get_height()))

        self.scene_surface.blit(self.midground_surface, (0, 0))          

        # Labels

        blit_plus(self.score_label, self.scene_surface, (2, 0, 2, 2), (0.5, SCORE_Y, 0.5, 0.5))
        blit_plus(self.message_label, self.scene_surface, (2, 0, 2, 2), (0.5, MESSAGE_Y, 0.5, 0.5))
        if self.score_goal != 0:
            blit_plus(self.score_goal_label, self.scene_surface, (0, 0, 2, 2), (WINDOW_CENTER_X + self.score_label.get_width() / 2 + SCORE_GOAL_X, SCORE_GOAL_Y, 0.5, 0.5))
        
        if self.started:

            # Board Blocks

            board_surface = pygame.surface.Surface(WINDOW_SIZE).convert_alpha()
            board_surface.fill((0, 0, 0, 0))
            all_positions = [tuple(p) for p in itertools.product(range(BBBoard.BOARD_SIZE), range(BBBoard.BOARD_SIZE))]

            self.draw_cell_surfaces(
                board_surface,
                self.board_filled_surface_mipmap,
                BOARD_TOPLEFT,
                {tuple(p): self.board_cell_sizes[p[0]][p[1]] for p in all_positions},
                BOARD_CELL_WIDTH,
                BOARD_CELL_MARGIN,
            )

            self.scene_surface.blit(board_surface, (0, 0))
                        
            # Wave Blocks

            for i in range(BBInfiniteGame.WAVE_SIZE):

                width = self.wave_block_widths[i]
                block_center = self.wave_block_positions[i]

                if self.game.wave_blocks[i] is None or self.game.wave_blocks[i] == self.selected_block:
                    continue

                mipmap = self.cell_preview_surface_mipmap
                if self.selected_block is None and distance(mouse_position, block_center) <= PREVIEW_HOVER_RADIUS:
                    mipmap = self.cell_preview_highlight_surface_mipmap

                self.draw_cell_surfaces(
                    self.scene_surface,
                    mipmap,
                    block_center,
                    {tuple(p): width for p in self.game.wave_blocks[i].relative_positions},
                    round(width),
                    PREVIEW_CELL_MARGIN,
                    True
                )
                
            # Hold Blocks
                
            for i in range(BBInfiniteGame.HOLD_SIZE):

                width = self.hold_block_widths[i]
                block_center = self.hold_block_positions[i]

                if self.game.hold_blocks[i] is None or self.game.hold_blocks[i] == self.selected_block:
                    continue

                mipmap = self.cell_preview_surface_mipmap
                if self.selected_block is None and distance(mouse_position, block_center) <= PREVIEW_HOVER_RADIUS:
                    mipmap = self.cell_preview_highlight_surface_mipmap

                self.draw_cell_surfaces(
                    self.scene_surface,
                    mipmap,
                    block_center,
                    {tuple(p): width for p in self.game.hold_blocks[i].relative_positions},
                    round(width),
                    PREVIEW_CELL_MARGIN,
                    True
                )
                
            # Timer Ring
                
            if not self.game.won:
                self.draw_timer_ring(self.scene_surface, BOARD_CENTER, self.game.life, self.color_index['timer'])
                self.draw_timer_ring(self.scene_surface, BOARD_CENTER, self.lerp_timer, self.color_index['lerp-timer'])

            # Selected Block
                
            if self.selected_block is not None:
                
                if self.game.board.place_block(selected_board_position, self.selected_block.relative_positions) != None:

                    self.draw_cell_surfaces(
                        self.scene_surface,
                        self.board_marker_surface_mipmap,
                        np.add(BOARD_TOPLEFT, np.multiply(selected_board_position, (BOARD_CELL_WIDTH + BOARD_CELL_MARGIN))),
                        {tuple(p): BOARD_CELL_WIDTH for p in self.selected_block.relative_positions},
                        BOARD_CELL_WIDTH,
                        BOARD_CELL_MARGIN
                    )

                self.draw_cell_surfaces(
                    self.scene_surface,
                    self.cell_preview_highlight_surface_mipmap,
                    self.selected_block_position,
                    {tuple(p): self.selected_block_width for p in self.selected_block.relative_positions},
                    round(self.selected_block_width),
                    BOARD_CELL_MARGIN,
                    True
                )
                
            # Released Block

            if self.released_block is not None:

                self.draw_cell_surfaces(
                    self.scene_surface,
                    self.cell_preview_highlight_surface_mipmap,
                    self.released_block_position,
                    {tuple(p): self.released_block_width for p in self.released_block.relative_positions},
                    BOARD_CELL_WIDTH,
                    BOARD_CELL_MARGIN,
                    True
                )
            
        # Flash

        self.scene_surface.blit(self.flash_surface, (0, 0))


    def draw_cell_surfaces(self, background_surface, cell_surface_mipmap, anchor_position, relative_positions_widths, cell_width, cell_margin, anchor_is_center=False):

        if anchor_is_center:
            max_x = max(position[0] for position in relative_positions_widths)
            max_y = max(position[1] for position in relative_positions_widths)
            whole_size = (cell_width * (max_x + 1) + cell_margin * max_x, cell_width * (max_y + 1) + cell_margin * max_y)
            anchor_position = np.subtract(anchor_position, np.multiply(whole_size, 0.5)).tolist()

        for relative_position in relative_positions_widths:
            this_cell_margin = int(round((cell_width - relative_positions_widths[relative_position]) / 2))
            this_cell_width = cell_width - 2 * this_cell_margin
            absolute_position = np.add(np.add(anchor_position, np.multiply(relative_position, cell_width + cell_margin)), this_cell_margin).round().tolist()
            background_surface.blit(cell_surface_mipmap[this_cell_width], absolute_position)


    def draw_timer_ring(self, surface, center, life, color):

        if not self.game.alive:
            return

        timer_eighth_index = math.ceil(life / (self.game.max_life / 8))
        timer_eighth_remainder_portion = (life % (self.game.max_life / 8)) / (self.game.max_life / 8)
        eighth_length = round(TIMER_SIZE / 2)
        remainder_length = round(eighth_length * timer_eighth_remainder_portion)
        (l, t) = np.subtract(center, np.multiply([TIMER_SIZE, TIMER_SIZE], 0.5)).tolist()
        
        if timer_eighth_index > 1:
            pygame.draw.rect(surface, color, (l, t, eighth_length, TIMER_RING_THICKNESS))
            if timer_eighth_index > 2:
                pygame.draw.rect(surface, color, (l, t, TIMER_RING_THICKNESS, eighth_length))
                if timer_eighth_index > 3:
                    pygame.draw.rect(surface, color, (l, t + eighth_length, TIMER_RING_THICKNESS, eighth_length))
                    if timer_eighth_index > 4:
                        pygame.draw.rect(surface, color, (l, t + TIMER_SIZE - TIMER_RING_THICKNESS, eighth_length, TIMER_RING_THICKNESS))
                        if timer_eighth_index > 5:
                            pygame.draw.rect(surface, color, (l + eighth_length, t + TIMER_SIZE - TIMER_RING_THICKNESS, eighth_length, TIMER_RING_THICKNESS))
                            if timer_eighth_index > 6:
                                pygame.draw.rect(surface, color, (l + TIMER_SIZE - TIMER_RING_THICKNESS, t + eighth_length, TIMER_RING_THICKNESS, eighth_length))
                                if timer_eighth_index > 7:
                                    pygame.draw.rect(surface, color, (l + TIMER_SIZE - TIMER_RING_THICKNESS, t, TIMER_RING_THICKNESS, eighth_length))
                                    pygame.draw.rect(surface, color, (l + TIMER_SIZE - remainder_length, t, remainder_length, TIMER_RING_THICKNESS))
                                else:
                                    pygame.draw.rect(surface, color, (l + TIMER_SIZE - TIMER_RING_THICKNESS, t + eighth_length - remainder_length, TIMER_RING_THICKNESS, remainder_length))
                            else:
                                pygame.draw.rect(surface, color, (l + TIMER_SIZE - TIMER_RING_THICKNESS, t + TIMER_SIZE - remainder_length, TIMER_RING_THICKNESS, remainder_length))
                        else:
                            pygame.draw.rect(surface, color, (l + eighth_length, t + TIMER_SIZE - TIMER_RING_THICKNESS, remainder_length, TIMER_RING_THICKNESS))
                    else:
                        pygame.draw.rect(surface, color, (l, t + TIMER_SIZE - TIMER_RING_THICKNESS, remainder_length, TIMER_RING_THICKNESS))
                else:
                    pygame.draw.rect(surface, color, (l, t + eighth_length, TIMER_RING_THICKNESS, remainder_length))
            else:
                pygame.draw.rect(surface, color, (l, t, TIMER_RING_THICKNESS, remainder_length))
        else:
            pygame.draw.rect(surface, color, (l + eighth_length - remainder_length, t, remainder_length, TIMER_RING_THICKNESS))


    def update_score_label(self, score):

        self.score_label = FONT_SCORE.render(str(score), True, self.color_index['text-score'])
        self.score_label.set_alpha(self.color_index['text-score'][3])

    
    def update_message_label(self, message):

        self.message_label = FONT_MESSAGE.render(message, True, self.color_index['text-message'])
        self.message_label.set_alpha(self.color_index['text-message'][3])