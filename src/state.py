import numpy as  np
from copy import deepcopy



import chess
from stockfish import Stockfish

from src.value_net_test import Valuator


class State(object):
    def __init__(self,board=None):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board

    def first_player(self):
        return self.board.turn

    def do_action(self, action):
        # s = deepcopy(State(self.board))
        self.board.push(chess.Move.from_uci(action))
        return self

    def undo_action(self):
        self.board.pop()
        return self

    def actions(self):
        return [str(move) for move in self.board.legal_moves]

    def value(self):
        sf = Stockfish('/opt/homebrew/bin/stockfish')
        sf.set_fen_position(self.board.fen())
        # If there is no visible mate yet !
        if sf.get_evaluation()['type'] == "cp":
            return sf.get_evaluation()['value'] if self.first_player() else  -sf.get_evaluation()['value']
        # In case we have mate visible
        else:
            return sf.get_evaluation()['value']*1e6 if self.first_player() else  -sf.get_evaluation()['value']*1e6

    def value_nn(self):
        v = Valuator()
        return v(self)


    # Get whether the current game state is in the terminal state (win/draw/loss) or not
    def is_terminal(self):
        return self.board.is_game_over()

    def __str__(self):
        return f"\n----------------\n" \
               f"{self.board.unicode().replace('⭘', '.')}\n" \
               f"----------------"

    def serialize(self):
        assert self.board.is_valid()

        bstate = np.zeros(64, np.uint8)
        for i in range(64):
            pp = self.board.piece_at(i)
            if pp is not None:
                # print(i, pp.symbol())
                bstate[i] = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6, \
                             "p": 9, "n": 10, "b": 11, "r": 12, "q": 13, "k": 14}[pp.symbol()]
        if self.board.has_queenside_castling_rights(chess.WHITE):
            assert bstate[0] == 4
            bstate[0] = 7
        if self.board.has_kingside_castling_rights(chess.WHITE):
            assert bstate[7] == 4
            bstate[7] = 7
        if self.board.has_queenside_castling_rights(chess.BLACK):
            assert bstate[56] == 8 + 4
            bstate[56] = 8 + 7
        if self.board.has_kingside_castling_rights(chess.BLACK):
            assert bstate[63] == 8 + 4
            bstate[63] = 8 + 7

        if self.board.ep_square is not None:
            assert bstate[self.board.ep_square] == 0
            bstate[self.board.ep_square] = 8
        bstate = bstate.reshape(8, 8)

        # binary state
        state = np.zeros((5, 8, 8), np.uint8)

        # 0-3 columns to binary
        state[0] = (bstate >> 3) & 1
        state[1] = (bstate >> 2) & 1
        state[2] = (bstate >> 1) & 1
        state[3] = (bstate >> 0) & 1

        # 4th column is who's turn it is
        state[4] = (self.board.turn * 1.0)

        # 257 bits according to readme
        return state


