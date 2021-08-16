import os
import csv

import chess

from src.chess_player import ChessPlayer
from src.state import State
from src.alpha_beta_search import AlphaBeta
from src.ubfms import UBFMS
from src.config import WARNING,ENDC


# Evaluation Policy using Stockfish's NNUE algorithm
def nnue_policy(state):
    return state.value()

def main():

    results = []

    with open(os.path.join('..','data','opennings.csv'),'r') as op:
        reader = csv.reader(op)
        fens = [row[1] for row in reader]


    for i in range(len(fens)):

        # Initial Game Board
        board = chess.Board(fens[i])

        # Initial State
        state = State(board)

        # Searches Methods to compare
        alpha_beta = AlphaBeta(root=state, eval_policy=nnue_policy, depth=2)
        ubfms = UBFMS(root=state, eval_policy=nnue_policy)

        # Players
        player1 = ChessPlayer(search_policy=alpha_beta)
        player2 = ChessPlayer(search_policy=ubfms)
        players = [player1, player2]



        print(f'{WARNING}\n---------------------- Start of Match {i + 1} ------------------------ {ENDC}')
        while not state.is_terminal():
            w_player, b_player = players[0] , players[1]
            w_action = w_player.play(state)
            if w_action is None:
                break

            state = state.do_action(w_action)
            print(f' Player1 (White) : {w_action} \n {state}')
            b_action = b_player.play(state)
            if b_action is None:
                break

            state = state.do_action(b_action)
            print(f' Player2 (Black) : {b_action} \n {state}')

            if state.is_terminal():
                results.append(state.board.outcome().result())
                print(f'{WARNING} \n---------------------- END of Match {i+1} ------------------------ {ENDC}')
                print(f'    Score : {state.board.outcome().result()}')
                print(f'\n------------------------------------------------------------------')

    with open('results.txt', 'w') as f:
        for result in results:
            f.write("%s\n" % result)












if __name__ == '__main__':
    main()