from src.chess_player import ChessPlayer
from src.state import State
from src.alpha_beta_search import AlphaBeta
from src.ubfms import UBFMS


# Evaluation Policy using Stockfish's NNUE algorithm
def nnue_policy(state):
    return state.value()

def main():
    # Initial State
    state = State()

    # Searches Methods to compare
    alpha_beta = AlphaBeta(root=state,eval_policy=nnue_policy,depth=2)
    ubfms = UBFMS(root=state,eval_policy=nnue_policy,depth=2)

    # Players
    white = ChessPlayer(search_policy=ubfms)
    black = ChessPlayer(search_policy=ubfms)

    while True:
        w_action = white.play(state)
        state = state.do_action(w_action)
        print(f' White : {w_action} \n {state}')
        b_action = black.play(state)
        state = state.do_action(b_action)
        print(f' Black : {b_action} \n {state}')










if __name__ == '__main__':
    main()