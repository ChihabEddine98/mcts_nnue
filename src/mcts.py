import numpy as np
from time import time
import random





def nnue_policy(state):
    return state.value()

def custom_policy(state):
    return state.value_nn()

class Node(object):
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
        self.children = {}
        self.is_terminal = state.is_terminal()
        self.is_fully_expanded = self.is_terminal
        self.num_visits = 0
        self.total_reward = 0

    def uct(self,parent,explore_val):
        return self.total_reward / self.num_visits + explore_val * np.sqrt(
                2 * np.log(parent.num_visits) / self.num_visits)



    def __repr__(self):
        return self.state.board.fen()

    def __str__(self):
        return self.state.__str__()

    def make_action(self,action):
        return Node(self.state.do_action(action), self)

class MCTS(object):
    def __init__(self,root, time_limit=0, iteration_limit=0, exploration_constant= 1 / np.sqrt(2),
                 rollout_policy=nnue_policy):
        if time_limit :
            if iteration_limit:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.time_limit = time_limit
            self.limit_type = 'time'
        else:
            if not iteration_limit:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iteration_limit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.search_limit = iteration_limit
            self.limit_type = 'iterations'
        self.exploration_constant = exploration_constant
        self.rollout = rollout_policy
        self.root = Node(root, None)


    def search(self):

        if self.limit_type == 'time':
            time_limit = time() + self.time_limit / 1000
            while time() < time_limit:
                self.mcts_iter()
        else:
            for i in range(self.search_limit):
                self.mcts_iter()

        best_child = self.best_action(self.root, 0)
        return self.get_action(self.root, best_child), -nnue_policy(best_child.state)

    def mcts_iter(self):
        node = self.select(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.best_action(node, self.exploration_constant)
            else:
                return self.expand(node)
        return node

    def best_action(self, node, explore_val):
        r = random.Random(500)
        best_val = float("-inf")
        best_nodes = []
        for child in node.children.values():
            node_val = child.uct(node,explore_val)

            print(f'({child},{node_val})')

            if node_val >= best_val :
                best_val = node_val
                best_nodes.append(child)

            # TODO----------------------
            # Here need to check if appending items to best nodes is working or need to change
            # it to another approach in comment below
            '''
            if node_val > best_val:
                best_val = node_val
                best_nodes = [child]
            elif node_val == best_val:
                best_nodes.append(child)
            
            [print(n) for n in best_nodes]
            print(best_nodes)
            '''
        return r.choice(best_nodes)

    def expand(self, node):
        actions = node.state.actions()
        for action in actions:
            if action not in node.children:
                # TODO -----------
                # Here need to check if node's making action or go back to state method
                #new_node = Node(node.state.make_action(action), node)
                new_node = node.do_action(action)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                return new_node

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        turn = -1
        while node is not None:
            node.num_visits += 1
            node.total_reward += reward * turn
            node = node.parent
            turn *= -1



    def get_action(self, root, best_child):
        for action, node in root.children.items():
            if node is best_child:
                return action