





# In this Class we have an implmenatation for the Alpha-Beta Alogrithm
# Using the Negamax Framework to avoid writing the same code for max and
# min cases separatly

class AlphaBeta(object):

    def __init__(self,root,depth=4):
        self.depth = depth
        self.root = root

    def __call__(self, *args, **kwargs):
        return self.search(self.depth,self.root,float("-inf"),float("inf"))

    def search(self,depth,state,alpha,beta):
        if state.is_terminal() or depth == 0 :
            return state.value()

        for action in state.actions():
            state = state.do_action(action)
            score = -self.search(depth-1,state,-beta,-alpha)
            if score >= beta :
                return beta
            if score > alpha :
                alpha = score

        return alpha
