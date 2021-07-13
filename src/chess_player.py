





class ChessPlayer(object):

    def __init__(self,search_policy):
        self.search = search_policy

    def play(self,state):
        return self.search.search(state)
