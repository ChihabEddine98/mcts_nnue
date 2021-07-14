





# In this Class we have an implmenatation for the Alpha-Beta Alogrithm
# Using the Negamax Framework to avoid writing the same code for max and
# min cases separatly

class AlphaBeta(object):

    def __init__(self,root,eval_policy,depth=2):
        self.depth = depth
        self.root = root
        self.eval_policy = eval_policy
        self.v, self.v_max , self.v_min = {},{},{}

    def search(self,state):
        return self.best_action(state,self.depth)

    def best_action(self,state,depth):
        actions = state.actions()
        best_score = float('-inf')
        best_action = None

        for a in actions:
            state = state.do_action(a)
            value = max(best_score,self.negamax(state,depth-1,-1e4,1e4))
            state = state.undo_action()
            if value > best_score :
                best_action = a
                best_score = value

        return best_action



    def negamax(self,state,depth,alpha,beta):
        if depth == 0  or state.is_terminal():
            return -self.eval_policy(state)

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
        if depth == 0 :
            return -self.eval_policy(state)

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
            score = -self.minimax_a_b(state, -beta, -alpha)
            self.v[action] = score
            state.undo_action()

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        return alpha

