import copy
import numpy as np


class BBBoard:


    BOARD_SIZE = 7


    def __init__(self, board=None):

        self.board = board
        if self.board is None:
            self.board = [[0 for _ in range(BBBoard.BOARD_SIZE)] for _ in range(BBBoard.BOARD_SIZE)]

        self.text = self._to_text()


    def filled_positions(self):
        """
        Get an (x, y) list of all the board positions marked with a 1.
        """
        positions = []
        for y in range(BBBoard.BOARD_SIZE):
            for x in range(BBBoard.BOARD_SIZE):
                if self.board[y][x] == 1:
                    positions.append((x, y))
        return positions


    def place_block(self, anchor_position, relative_positions):
        """
        Generate another BBBoard object with the new block inserted.

        Returns None if the block could not be inserted.
        """
        absolute_positions = []
        for relative_position in relative_positions:
            absolute_positions.append(np.add(anchor_position, relative_position).tolist())

        # Perform check
        for absolute_position in absolute_positions:
            if absolute_position[0] < 0 or absolute_position[1] < 0 or absolute_position[0] >= BBBoard.BOARD_SIZE or absolute_position[1] >= BBBoard.BOARD_SIZE:
                return None
            if self.board[absolute_position[1]][absolute_position[0]] == 1:
                return None

        # Generate new board
        new_board = copy.deepcopy(self.board)
        for absolute_position in absolute_positions:
            new_board[absolute_position[1]][absolute_position[0]] = 1
        
        return BBBoard(new_board)
    

    def clear(self):
        """
        Clears all available full rows and columns on the board.

        Returns the number of rows and columns cleared.
        """
        rows = []
        columns = []

        # Perform check
        for i in range(BBBoard.BOARD_SIZE):
            if all(self.board[i][j] == 1 for j in range(BBBoard.BOARD_SIZE)):
                rows.append(i)
            if all(self.board[j][i] == 1 for j in range(BBBoard.BOARD_SIZE)):
                columns.append(i)
        
        # Clear board
        for row in rows:
            self.board[row] = [0 for _ in range(BBBoard.BOARD_SIZE)]
        for column in columns:
            for row in range(BBBoard.BOARD_SIZE):
                self.board[row][column] = 0

        self.text = self._to_text()

        return len(rows) + len(columns)


    def _to_text(self):

        x_axis = '  ' + ' '.join(str(i) for i in range(1, BBBoard.BOARD_SIZE + 1))
        return '\n'.join(
            [x_axis] + 
            [' '.join(
                [str(y + 1)] +
                ['O' if value == 1 else '-' for value in self.board[y]]) for y in range(BBBoard.BOARD_SIZE)]
        )