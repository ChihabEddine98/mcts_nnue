





# In this Class we have an implmenatation for the Alpha-Beta Alogrithm
# Using the Negamax Framework to avoid writing the same code for max and
# min cases separatly

class AlphaBeta(object):

    def __init__(self,root,eval_policy,depth=2):
        self.depth = depth
        self.root = root
        self.eval_policy = eval_policy

    def search(self,state):
        return self.minimax_alpha_beta(state,self.depth)

    def minimax_alpha_beta(self,state,depth):

        state_cpy = state
        actions = state_cpy.actions()
        best_action = None
        h_score , l_score = float('inf') , float('-inf')

        for action in actions :

            if state_cpy.first_player():
                best_score = self.max_value(state_cpy,depth,h_score,l_score)
            else:
                best_score = self.min_value(state_cpy,depth,h_score,l_score)

            if state_cpy.first_player() and best_score > h_score:
                h_score = best_score
                best_action = action
            elif not(state_cpy.first_player()) and best_score < l_score:
                l_score = best_score
                best_action = action

        print(f' Turn : {state_cpy.first_player()} , Action : {best_action}')
        return  best_action

    def max_value(self,state,depth,alpha,beta):

        if state.is_terminal() or depth == 0:
            return self.eval_policy(state)

        state_cpy = state
        actions = state_cpy.actions()
        best_score = float('-inf')

        for action in actions:
            state_cpy.do_action(action)
            res_score = self.min_value(state_cpy,depth-1,alpha,beta)
            best_score = max(best_score,res_score)

            if best_score >= beta :
                return best_score
            alpha = max(alpha,best_score)

        return best_score

    def min_value(self,state,depth,alpha,beta):

        if state.is_terminal() or depth == 0:
            return self.eval_policy(state)

        state_cpy = state
        actions = state_cpy.actions()
        best_score = float('inf')

        for action in actions:
            state_cpy.do_action(action)
            res_score = self.max_value(state_cpy,depth-1,alpha,beta)
            best_score = min(best_score,res_score)

            if best_score <= alpha :
                return best_score
            beta = min(beta,best_score)

        return best_score










'''
    def search(self,depth,state,alpha,beta):
        if state.is_terminal() or depth == 0 :
            return state.value()

        print(f' Node : {state}')
        print(f' Actions : {state.actions()}')
        for action in state.actions():
            print(f' Before : {state}')
            state = state.do_action(action)
            print(f' After {action} : {state}')
            score = -self.search(depth-1,state,-beta,-alpha)
            if score >= beta :
                return beta
            if score > alpha :
                alpha = score

        return alpha
'''