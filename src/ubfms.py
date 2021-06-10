from time import time
import operator


class Node(object):
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
        self.is_terminal = state.is_terminal()


class UBFMS(object):
    def __init__(self,root):
        self.root = Node(state=root,parent=None)
        # Transposition Table which will have the following struct
        '''
            T : { s1: e1 , s2: e2 , s3: e3 .... }
        '''
        self.T = {}
        # it will have this structure
        '''
            v(s,a) : { (s1,a1): v(s1,a1) , (s2,a2): v(s2,a2) , (s3,a3): v(s3,a3) .... }
        '''
        self.v = {}

    # Execute the UBFMS search from root node
    def search(self):
        return self.ub_minimax(self.root)
    # unbounded minimax search starting from state #state
    def ub_minimax(self,state,tho):
        t = time()
        while (time()- t < tho) :
            self.ub_minimax_iter(state)
        return self.best_action(state)

    # unbounded minimax search iteration on state #state
    def ub_minimax_iter(self, state):
        if state.is_terminal:
            return state.state.evaluation()
        if state not in self.T:
            self.T[state] = state.state.evaluation()
            for a in state.state.actions():
                self.v[(state,a)] = state.state.make_action(a).evaluation()
        else:
            a_b = self.best_action(state)
            self.v[(state, a_b)] = self.ub_minimax_iter(state.state.make_action(a_b))

        a_b = self.best_action(state)

        return self.v[(state,a_b)]

    # Get the best available action from current state #state for the current player (white,black)
    def best_action(self, state):
        if state.state.first_player():
            return max(self.v.items(), key=operator.itemgetter(1))[0][1]
        else:
            return min(self.v.items(), key=operator.itemgetter(1))[0][1]



