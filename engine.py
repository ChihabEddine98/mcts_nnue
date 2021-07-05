
import chess.pgn
import chess.engine
from stockfish import Stockfish

from src.alpha_beta_search import AlphaBeta
from src.mcts import MCTS, custom_policy, nnue_policy
from src.state import State
from src.ubfms import UBFMS
from src.config import value_model_config as vmc

if __name__ == '__main__':
    sf = Stockfish('/opt/homebrew/bin/stockfish')
    sf.set_fen_position("r4b1r/ppp2p1p/8/6Q1/3k4/8/PPPP1PPP/RNB1KBNR w KQ -")
    #print(sf.get_evaluation())

    s = "rnbk3r/ppp3pp/8/7n/3b4/2P5/PP1K1P1P/RNB4q b - -"
    board = chess.Board("rnbqkbnr/pppp1ppp/8/6N1/4P3/4K3/PP3PPP/RNBq1B1R b kq -")
    state = State(board)
    #print(state.evaluation())

    c = 'r1bqk2r/pppp1ppp/2n5/1Bb1p3/8/1PN2N2/PBPP1PPP/R2Q1RK1 b kq - 0 7'
    board = chess.Board('1rbq1rk1/p1N2p1p/2pp2p1/8/3P2Q1/1P6/PBP2KPP/R3R3 b - - 0 1')
    s = State()
    ubfm = UBFMS(s)
    mcts = MCTS(root=s,iteration_limit=50,rollout_policy=custom_policy)
    alpha_beta = AlphaBeta(root=s,eval_policy=nnue_policy,depth=2)


    print(alpha_beta())



