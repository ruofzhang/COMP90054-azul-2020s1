import copy
import random
import math
import numpy as np


class mctsNode(object):
    def __init__(self, next_to_move, game_state, last_action=None, parent=None):
        self.next_to_move = next_to_move
        self.state = game_state
        self.last_action = last_action
        self.parent = parent
        self.children = []
        self.untried_actions = self.shrink_untried_moves(2)
        self.visits = 0
        self.wins = 0



    def expand(self):
        action = self.move_selection(self.untried_actions)
        self.untried_actions.remove(action)
        copy_state = copy.deepcopy(self.state)
        copy_state.ExecuteMove(self.next_to_move, action)
        child_node = mctsNode(1 - self.next_to_move, copy_state, last_action=action, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        game_over = False
        if not self.state.TilesRemaining():
            game_over = True
        return game_over

    def rollout(self):
        next = self.next_to_move
        rollout_state = copy.deepcopy(self.state)
        this_plr = rollout_state.players[self.next_to_move]
        opponent_plr = rollout_state.players[1 - self.next_to_move]

        while rollout_state.TilesRemaining():
            plr_state = rollout_state.players[next]
            possible_moves = plr_state.GetAvailableMoves(rollout_state)
            action = self.move_selection(possible_moves)
            rollout_state.ExecuteMove(next, action)
            next = 1 - next

        rollout_state.ExecuteEndOfRound()
        this_score = this_plr.score
        opponent_score = opponent_plr.score
        if this_score >= opponent_score:
            result = 1
        else:
            result = 0
        return result

    def backpropagate(self, result):
        self.visits += 1
        if result == 1:
            self.wins -= 1
        else:
            self.wins += 1
        if self.parent != None:
            self.parent.backpropagate(1 - result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param = 0):
        choices_weights = [
            (c.wins / c.visits) + c_param * np.sqrt((2 * np.log(self.visits) / (c.visits)))
            for c in self.children
        ]
        best_child = self.children[np.argmax(choices_weights)]
        return best_child

    def rollout_policy(self, possible_moves):
        return random.choice(possible_moves)

    def shrink_untried_moves(self,size=1):

        available_moves = self.state.players[self.next_to_move].GetAvailableMoves(self.state)
        num_moves = len(available_moves)
        new_num_moves = math.ceil(num_moves / size)
        new_moves = random.sample(available_moves, new_num_moves)

        return new_moves

    def move_selection(self, moves):

        selected_move = None
        plr_lines_number = self.state.players[self.next_to_move].lines_number
        plr_lines_tile = self.state.players[self.next_to_move].lines_tile
        num_to_floor = 7

        for mid, fid, tgrab in moves:
            if tgrab.num_to_pattern_line == 1 and tgrab.pattern_line_dest == 0\
                    or tgrab.num_to_pattern_line == 2 and tgrab.pattern_line_dest == 1\
                    or tgrab.num_to_pattern_line == 3 and tgrab.pattern_line_dest == 2\
                    or tgrab.num_to_pattern_line == 4 and tgrab.pattern_line_dest == 3\
                    or tgrab.num_to_pattern_line == 5 and tgrab.pattern_line_dest == 4:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line == 1 and tgrab.pattern_line_dest == 1\
                    or tgrab.num_to_pattern_line == 2 and tgrab.pattern_line_dest == 2\
                    or tgrab.num_to_pattern_line == 3 and tgrab.pattern_line_dest == 3\
                    or tgrab.num_to_pattern_line == 4 and tgrab.pattern_line_dest == 4:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line == 1 and tgrab.pattern_line_dest == 2\
                    or tgrab.num_to_pattern_line == 2 and tgrab.pattern_line_dest == 3\
                    or tgrab.num_to_pattern_line == 3 and tgrab.pattern_line_dest == 4:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 2 and  tgrab.pattern_line_dest == 1 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest] and tgrab.num_to_floor_line == 0\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 3 and  tgrab.pattern_line_dest == 2 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest] and tgrab.num_to_floor_line == 0\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 4 and  tgrab.pattern_line_dest == 3 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest] and tgrab.num_to_floor_line == 0\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 5 and  tgrab.pattern_line_dest == 4 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest] and tgrab.num_to_floor_line == 0:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 2 and  tgrab.pattern_line_dest == 1 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest] and tgrab.num_to_floor_line == 1\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 3 and  tgrab.pattern_line_dest == 2 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest] and tgrab.num_to_floor_line == 1\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 4 and  tgrab.pattern_line_dest == 3 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest] and tgrab.num_to_floor_line == 1\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 5 and  tgrab.pattern_line_dest == 4 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest]:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 2 and  tgrab.pattern_line_dest == 1 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest]\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 3 and  tgrab.pattern_line_dest == 2 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest]\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 4 and  tgrab.pattern_line_dest == 3 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest]\
                or tgrab.num_to_pattern_line > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 5 and  tgrab.pattern_line_dest == 4 and tgrab.tile_type == plr_lines_tile[tgrab.pattern_line_dest]:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line == -1:
                if tgrab.num_to_floor_line < num_to_floor:
                    selected_move = (mid, fid, tgrab)
                    num_to_floor = tgrab.num_to_floor_line
                    continue

        if selected_move == None:
            selected_move = random.choice(moves)

        return selected_move
