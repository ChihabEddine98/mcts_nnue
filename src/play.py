from src.chess_player import ChessPlayer
from src.state import State
from src.alpha_beta_search import AlphaBeta
from src.ubfms import UBFMS


# Evaluation Policy using Stockfish's NNUE algorithm
def nnue_policy(state):
    return state.value()

def main():

    results = []
    nb_games = 11

    for i in range(nb_games):

        # Initial State
        state = State()

        # Searches Methods to compare
        alpha_beta = AlphaBeta(root=state, eval_policy=nnue_policy, depth=1)
        ubfms = UBFMS(root=state, eval_policy=nnue_policy)

        # Players
        player1 = ChessPlayer(search_policy=ubfms)
        player2 = ChessPlayer(search_policy=alpha_beta)
        players = [player1, player2]

        print(f'\n---------------------- Start of Match {i + 1} ------------------------')
        while not state.is_terminal():

            # We will play half games in black for each search approach
            if i % 2 == 0:
                w_player, b_player = players[0] , players[1]
            else:
                w_player, b_player = players[1] , players[0]

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
                print(f'\n---------------------- END of Match {i+1} ------------------------')
                print(f'    Score : {state.board.outcome().result()}')
                print(f'\n------------------------------------------------------------------')

    with open('results.txt', 'w') as f:
        for result in results:
            f.write("%s\n" % result)












if __name__ == '__main__':
    main()