import json
import random
import copy

from .board import BBBoard


class BBInfiniteGame:


    WAVE_SIZE = 3
    HOLD_SIZE = 1

    MAX_LIFE = 20
    PLACE_REPLENISH = 1
    ROW_REPLENISH = 5

    ABILITY_TAGS = [
        'buff_i',
        'buff_o',
        'buff_t',
        'buff_z',
        'buff_l',
        'buff_life_replenish',
        'buff_score',
        'insert_tile',
        'delete_tile',
        'skip_block',
        'rotate_block_cw',
        'rotate_block_ccw',
        'flip_block',
        'ghost_block',
        'reshuffle'
    ]


    class Block:

        def __init__(self, relative_positions, frequency):

            self.relative_positions = relative_positions
            self.frequency = frequency

            self.text = self._to_text()

        
        def _to_text(self):

            max_x = max(position[0] for position in self.relative_positions)
            max_y = max(position[1] for position in self.relative_positions)

            rows = [['O' if [x, y] in self.relative_positions else ' ' for x in range(max_x + 1)] for y in range(max_y + 1)]

            return '\n'.join(' '.join(row) for row in rows)

    
    def __init__(self, block_json_path, active_abilities):

        self.board = BBBoard()
        self.started = False
        self.alive = True
        self.all_blocks = []
        self.wave_blocks = [None for _ in range(BBInfiniteGame.WAVE_SIZE)]
        self.hold_blocks = [None for _ in range(BBInfiniteGame.HOLD_SIZE)]
        self.score = 0
        self.life = 0
        self.abilities = {ability: ability in active_abilities for ability in BBInfiniteGame.ABILITY_TAGS}

        self._load_blocks(block_json_path)


    def _load_blocks(self, block_json_path):

        with open(block_json_path) as f:
            block_datas = json.load(f)['blocks']
            rotated_block_datas = []
            for block_data in block_datas:
                rotated_block_datas.append(block_data)
                for _ in range(3):
                    rotated_block_data = copy.deepcopy(rotated_block_datas[-1])
                    new_relative_positions = []
                    for relative_position in rotated_block_data['coordinates']:
                        new_relative_positions.append([-relative_position[1], relative_position[0]])
                    min_x = min(relative_position[0] for relative_position in new_relative_positions)
                    min_y = min(relative_position[1] for relative_position in new_relative_positions)
                    for relative_position in new_relative_positions:
                        relative_position[0] -= min_x
                        relative_position[1] -= min_y
                    rotated_block_data['coordinates'] = new_relative_positions
                    rotated_block_datas.append(rotated_block_data)

            # Apply buffs
            for rotated_block_data in rotated_block_datas:
                if self.abilities[f'buff_{rotated_block_data['name']}']:
                    rotated_block_data['frequency_scale'] *= 3

            frequency_sum = sum(block_data['frequency_scale'] for block_data in rotated_block_datas)
            for block_data in rotated_block_datas:
                self.all_blocks.append(BBInfiniteGame.Block(block_data['coordinates'], block_data['frequency_scale'] / frequency_sum))


    def _update_alive(self):

        available_wave_blocks = [block for block in self.wave_blocks if block is not None]
        available_hold_blocks = [block for block in self.hold_blocks if block is not None]

        if len(available_wave_blocks) <= (BBInfiniteGame.HOLD_SIZE - len(available_hold_blocks)):
            return

        available_blocks = available_wave_blocks + available_hold_blocks

        for x in range(BBBoard.BOARD_SIZE):
            for y in range(BBBoard.BOARD_SIZE):
                for block in available_blocks:
                    if self.board.place_block((x, y), block.relative_positions) is not None:
                        return

        self.alive = False
    
    def _generate_wave(self):

        for i in range(BBInfiniteGame.WAVE_SIZE):
            random_value = random.random()
            for block in self.all_blocks:
                if random_value <= block.frequency or block == self.all_blocks[-1]:
                    self.wave_blocks[i] = copy.deepcopy(block)
                    break
                random_value -= block.frequency


    def _pop_wave(self, wave_block):

        if wave_block is None or wave_block not in self.wave_blocks:
            return False
        
        self.wave_blocks[self.wave_blocks.index(wave_block)] = None
        if all(w is None for w in self.wave_blocks):
            self._generate_wave()

        return True
    

    def _pop_hold(self, hold_block):

        if hold_block is None or hold_block not in self.hold_blocks:
            return False
        
        self.hold_blocks[self.hold_blocks.index(hold_block)] = None

        return True
    

    def _add_life(self, life):

        self.life = min(self.life + life, BBInfiniteGame.MAX_LIFE)


    def hold_block(self, wave_block, hold_index):

        if wave_block is None or wave_block not in self.wave_blocks:
            return False
        
        if hold_index < 0 or hold_index >= BBInfiniteGame.HOLD_SIZE or self.hold_blocks[hold_index] is not None:
            return False
        
        self.hold_blocks[hold_index] = copy.deepcopy(wave_block)
        self._pop_wave(wave_block)

        return True
    

    def _place_block(self, block, anchor_position):

        new_board = self.board.place_block(anchor_position, block.relative_positions)
        if new_board is None:
            return False
        
        score = new_board.clear()
        self.score += score
        self._add_life(BBInfiniteGame.PLACE_REPLENISH if score == 0 else score * BBInfiniteGame.ROW_REPLENISH)
        self.board = new_board

        return True

    
    def place_wave_block(self, wave_block, anchor_position):

        if not self.alive or wave_block is None or wave_block not in self.wave_blocks:
            return False
        
        result = self._place_block(wave_block, anchor_position)

        if result:
            self._pop_wave(wave_block)
            self._update_alive()

        return result
    

    def place_hold_block(self, hold_block, anchor_position):

        if not self.alive or hold_block is None or hold_block not in self.hold_blocks:
            return False
        
        result = self._place_block(hold_block, anchor_position)

        if result:
            self._pop_hold(hold_block)
            self._update_alive()

        return result
    

    def start(self):

        self._generate_wave()
        self.started = True
        self.life = BBInfiniteGame.MAX_LIFE

    
    def update(self, dt):

        self.life = max(0, self.life - dt)
        if self.life == 0:
            self.alive = False