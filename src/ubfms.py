from time import time
import operator


class Node(object):
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
        self.is_terminal = state.is_terminal()

    def make_action(self,node,action):
        return Node(node.state.make_action(action), node)


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
    def search(self,tho=2000):
        return self.ub_minimax(self.root,tho)
    # unbounded minimax search starting from state #state
    def ub_minimax(self,node,tho):
        t = time()
        while (time()- t < tho) :
            self.ub_minimax_iter(node)
        return self.best_action(node)

    # unbounded minimax search iteration on state #state
    def ub_minimax_iter(self, node):
        if node.is_terminal:
            return node.state.evaluation()

        if node in self.T :
            return self.T[node]

        if node not in self.T:
            self.T[node] = node.state.evaluation()
            for a in node.state.actions():
                self.v[(node,a)] = node.make_action(node,a).state.evaluation()
        else:
            a_b = self.best_action(node)
            #new_node = Node(node.state.make_action(a_b), node)
            self.v[(node, a_b)] = self.ub_minimax_iter(node.make_action(node,a_b))

        a_b = self.best_action(node)

        print(self.v)
        print(a_b, node.state.first_player())
        vn = self.v[(node,a_b)]

        self.v = {}

        return vn

    # Get the best available action from current state #state for the current player (white,black)
    def best_action(self, node):
        if node.state.first_player():
            return max(self.v.items(), key=operator.itemgetter(1))[0][1]
        else:
            return min(self.v.items(), key=operator.itemgetter(1))[0][1]



