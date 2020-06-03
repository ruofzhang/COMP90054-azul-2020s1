from advance_model import *
from players.mcts import monte_carlo_tree_search
from players.mctsnodes import mctsNode


class myPlayer(AdvancePlayer):
    def __init__(self,_id):
        super().__init__(_id)
    
    def SelectMove(self,moves,game_state):
        root = mctsNode(self.id, game_state, last_action=None, parent=None)
        mcts = monte_carlo_tree_search(root)
        best_move = mcts.best_move(300)
        return best_move





