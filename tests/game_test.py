from __future__ import annotations

import unittest
from unittest.mock import patch

import numpy as np

from game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_get_first_free_idx(self):

        self.game.board = np.zeros((6, 7))
        self.game.board[-1, :] = 1
        self.game.board[-2, :3] = 2
        self.game.board[-3, 2] = 1

        lst_idxs = [-3, -3, -4, -2, -2, -2, -2]

        for col_n, last_idx in enumerate(lst_idxs):
            self.assertEqual(self.game.get_first_free_idx(col_n), last_idx + 6)

        self.game.board[:, -1] = 1
        self.assertEqual(self.game.get_first_free_idx(6), -1)

    @patch('game.Game.check_win')
    @patch('game.Game.get_first_free_idx')
    def test_place_token(self, mock_get_first_free_idx, mock_check_win):
        # Reset board, just to be sure
        self.game.board = np.zeros((6, 7))

        # Checking that the function places the token in the correct spot
        # Since win is set to return False, make sure that there is no winner

        mock_get_first_free_idx.return_value = 5
        mock_check_win.return_value = False
        ret = self.game.place_token(0, 1)
        self.assertEqual(ret, (5, 0))
        self.assertEqual(self.game.board[5, 0], 1)
        self.assertEqual(self.game.winner, 0)
        self.assertEqual(mock_get_first_free_idx.call_count, 1)
        self.assertEqual(mock_check_win.call_count, 1)

        # Now we do the same, but now there is a winner

        self.game.winner = 0
        mock_get_first_free_idx.return_value = 5
        mock_check_win.return_value = True
        ret = self.game.place_token(0, 1)
        self.assertEqual(ret, (5, 0))
        self.assertEqual(self.game.board[5, 0], 1)
        self.assertEqual(self.game.winner, 1)
        self.assertEqual(mock_get_first_free_idx.call_count, 2)
        self.assertEqual(mock_check_win.call_count, 2)
        self.game.winner = 0

        # Now we do the same, but now the column is full (idx = -1)
        # Note that in this case the token is not placed
        # and the win function should not be called

        mock_get_first_free_idx.return_value = -1
        ret = self.game.place_token(2, 1)
        self.assertEqual(ret, (-1, -1))
        self.assertEqual(self.game.board[5, 2], 0)
        self.assertEqual(self.game.winner, 0)
        self.assertEqual(mock_get_first_free_idx.call_count, 3)
        self.assertEqual(mock_check_win.call_count, 2)

    def test_check_win(self):

        # Checking where winners are found in the following board
        # (checks all 4 directions and both players)
        # 0 0 0 0 0 0 0
        # 0 0 0 1 0 0 0
        # 0 0 0 1 1 0 1
        # 0 0 1 2 2 1 1
        # 0 1 2 2 2 2 1
        # 1 1 1 2 1 1 1

        self.game.board = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1],
            [0, 0, 1, 2, 2, 1, 1],
            [0, 1, 2, 2, 2, 2, 1],
            [1, 1, 1, 2, 1, 1, 1],
        ])

        should_win = np.array([
            [False, False, False, False, False, False, False],
            [False, False, False, True, False, False, False],
            [False, False, False, True, True, False, True],
            [False, False, True, False, False, True, True],
            [False, True, True, True, True, True, True],
            [True, False, False, False, False, False, True],
        ])

        # Check spots that should not have a win
        self.assertFalse(self.game.check_win(5, 1))
        self.assertFalse(self.game.check_win(5, 3))
        self.assertFalse(self.game.check_win(5, 5))

        # Check some spots that should have a win
        self.assertTrue(self.game.check_win(5, 0))
        self.assertTrue(self.game.check_win(5, 6))
        self.assertTrue(self.game.check_win(4, 1))
        self.assertTrue(self.game.check_win(4, 2))
        self.assertTrue(self.game.check_win(4, 3))
        self.assertTrue(self.game.check_win(4, 5))

        # Check all spots and compare with the should_win array

        for i, row in enumerate(self.game.board):
            for j, num in enumerate(row):
                self.assertEqual(self.game.check_win(i, j), should_win[i, j])

    def test_check_draw(self):
        self.game.board = np.zeros((6, 7))
        self.assertFalse(self.game.check_draw())

        self.game.board[:, :3] = 1
        self.assertFalse(self.game.check_draw())

        self.game.board = np.ones_like(self.game.board)
        self.assertTrue(self.game.check_draw())

    @patch('numpy.random.randint')
    @patch('game.Game.place_token')
    def test_make_move_correct_output(self, mock_place_token, mock_random):
        # Reset board, just to be sure
        self.game.board = np.zeros((6, 7))

        # Checking that the function returns the correct location
        mock_random.return_value = 1
        mock_place_token.return_value = [0, 1]
        ret = self.game.make_move()
        self.assertEqual(ret, (0, 1))
        self.assertEqual(mock_place_token.call_count, 1)
        self.assertEqual(mock_random.call_count, 1)

        # Check that if the place_token function return -1
        # the while loops keeps searcing for a valid move
        # until the place_token function returns a valid move

        mock_place_token.side_effect = [(-1, -1), (-1, -1), (2, 0)]
        ret = self.game.make_move()
        self.assertEqual(ret, (2, 0))
        self.assertEqual(mock_place_token.call_count, 4)
        self.assertEqual(mock_random.call_count, 4)
