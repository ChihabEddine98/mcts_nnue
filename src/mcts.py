import numpy as np
from time import time
import random





def nnue_policy(state):
    return state.value()



class Node(object):
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent
        self.children = {}
        self.is_terminal = state.is_terminal()
        self.is_fully_expanded = self.is_terminal
        self.num_visits = 0
        self.total_reward = 0


    def __repr__(self):
        return self.state.board.fen()

    def __str__(self):
        return self.state.__str__()

    def make_action(self,action):
        return Node(self.state.make_action(action),self)

class MCTS():
    def __init__(self,root, time_limit=None, iteration_limit=None, exploration_constant= 1 / np.sqrt(2),
                 rollout_policy=nnue_policy):
        if time_limit != None:
            if iteration_limit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.time_limit = time_limit
            self.limit_type = 'time'
        else:
            if iteration_limit is None:
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
                self.executeRound()
        else:
            for i in range(self.search_limit):
                self.executeRound()

        best_child = self.getBestChild(self.root, 0)
        return self.getAction(self.root, best_child), -nnue_policy(best_child.state)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.getBestChild(node, self.exploration_constant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.actions()
        for action in actions:
            if action not in node.children:
                new_node = Node(node.state.make_action(action), node)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                return new_node

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        turn = 1
        while node is not None:
            node.num_visits += 1
            node.total_reward += reward * turn
            node = node.parent
            turn *= -1

    def getBestChild(self, node, exploration_value):
        best_value = float("-inf")
        best_nodes = []
        for child in node.children.values():
            node_value = child.total_reward / child.num_visits + exploration_value * np.sqrt(
                2 * np.log(node.num_visits) / child.num_visits)

            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def getAction(self, root, best_child):
        for action, node in root.children.items():
            if node is best_child:
                return action