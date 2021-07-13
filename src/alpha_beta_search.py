





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
            value = max(best_score,self.minimax(state,depth-1,-1e4,1e4))
            state = state.undo_action()
            if value > best_score :
                best_action = a
                best_score = value

        return best_action




    def minimax(self,state,depth,alpha,beta):
        if depth == 0 :
            return -self.eval_policy(state)

        actions = state.actions()
        if state.first_player():
            best_score = float('-inf')
            for a in actions:
                state = state.do_action(a)
                best_score = max(best_score,self.minimax(state,depth-1,alpha,beta))
                state = state.undo_action()
                alpha = max(alpha,best_score)
                if beta <= alpha :
                    return best_score
            return best_score

        else:
            best_score = float('inf')
            for a in actions:
                state = state.do_action(a)
                best_score = min(best_score, self.minimax(state, depth - 1, alpha, beta))
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

    def minimax_alpha_beta(self,state,depth):
        h_score , l_score = float('inf') , float('-inf')


        if state.first_player():
            best_score = self.max_value(state, depth, h_score, l_score)
            best_action = self.best_action(state)
            print(f' V_max : {self.v_max}')


        else:
            best_score = self.min_value(state, depth, h_score, l_score)
            best_action = self.best_action(state)
            print(f' V_min : {self.v_min}')

        return best_action

    # To be changed !
    def minimax_alpha_beta2(self,state,depth):

        state_cpy = state
        actions = state_cpy.actions()
        best_action = None
        h_score , l_score = float('inf') , float('-inf')

        for action in actions :

            if state_cpy.first_player():
                best_score = self.max_value(state_cpy,depth,h_score,l_score)
            else:
                print(f'#1 {state_cpy}')
                best_score = self.min_value(state_cpy,depth,h_score,l_score)
                print(f'#2 {action} :  {best_score} ,  {state_cpy} ')

            if state_cpy.first_player() or best_score >= h_score:
                print('Yoooooo High ')
                h_score = best_score
                best_action = action
            else:
                print('Yoooooo')
                l_score = best_score
                best_action = action



        print(f' Turn : {state_cpy.first_player()} , Action : {best_action}')
        return  best_action


    def best_action(self,state):
        print(f'MAX  : {self.v_max} \nMIN :  {self.v_min}')
        if state.first_player():
            return max(self.v_max, key=self.v_max.get)
        else:
            return min(self.v_min, key=self.v_min.get)

    # Use Negamax for alpha beta
    def max_value(self,state,depth,alpha,beta):

        if state.is_terminal() or depth == 0:
            return self.eval_policy(state)

        state_cpy = state
        actions = state_cpy.actions()
        best_score = float('-inf')

        for action in actions:
            print(f' MAX AVANT : {state_cpy} ')
            state_cpy.do_action(action)
            print(f' MAX : {state_cpy} ')
            res_score = self.min_value(state_cpy,depth-1,alpha,beta)
            best_score = max(best_score,res_score)
            self.v_max[action] = best_score

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
            print(f' MIN AVANT : {state_cpy} ')
            state_cpy.do_action(action)
            print(f' MIN : {state_cpy} ')
            res_score = self.max_value(state_cpy,depth-1,alpha,beta)
            best_score = min(best_score,res_score)
            self.v_min[action] = best_score

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