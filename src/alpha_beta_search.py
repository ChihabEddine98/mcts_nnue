from time import time





# In this Class we have an implmenatation for the Alpha-Beta Alogrithm
# Using the Negamax Framework to avoid writing the same code for max and
# min cases separately

class AlphaBeta(object):

    def __init__(self,root,eval_policy,depth=2):
        self.max_depth = depth
        self.node_expanded = 0
        self.root = root
        self.eval_policy = eval_policy
        self.v, self.v_max , self.v_min = {},{},{}

    def search(self,state):
        return self.choose_action(state)

    def best_action(self,state,depth):
        actions = state.actions()
        best_score = float('-inf')
        best_action = None

        for a in actions:
            state = state.do_action(a)
            score = max(best_score,self.minimax_alpha_beta(state,depth-1,-1e4,1e4))
            state = state.undo_action()
            if score > best_score :
                best_action = a
                best_score = score

        return best_action

    def choose_action(self, state):
        self.node_expanded = 0

        start_time = time()

        print("MINIMAX AB : Wait AI is choosing")
        list_action = state.actions()
        eval_score, selected_key_action = self._minimax(0, state, True, float('-inf'), float('inf'))
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
        print("--- %s seconds ---" % (time() - start_time))
        print("--- %s Best :  ---" % (selected_key_action))

        return selected_key_action

    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):

        if current_depth == self.max_depth or state.is_terminal():
            return self.eval_policy(state), ""

        self.node_expanded += 1

        key_of_actions = state.actions()

        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            new_state = state.do_action(action_key)
            eval_child, action_child = self._minimax(current_depth + 1, new_state, not is_max_turn, alpha, beta)
            state.undo_action()
            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action_key
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action_key
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, action_target

    def negamax(self,state,depth,alpha,beta):
        if depth == 0  or state.is_terminal():
            return self.eval_policy(state) if state.first_player() else -self.eval_policy(state)

        actions = state.actions()
        best_score = float('-inf')

        for a in actions:
            state = state.do_action(a)
            score = -self.negamax(state,depth-1,-beta,-alpha)
            state = state.undo_action()
            if score > best_score :
                best_score = score
            if best_score > alpha :
                alpha = best_score
            if best_score >= beta :
                break

        return alpha

    def minimax_alpha_beta(self,state,depth,alpha,beta):
        if depth == 0 or state.is_terminal():
            return self.eval_policy(state) if state.first_player() else -self.eval_policy(state)

        actions = state.actions()
        if state.first_player():
            best_score = float('-inf')
            for a in actions:
                state = state.do_action(a)
                best_score = max(best_score,self.minimax_alpha_beta(state,depth-1,alpha,beta))
                state = state.undo_action()
                alpha = max(alpha,best_score)
                if beta <= alpha :
                    return best_score
            return best_score

        else:
            best_score = float('inf')
            for a in actions:
                state = state.do_action(a)
                best_score = min(best_score, self.minimax_alpha_beta(state, depth - 1, alpha, beta))
                state = state.undo_action()
                beta = min(beta, best_score)
                if beta <= alpha:
                    return best_score
            return best_score




    def quiescence(self,state,alpha,beta):
        stand_pat = self.eval_policy(state)

        if stand_pat >= beta:
            return beta

        if alpha < stand_pat:
            alpha = stand_pat

        for action in state.actions():
            state.do_action(action)
            score = -self.negamax(state, -beta, -alpha)
            self.v[action] = score
            state.undo_action()

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        return alpha

