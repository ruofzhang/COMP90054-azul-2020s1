from players.mctsnodes import mctsNode


class monte_carlo_tree_search:
    def __init__(self, node: mctsNode):
        self.root = node

    def best_move(self, simulations_number):
        for _ in range(0, simulations_number):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        best_move = self.root.best_child().last_action
        return best_move

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node