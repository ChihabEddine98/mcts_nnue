from time import time
import operator
from copy import deepcopy


class Node(object):
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
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
    def __init__(self,root,eval_policy):
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

        self.eval_policy = eval_policy


    # Execute the UBFMS search from root node
    def search(self,state,tho=1):
       node = Node(state=state,parent=None)
       return self.ub_minimax(node,tho)
    # unbounded minimax search starting from state #state
    def ub_minimax(self,node,tho):
        t = time()

        while (time()- t < tho)  :
            value = self.ub_minimax_iter(node)
            if value == 1e6 :
                return None
            #print(f'({value})')



        '''
        a_b = self.best_action(node)
        node = node.do_action(a_b)
        '''
        return self.best_action(node)

    # unbounded minimax search iteration on state #state
    def ub_minimax_iter(self, node):

        if node.state.is_terminal():
            return self.eval_policy(node.state) if node.state.first_player() else -self.eval_policy(node.state)

        self.v = {}

        if repr(node) not in self.T:
            self.T.append(node)

            for i,a in enumerate(node.state.actions()):
                #print(f'Before : ')
                #print(node.state)
                fen = repr(node)

                child = node.do_action(a)
                #print(f' Child #{i+1} : {child} ')
                node.children.append(child)
                self.v[(fen,a)] = self.eval_policy(node.state) if child.state.first_player() else -self.eval_policy(child.state)
                node = node.undo_action()

                #print(f'After : {self.v} ')
                #print(node.make_action(a).state)


        else:
            print(f' ----------------------------------')
            #print(f'Before , {node.state.first_player()} :  {node}')
            #print(f' Heree #1 : {node}')
            a_b = self.best_action(node)
            #print(f' Heree #2 : {node}')
            #new_node = Node(node.state.make_action(a_b), node)
            bkp_node = node
            node = node.do_action(a_b)
            #print(f'After {a_b} , {node.state.first_player()} : {node}')
            self.v[(repr(bkp_node),a_b)] = self.ub_minimax_iter(node)
            node = node.undo_action()

        a_b = self.best_action(node)
        return self.v[(repr(node),a_b)]

    def get_action_value_by_fen(self,fen):
        result = {}
        for (state,action),value in self.v.items():
            if state == fen :
                result[action] = value
        return result


    # TODO SOS ----- wrong push action for BLACK (f1d3)
    #        Verify self.v dict if there is doubles
    #        it can be the issue
    #       Delete the old version of self.v ( values function )
    # Get the best available action from current state #state for the current player (white,black)
    def best_action(self, node):
        result = self.get_action_value_by_fen(repr(node))
        if node.state.first_player():
            return max(result, key=result.get)
        else:
            return min(result, key=result.get)


