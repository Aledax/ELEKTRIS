import os

from lib.blockblast.infinitegame import BBInfiniteGame


if __name__ == '__main__':

    game = BBInfiniteGame(os.path.join('data', 'blocks.json'))

    while True:

        print(f'\n{game.board.text}')
        for i in range(BBInfiniteGame.WAVE_SIZE):
            if game.wave_blocks[i] is not None:
                print(f'\n{i + 1}.\n\n{game.wave_blocks[i].text}')

        inp = input('\n> ')
        inp_values = inp.split(',')
        if len(inp_values) == 3 and all(value.isdigit() for value in inp_values):
            game.place_wave_block(int(inp_values[0]) - 1, (int(inp_values[1]) - 1, int(inp_values[2]) - 1))