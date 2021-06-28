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
        # This struct is useless because the state s doesnt change
        # s1 = s2 = ... = sn = s so there is no need
        '''
            v(s,a) : { (s1,a1): v(s1,a1) , (s2,a2): v(s2,a2) , (s3,a3): v(s3,a3) .... }
        '''

        # This structure is more optimized because states
        # are not so important as their evaluation is

        '''
            We will use this representation for the function v : 
            v(s,a) : { a1 : v(s,a1) , a2 : v(s,a2) , ... }
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

        if node.is_terminal or depth == 0:
            return node.state.value()
        '''
        if node in self.T :
            return self.T[node]
        '''

        print(f' Node : \n {node}')
        print(f' T: {self.T}')

        if repr(node) not in self.T:
            self.T.append(node)
            self.v = {}

            for i,a in enumerate(node.state.actions()):
                #print(f'Before : ')
                #print(node.state)
                child = node.do_action(a)
                print(f' Child #{i+1} : {child} ')
                node.children.append(child)
                self.v[a] = child.state.value()
                node.undo_action()
                #print(f'After : {self.v} ')
                #print(node.make_action(a).state)


        else:
            print(f' ----------------------------------')
            #print(f'Before , {node.state.first_player()} :  {node}')
            print(f' Heree #1 : {node}')
            a_b = self.best_action(node)
            print(f' Heree #2 : {node}')
            #new_node = Node(node.state.make_action(a_b), node)
            node = node.do_action(a_b)
            #print(f'After {a_b} , {node.state.first_player()} : {node}')
            self.v[a_b] = self.ub_minimax_iter(depth-1,node)

        a_b = self.best_action(node)
        return self.v[a_b]

    # Get the best available action from current state #state for the current player (white,black)
    def best_action(self, node):
        if node.state.first_player():
            print(f' MAX : {self.v}')
            a = max(self.v, key=self.v.get)
            node = node.do_action(a)
            print(f' BEST MAX  , {a} : {self.v[a]}')
            return a
        else:
            print(f' MIN : {self.v}')
            a = min(self.v, key=self.v.get)
            node = node.do_action(a)
            print(f' BEST MIN , {a} :  {self.v[a]}')
            return a


