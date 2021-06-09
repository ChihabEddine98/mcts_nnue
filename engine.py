import chess
import chess.engine
from stockfish import Stockfish



if __name__ == '__main__':
    engine = chess.engine.SimpleEngine.popen_uci('stockfish')
    sf = Stockfish('/opt/homebrew/bin/stockfish')
    sf.set_fen_position("rnbk3r/ppp3pp/8/7n/3b4/2P5/PP1K1P1P/RNB4q b - -")
    print(sf.get_evaluation())

    board = chess.Board("rnbk3r/ppp3pp/8/7n/3b4/2P5/PP1K1P1P/RNB4q b - -")
    info = engine.analyse(board, chess.engine.Limit(depth=10), game=object())
    print(info["score"])


    print(board.unicode().replace('⭘','.'))



