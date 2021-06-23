from time import time
import operator
from copy import deepcopy


class Node(object):
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
        self.is_terminal = state.is_terminal()
        self.children = []

    def __repr__(self):
        return self.state.board.fen()

    def __str__(self):
        return self.state.__str__()

    def do_action(self, action):
        return Node(self.state.do_action(action), self)

    def undo_action(self):
        return Node(self.state.undo_action(), self)



class UBFMS(object):
    def __init__(self,root):
        self.root = Node(state=root,parent=None)
        # Transposition Table which will have the following struct
        '''
            T : { s1: e1 , s2: e2 , s3: e3 .... }
        '''
        self.T = []
        # it will have this structure
        '''
            v(s,a) : { (s1,a1): v(s1,a1) , (s2,a2): v(s2,a2) , (s3,a3): v(s3,a3) .... }
        '''
        self.v = {}

    # Execute the UBFMS search from root node
    def search(self,tho=1000):
       return self.ub_minimax(2,self.root,tho)
    # unbounded minimax search starting from state #state
    def ub_minimax(self,depth,node,tho):
        t = time()

        while (time()- t < tho) :
            value = self.ub_minimax_iter(depth,node)
            #print(f'({value})')



        a_b = self.best_action(node)
        node = node.do_action(a_b)

        return self.best_action(node),node

    # unbounded minimax search iteration on state #state
    def ub_minimax_iter(self,depth, node):

        print(f' Start : \n {node}')
        if node.is_terminal or depth == 0:
            return node.state.value()
        '''
        if node in self.T :
            return self.T[node]
        '''
        if node not in self.T:
            self.T.append(node)

            for a in node.state.actions():
                #print(f'Before : ')
                #print(node.state)
                child = node.do_action(a)
                node.undo_action()
                node.children.append(child)
                self.v[(repr(node),a)] = child.state.value()
                #print(f'After : {self.v} ')
                #print(node.make_action(a).state)


        else:
            print(f' ----------------------------------')
            #print(f'Before , {node.state.first_player()} :  {node}')
            a_b = self.best_action(node)
            #new_node = Node(node.state.make_action(a_b), node)
            self.v = {}
            node = node.do_action(a_b)
            #print(f'After {a_b} , {node.state.first_player()} : {node}')

            self.v[(repr(node), a_b)] = self.ub_minimax_iter(depth-1,node)

        a_b = self.best_action(node)
        return self.v[(repr(node),a_b)]

    # Get the best available action from current state #state for the current player (white,black)
    def best_action(self, node):
        if node.state.first_player():
            return max(self.v.items(), key=operator.itemgetter(1))[0][1]
        else:
            return min(self.v.items(), key=operator.itemgetter(1))[0][1]



