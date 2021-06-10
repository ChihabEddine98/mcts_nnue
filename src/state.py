import numpy as  np



import chess
from stockfish import Stockfish



class State(object):
    def __init__(self,board=None,parent=None):
        self.board = board
        self.parent = parent

    def make_action(self,action):
        self.board.push(chess.Move.from_uci(action))
        return self

    def actions(self):
        return [str(move) for move in self.board.legal_moves]

    def evaluation(self):
        sf = Stockfish('/opt/homebrew/bin/stockfish')
        sf.set_fen_position(self.board.fen())
        # If there is no visible mate yet !
        if sf.get_evaluation()['type'] == "cp":
            return sf.get_evaluation()['value']
        # In case we have mate visible
        else:
            return np.sign(sf.get_evaluation()['value'])*float('inf')

    # Get whether the current game state is in the terminal state (win/draw/loss) or not
    def is_terminal(self):
        return self.board.is_game_over()

    def __str__(self):
        return f"\n----------------\n" \
               f"{self.board.unicode().replace('⭘', '.')}\n" \
               f"----------------"


