import chess
import chess.engine
from stockfish import Stockfish
from src.state import State
import operator

if __name__ == '__main__':
    sf = Stockfish('/opt/homebrew/bin/stockfish')
    sf.set_fen_position("r4b1r/ppp2p1p/8/6Q1/3k4/8/PPPP1PPP/RNB1KBNR w KQ -")
    print(sf.get_evaluation())

    s = "rnbk3r/ppp3pp/8/7n/3b4/2P5/PP1K1P1P/RNB4q b - -"
    board = chess.Board("rnbqkbnr/pppp1ppp/8/6N1/4P3/4K3/PP3PPP/RNBq1B1R b kq -")
    state = State(board)
    print(state.evaluation())

    stats = {('a',1):1000, ('b',2):3000, ('c',3): 100, ('d',4):3000}
    print(min(stats.items(), key=operator.itemgetter(1))[0])





