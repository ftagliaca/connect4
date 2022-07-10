from __future__ import annotations

import pygame as pg

from game import Game


class App:
    """_summary_
    test
    """

    def __init__(self):
        self.bg_col = (246, 246, 246)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.black = (0, 0, 0)
        self.gray = (163, 163, 163)

        self.game = Game()

        self.turn = 1

        self.testing = False

    def start_pg(self):
        """
        Helper function to intialize and start pygame
        """
        pg.init()

        self.xmax = 900
        self.ymax = 700
        self.res = (self.xmax, self.ymax)
        self.min_margin = 50
        self.sqWidth = min(
            (self.xmax-self.min_margin*2)/self.game.board.shape[1],
            (self.ymax-self.min_margin*2)/self.game.board.shape[0],
        )
        self.xmargin = (self.xmax-self.sqWidth*self.game.board.shape[1])/2
        self.ymargin = (self.ymax-self.sqWidth*self.game.board.shape[0])/2
        self.center = (self.xmax/2, self.ymax/2)

        self.screen = pg.display.set_mode(self.res)
        pg.display.set_caption('Connect4')

        self.winnerFont = pg.font.SysFont('Arial', 40)

        self.clock = pg.time.Clock()
        self.running = True

        pg.font.init()

    def stop_pg(self):
        """
        Helper function to stop pygame
        """
        pg.quit()

    def run_app(self):
        self.start_pg()
        self.main_app()
        self.stop_pg()

    def main_app(self):
        while self.running:

            pg.event.pump()

            self.screen.fill(self.bg_col)

            self.draw_grid()

            self.draw_circles()

            self.display_winner()

            self.display_draw()

            if self.turn == 2:
                self.game.make_move()
                self.turn = 0 if self.game.winner == 2 else 1

            self.handle_events()

            pg.display.update()

            if self.testing:
                return

    def handle_events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.reset_game()
            elif event.type == pg.MOUSEBUTTONUP:
                select_pos = self.mouse2idx(pg.mouse.get_pos())
                if self.turn == 1 and select_pos != (-1, -1):
                    token_loc = self.game.place_token(select_pos[1], 1)
                    if self.game.winner == 1:
                        self.turn = 0
                    elif token_loc != (-1, -1):
                        self.turn = 2

    def draw_grid(self):
        for vertical_idx in range(self.game.board.shape[1]+1):
            x_pos = self.xmargin+vertical_idx*self.sqWidth
            y_start = self.ymargin
            y_end = self.ymax-self.ymargin
            pg.draw.line(self.screen, self.gray, (x_pos, y_start), (x_pos, y_end), width=5)
        for horizontal_idx in range(self.game.board.shape[0]+1):
            x_start = self.xmargin
            x_end = self.xmax-self.xmargin
            y_pos = self.ymargin+horizontal_idx*self.sqWidth
            pg.draw.line(self.screen, self.gray, (x_start, y_pos), (x_end, y_pos), width=5)

    def draw_circles(self):
        for i, row in enumerate(self.game.board):
            for j, num in enumerate(row):
                center = (
                    self.xmargin+self.sqWidth*(j + 0.5),
                    self.ymargin+self.sqWidth*(i + 0.5),
                )
                if num != 0:
                    color = self.red if num == 1 else self.blue
                    pg.draw.circle(self.screen, color, center, self.sqWidth/2 - 5)

    def mouse2idx(self, pos: tuple) -> tuple:
        if not self.xmargin <= pos[0] <= (self.xmax-self.xmargin) or\
           not self.ymargin <= pos[1] <= (self.ymax-self.ymargin):
            return -1, -1
        idx_x = (pos[0]-self.xmargin)*self.game.board.shape[1]//(self.xmax-self.xmargin*2)
        idx_y = (pos[1]-self.ymargin)*self.game.board.shape[0]//(self.ymax-self.ymargin*2)
        return int(idx_y), int(idx_x)

    def display_winner(self):
        if self.game.winner != 0:
            winner_text = self.winnerFont.render(
                f'Player {self.game.winner} wins!', True,
                self.red if self.game.winner == 1 else self.blue,
            )
            winner_rect = winner_text.get_rect()
            winner_rect.center = self.center
            self.screen.blit(winner_text, winner_rect)

    def display_draw(self):
        if self.game.winner == 0 and self.game.check_draw():
            self.turn = 0
            draw_text = self.winnerFont.render('Draw!', True, self.black)
            draw_rect = draw_text.get_rect()
            draw_rect.center = self.center
            self.screen.blit(draw_text, draw_rect)

    def reset_game(self):
        self.game = Game()
        self.turn = 1


if __name__ == '__main__':
    connect4app = App()
    connect4app.run_app()
