import os
import torch

from src.value_net_train import Net





class Valuator(object):
    def __init__(self):
        vals = torch.load(os.path.join(os.getcwd(),'models','value.pth'),
                          map_location=lambda storage,
                          loc: storage)
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self, state):
        ser = state.serialize()[None]
        output = self.model(torch.tensor(ser).float())
        return float(output.data[0][0])

'''
if __name__ == '__main__':
    v = Valuator()

    board = chess.Board('1rbq1rk1/p1N2p1p/2pp2p1/8/3P2Q1/1P6/PBP2KPP/R3R3 b - -')
    s = State(board)
    print(f' Current State \n {s}')
    print(f' Custom Valuator : {v(s)} ')
    print(f' NNUE Valuator : {s.value()} ')
'''