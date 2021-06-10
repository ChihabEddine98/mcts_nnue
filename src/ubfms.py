from time import time


class Node(object):
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
        self.is_terminal = state.is_terminal()


class UBFMS(object):
    def __init__(self,root):
        self.root = State(state=root,parent=None)

    def search(self):

    def ub_minimax(self,state,tho):
        t = time()
        while (time()- t < tho) :
            self.ub_minimax_iter(state)
        return self.best_action(state)

    def ub_minimax_iter(self, state):
        if state.is_terminal:

        pass

    def best_action(self, state):
        pass


