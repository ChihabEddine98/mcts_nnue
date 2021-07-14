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
    alpha_beta = AlphaBeta(root=state,eval_policy=nnue_policy,depth=1)
    ubfms = UBFMS(root=state,eval_policy=nnue_policy,depth=2)

    # Players
    player1 = ChessPlayer(search_policy=ubfms)
    player2 = ChessPlayer(search_policy=alpha_beta)

    # For now its self play ubfms
    # TODO -----
    #   Fix [ got e8h8 in 7q/8/5kpK/7p/7P/8/8/8 ]
    players = [player1,player2]
    results = []
    nb_games = 2

    for i in range(nb_games):
        print(f'\n---------------------- Start of Match {i + 1} ------------------------')
        while not state.is_terminal():

            # We will play half games in black for each search approach
            if i <= nb_games // 2:
                w_player, b_player = players[0] , players[1]
            else:
                w_player, b_player = players[1] , players[0]

            w_action = w_player.play(state)
            if w_action is None:
                break

            state = state.do_action(w_action)
            print(f' Player1 (White) : {w_action} \n {state}')
            b_action = b_player.play(state)
            if w_action is None:
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