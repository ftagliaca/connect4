from __future__ import annotations

import numpy as np

import tools as tl


class Game:
    """Game class for the game 'backend'
    """

    def __init__(self):
        """Initialize the game with a board full of zeros and no winner
        """

        self.board = np.zeros((6, 7))
        self.winner = 0

    def get_first_free_idx(self, col_n: int) -> int:
        """Function to get the first free index of a given column

        Args:
            col_n (int): The column number to check

        Returns:
            int: the first free index of the column (0 is the top row)
        """

        locations = np.where(self.board[:, col_n] == 0)[0]
        if len(locations) == 0:
            return -1
        return locations[-1]

    def place_token(self, col_n: int, token_id: int) -> tuple[int, int]:
        """Place a token in the indicated column, calls get_first_free_idx
        to get the first free index of the given column
        Calls check_win to check if the given token has won

        Args:
            col_n (int): The column number
            token_id (int): The token ID to place

        Returns:
            tuple[int, int]: The location where the token was placed
        """
        idx = self.get_first_free_idx(col_n)
        if idx != -1:
            self.board[idx, col_n] = token_id
            if self.check_win(idx, col_n):
                self.winner = token_id
            return idx, col_n

        return -1, -1

    def check_win(self, row_n: int, col_n: int) -> bool:
        """Check if the token has won
        Uses the tools.check_conseq_nums function to check if there are 4 consequtive numbers in the row,
        column or either diagonal

        Args:
            row_n (int): The row number of the token to check
            col_n (int): The column number of the token to check

        Returns:
            bool: Whether or not the given token has won
        """

        if self.board[row_n, col_n] == 0:
            return False

        conseq_n = 3
        row_n_min = max(row_n-conseq_n, 0)
        row_n_max = min(row_n+conseq_n+1, self.board.shape[0])
        col_n_min = max(col_n-conseq_n, 0)
        col_n_max = min(col_n+conseq_n+1, self.board.shape[1])
        row = self.board[row_n_min:row_n_max, col_n]
        col = self.board[row_n, col_n_min:col_n_max]
        arr = self.board[row_n_min:row_n_max, col_n_min:col_n_max]
        d1_row_n = row_n-row_n_min
        d1_col_n = col_n-col_n_min
        offset1 = d1_col_n - d1_row_n
        diag1 = arr.diagonal(offset1)
        d2_row_n = arr.shape[0] - 1 - d1_row_n
        d2_col_n = d1_col_n
        offset2 = d2_col_n - d2_row_n
        diag2 = np.flipud(arr).diagonal(offset2)
        row_win = tl.check_conseq_nums(row, conseq_n+1)[0]
        col_win = tl.check_conseq_nums(col, conseq_n+1)[0]
        diag1_win = tl.check_conseq_nums(diag1, conseq_n+1)[0]
        diag2_win = tl.check_conseq_nums(diag2, conseq_n+1)[0]

        return row_win or col_win or diag1_win or diag2_win

    def check_draw(self) -> bool:
        """Check if the game is a draw
        (All the columns are full)

        Returns:
            bool: true if the game is a draw
        """
        return np.all(self.board != 0)

    def make_move(self) -> tuple[int, int]:
        """Helper function to place a token for the AI
        Calls place_token to place a token in a random column

        Returns:
            tuple[int, int]: location of the placed token
        """
        row_n = -1
        while row_n == -1:
            col_n = np.random.randint(0, 6)
            row_n, col_n = self.place_token(col_n, 2)
        return row_n, col_n
