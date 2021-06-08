import chess



if __name__ == '__main__':
    board = chess.Board()

    print(board.unicode().replace('⭘','.'))
    board.push_san('e4')
    print(board.unicode().replace('⭘','.'))
    board.push_san('e5')
    print(board.unicode().replace('⭘','.'))

