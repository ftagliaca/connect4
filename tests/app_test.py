from __future__ import annotations

import unittest
from unittest import mock
from unittest.mock import patch

import numpy as np
import pygame as pg

from app import App
from game import Game


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.app.testing = True

    def test_init(self):
        self.assertEqual(self.app.bg_col, (246, 246, 246))
        self.assertEqual(self.app.red, (255, 0, 0))
        self.assertEqual(self.app.green, (0, 255, 0))
        self.assertEqual(self.app.blue, (0, 0, 255))
        self.assertEqual(self.app.black, (0, 0, 0))
        self.assertEqual(self.app.gray, (163, 163, 163))
        self.assertEqual(self.app.turn, 1)
        self.assertIsInstance(self.app.game, Game)

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.font.SysFont')
    @patch('pygame.time.Clock')
    @patch('pygame.font.init')
    def test_startPG(
        self, mock_font_init, mock_clock, mock_sysfont,
        mock_set_caption, mock_set_mode, mock_init,
    ):
        self.app.start_pg()
        mock_init.assert_called_once()
        mock_set_mode.assert_called_once()
        mock_set_caption.assert_called_once()
        mock_sysfont.assert_called_once()
        mock_clock.assert_called_once()
        mock_font_init.assert_called_once()

        self.assertEqual(self.app.sqWidth, 100)
        self.assertEqual(self.app.xmargin, 100)
        self.assertEqual(self.app.ymargin, 50)
        self.assertEqual(self.app.center, (450, 350))
        self.assertTrue(self.app.running)

    @patch('pygame.quit')
    def test_stopPG(self, mock_quit):
        self.app.stop_pg()
        mock_quit.assert_called_once()

    @patch('app.App.start_pg')
    @patch('app.App.main_app')
    @patch('app.App.stop_pg')
    def test_run_app(self, mock_stop, mock_main_app, mock_start):
        self.app.run_app()
        mock_start.assert_called_once()
        mock_main_app.assert_called_once()
        mock_stop.assert_called_once()

    @patch('pygame.event.pump')
    @patch('app.App.draw_grid')
    @patch('app.App.draw_circles')
    @patch('app.App.display_winner')
    @patch('app.App.display_draw')
    @patch('game.Game.make_move')
    @patch('app.App.handle_events')
    @patch('pygame.display.update')
    def test_main_app(
        self, mock_update, mock_handle_events, mock_make_move, mock_display_draw,
        mock_display_winner, mock_draw_circles, mock_draw_grid, mock_event_pump,
    ):

        self.app.screen = mock.Mock()
        mock_fill = mock.PropertyMock()
        self.app.screen.fill = mock_fill
        self.app.running = False
        self.app.main_app()
        self.assertFalse(mock_event_pump.called)
        self.assertFalse(mock_fill.called)
        self.assertFalse(mock_draw_grid.called)
        self.assertFalse(mock_draw_circles.called)
        self.assertFalse(mock_display_winner.called)
        self.assertFalse(mock_display_draw.called)
        self.assertFalse(mock_make_move.called)
        self.assertFalse(mock_handle_events.called)
        self.assertFalse(mock_update.called)

        self.app.running = True
        # The following is used to make sure running is immediately set to False
        self.app.turn = 1
        self.app.main_app()
        self.assertEqual(mock_update.call_count, 1)
        self.assertEqual(mock_handle_events.call_count, 1)
        self.assertFalse(mock_make_move.called)
        self.assertEqual(mock_display_draw.call_count, 1)
        self.assertEqual(mock_display_winner.call_count, 1)
        self.assertEqual(mock_draw_circles.call_count, 1)
        self.assertEqual(mock_draw_grid.call_count, 1)
        self.assertEqual(mock_event_pump.call_count, 1)

        self.app.turn = 2
        self.app.game.winner = 1
        self.app.main_app()
        self.assertEqual(mock_update.call_count, 2)
        self.assertEqual(mock_handle_events.call_count, 2)
        self.assertEqual(mock_make_move.call_count, 1)
        self.assertEqual(mock_display_draw.call_count, 2)
        self.assertEqual(mock_display_winner.call_count, 2)
        self.assertEqual(mock_draw_circles.call_count, 2)
        self.assertEqual(mock_draw_grid.call_count, 2)
        self.assertEqual(mock_event_pump.call_count, 2)
        self.assertEqual(self.app.turn, 1)

        self.app.turn = 2
        self.app.game.winner = 2
        self.app.main_app()
        self.assertEqual(mock_update.call_count, 3)
        self.assertEqual(mock_handle_events.call_count, 3)
        self.assertEqual(mock_make_move.call_count, 2)
        self.assertEqual(mock_display_draw.call_count, 3)
        self.assertEqual(mock_display_winner.call_count, 3)
        self.assertEqual(mock_draw_circles.call_count, 3)
        self.assertEqual(mock_draw_grid.call_count, 3)
        self.assertEqual(mock_event_pump.call_count, 3)
        self.assertEqual(self.app.turn, 0)

    @patch('app.App.reset_game')
    @patch('app.App.mouse2idx')
    @patch('game.Game.place_token')
    @patch('pygame.mouse.get_pos')
    @patch('pygame.event.get')
    def test_handle_events(self, mock_get_events, mock_get_pos, mock_place_token, mock_mouse2idx, mock_reset_game):
        mock_get_events.side_effect = [
            [pg.event.Event(pg.QUIT)],
            [pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE)],
            [pg.event.Event(pg.KEYDOWN, key=pg.K_r)],
            [pg.event.Event(pg.MOUSEBUTTONUP)],
            [pg.event.Event(pg.MOUSEBUTTONUP)],
            [pg.event.Event(pg.MOUSEBUTTONUP)],
            [pg.event.Event(pg.MOUSEBUTTONUP)],
        ]

        self.app.running = True
        self.app.handle_events()
        self.assertEqual(mock_get_events.call_count, 1)
        self.assertFalse(self.app.running)
        self.assertFalse(mock_reset_game.called)
        self.assertFalse(mock_mouse2idx.called)
        self.assertFalse(mock_place_token.called)

        self.app.running = True
        self.app.handle_events()
        self.assertEqual(mock_get_events.call_count, 2)
        self.assertFalse(self.app.running)
        self.assertFalse(mock_reset_game.called)
        self.assertFalse(mock_mouse2idx.called)
        self.assertFalse(mock_place_token.called)

        self.app.running = True
        self.app.handle_events()
        self.assertEqual(mock_get_events.call_count, 3)
        self.assertEqual(mock_reset_game.call_count, 1)
        self.assertTrue(self.app.running)
        self.assertFalse(mock_mouse2idx.called)
        self.assertFalse(mock_place_token.called)

        self.app.running = True
        self.app.turn = 2
        self.app.handle_events()
        self.assertEqual(mock_get_events.call_count, 4)
        self.assertTrue(self.app.running)
        self.assertEqual(mock_reset_game.call_count, 1)
        self.assertEqual(mock_mouse2idx.call_count, 1)
        self.assertFalse(mock_place_token.called)

        self.app.running = True
        self.app.turn = 1
        mock_mouse2idx.return_value = (-1, -1)
        self.app.handle_events()
        self.assertEqual(mock_get_events.call_count, 5)
        self.assertTrue(self.app.running)
        self.assertEqual(mock_reset_game.call_count, 1)
        self.assertEqual(mock_mouse2idx.call_count, 2)
        self.assertFalse(mock_place_token.called)

        self.app.running = True
        self.app.turn = 1
        self.app.game.winner = 0
        mock_mouse2idx.return_value = (0, 0)
        self.app.handle_events()
        self.assertEqual(mock_get_events.call_count, 6)
        self.assertTrue(self.app.running)
        self.assertEqual(mock_reset_game.call_count, 1)
        self.assertEqual(mock_mouse2idx.call_count, 3)
        self.assertEqual(mock_place_token.call_count, 1)
        self.assertEqual(self.app.turn, 2)

        self.running = True
        self.app.turn = 1
        self.app.game.winner = 1
        mock_mouse2idx.return_value = (0, 0)
        self.app.handle_events()
        self.assertEqual(mock_get_events.call_count, 7)
        self.assertTrue(self.app.running)
        self.assertEqual(mock_reset_game.call_count, 1)
        self.assertEqual(mock_mouse2idx.call_count, 4)
        self.assertEqual(mock_place_token.call_count, 2)
        self.assertEqual(self.app.turn, 0)

    @patch('pygame.draw.line')
    def test_draw_grid(self, mock_draw_line):
        self.app.xmax = 900
        self.app.ymax = 700
        self.app.xmargin = 100
        self.app.ymargin = 50
        self.app.sqWidth = 100
        self.app.screen = None
        self.app.gray = None
        self.app.draw_grid()
        self.assertEqual(mock_draw_line.call_count, 15)

    @patch('pygame.draw.circle')
    def test_draw_circle(self, mock_draw_circle):
        self.app.xmax = 900
        self.app.ymax = 700
        self.app.xmargin = 100
        self.app.ymargin = 50
        self.app.sqWidth = 100
        self.app.screen = None
        self.app.red = 'red'
        self.app.blue = 'blue'

        self.app.game.board = np.zeros((6, 7))
        self.app.draw_circles()
        self.assertFalse(mock_draw_circle.called)

        self.app.game.board = np.array([[1]])
        self.app.draw_circles()
        mock_draw_circle.assert_called_with(None, 'red', (150, 100), 45)

        self.app.game.board = np.array([[2]])
        self.app.draw_circles()
        self.assertEqual(mock_draw_circle.mock_calls[-1], mock.call(None, 'blue', (150, 100), 45))

    def test_mouse_2_idx(self):
        self.app.xmax = 900
        self.app.ymax = 700
        self.app.xmargin = 100
        self.app.ymargin = 50

        self.assertEqual(self.app.mouse2idx((0, 0)), (-1, -1))
        self.assertEqual(self.app.mouse2idx((900, 700)), (-1, -1))
        self.assertEqual(self.app.mouse2idx((100, 50)), (0, 0))
        self.assertEqual(self.app.mouse2idx((100, 150)), (1, 0))
        self.assertEqual(self.app.mouse2idx((200, 250)), (2, 1))

    def test_display_winner(self):

        self.app.winnerFont = mock.Mock()
        render_mock = mock.PropertyMock()
        self.app.winnerFont.render = render_mock

        self.app.center = None
        self.app.screen = mock.Mock()

        self.app.game.winner = 0
        self.app.display_winner()
        self.assertFalse(render_mock.called)

        self.app.game.winner = 1
        self.app.display_winner()
        render_mock.assert_called_once()

    @patch('game.Game.check_draw')
    def test_display_draw(self, mock_draw):
        self.app.winnerFont = mock.Mock()
        render_mock = mock.PropertyMock()
        self.app.winnerFont.render = render_mock

        self.app.center = None
        self.app.screen = mock.Mock()

        mock_draw.return_value = False
        self.app.game.winner = 0
        self.app.turn = 1
        self.app.display_draw()
        self.assertEqual(self.app.turn, 1)
        self.assertFalse(render_mock.called)

        mock_draw.return_value = True
        self.app.game.winner = 1
        self.app.turn = 1
        self.app.display_draw()
        self.assertEqual(self.app.turn, 1)
        self.assertFalse(render_mock.called)

        mock_draw.return_value = False
        self.app.game.winner = 1
        self.app.turn = 1
        self.app.display_draw()
        self.assertEqual(self.app.turn, 1)
        self.assertFalse(render_mock.called)

        mock_draw.return_value = True
        self.app.game.winner = 0
        self.app.turn = 1
        self.app.display_draw()
        self.assertEqual(self.app.turn, 0)
        render_mock.assert_called_once()

    def test_reset_game(self):
        self.app.turn = 5
        self.app.game = None

        self.app.reset_game()

        self.assertEqual(self.app.turn, 1)
        self.assertIsInstance(self.app.game, Game)
