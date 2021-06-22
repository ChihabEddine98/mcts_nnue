import os
import chess.pgn
import numpy as np
from state import State

def get_dataset(num_samples=None):
  # Init used variables
  X,y = [], []          # features , labels
  gn = 0                # Game Number
  values = {'1/2-1/2': 0, '0-1':-1, '1-0':1}   # Game result representation


  # Open file containing games
  pgn = open(os.path.join('..','data', '120K_games.pgn'))

  # Do while games are not parsed :
  while 1:
    game = chess.pgn.read_game(pgn)

    # If we reached the last game then we break the loop
    if game is None:
      break

    # Get game's result format ('1/2,1/2','0-1','1-0')
    res = game.headers['Result']

    # If we got an undefined result format we pass to next iteration
    if res not in values:
      continue

    # Get actual game board
    value = values[res]
    board = game.board()

    # For all moves in games mainline moves we save the board after
    # pushing this move with the final result for labels (y)
    '''
      For example lets say the game has this moves : 
        1. e4 2. e5 3.Nf3 ... etc 
        Then in this case we will save the board in which we made the e4 move 
        and another board with e5 in it , so in this way we will get 
        all states of our game after each move. 
    '''
    for i, move in enumerate(game.mainline_moves()):
      board.push(move)
      ser = State(board).serialize()
      X.append(ser)
      y.append(value)

    # Visualize charging state
    print("parsing game %d, got %d examples" % (gn, len(X)))


    # If we exceed maximal number of states we need then in this case
    # We can stop serializing more data
    if num_samples is not None and len(X) > num_samples:
      return np.array(X),np.array(Y)

    # When we finish to push all moves of game $(i) we can pass to game $(i+1)
    gn += 1

  return np.array(X), np.array(Y)

if __name__ == "__main__":
  X,Y = get_dataset(1e4)
  print(f'({np.sum(Y==-1)})')
  np.savez(os.path.join('..','data','dataset_120K.npz'), X, Y)

