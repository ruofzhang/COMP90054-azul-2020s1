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
        self.untried_actions = self.sort_moves()
        self.visits = 0
        self.wins = 0



    def expand(self):
        # action = self.move_selection(self.untried_actions)
        # self.untried_actions.remove(action)
        action = self.untried_actions[0]
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
        count = 0
        rollout_state = copy.deepcopy(self.state)
        this_plr = rollout_state.players[self.next_to_move]
        opponent_plr = rollout_state.players[1 - self.next_to_move]

        while rollout_state.TilesRemaining() and count < 3:
            plr_state = rollout_state.players[next]
            possible_moves = sorted(plr_state.GetAvailableMoves(rollout_state), key= lambda x: (x[2].num_to_floor_line, -x[2].num_to_pattern_line))
            action = possible_moves[0]
            rollout_state.ExecuteMove(next, action)
            count += 1
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

    def sort_moves(self):
        available_moves = self.state.players[self.next_to_move].GetAvailableMoves(self.state)
        sorted_moves = sorted(available_moves, key= lambda x: (x[2].num_to_floor_line, -x[2].num_to_pattern_line))
        num_moves = len(sorted_moves)
        sorted_moves = sorted_moves[0: math.ceil(num_moves / 10)]
        return sorted_moves

    def shrink_untried_moves(self,size=1):

        available_moves = self.state.players[self.next_to_move].GetAvailableMoves(self.state)
        num_moves = len(available_moves)
        new_num_moves = math.ceil(num_moves / size)
        new_moves = random.sample(available_moves, new_num_moves)

        return new_moves

    def move_selection(self, moves):

        selected_move = None
        plr_lines_number = self.state.players[self.next_to_move].lines_number
        num_to_floor = 7

        for mid, fid, tgrab in moves:
            if tgrab.num_to_pattern_line == 0:
                continue
            if (tgrab.num_to_pattern_line == 1 and tgrab.pattern_line_dest == 3 and tgrab.num_to_floor_line ==0)\
                or (tgrab.num_to_pattern_line == 1  and tgrab.pattern_line_dest == 4 and tgrab.num_to_floor_line ==0):
                continue
            if tgrab.num_to_pattern_line == 5:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line == 4:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line == 3 and tgrab.num_to_floor_line == (0 or 1):
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line == 2 and tgrab.num_to_floor_line == (0 or 1):
                selected_move = (mid, fid, tgrab)
                break
            if (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 2 and  tgrab.pattern_line_dest == 1 and tgrab.num_to_floor_line == 0)\
                or (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and  tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 3 and  tgrab.pattern_line_dest == 2 and tgrab.num_to_floor_line == 0)\
                or (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and  tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 4 and  tgrab.pattern_line_dest == 3 and tgrab.num_to_floor_line == 0)\
                or (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and  tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 5 and  tgrab.pattern_line_dest == 4 and tgrab.num_to_floor_line == 0):
                selected_move = (mid, fid, tgrab)
                break
            if (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 2 and  tgrab.pattern_line_dest == 1 and tgrab.num_to_floor_line == 1)\
                or (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 3 and  tgrab.pattern_line_dest == 2 and tgrab.num_to_floor_line == 1)\
                or (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 4 and  tgrab.pattern_line_dest == 3 and tgrab.num_to_floor_line == 1)\
                or (tgrab.num_to_pattern_line > 0 and plr_lines_number[tgrab.pattern_line_dest] > 0 and tgrab.num_to_pattern_line + plr_lines_number[tgrab.pattern_line_dest] == 5 and  tgrab.pattern_line_dest == 4 and tgrab.num_to_floor_line == 1):
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_pattern_line > 0 and tgrab.num_to_floor_line <= 2:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_floor_line == 1:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_floor_line == 2:
                selected_move = (mid, fid, tgrab)
                break
            if tgrab.num_to_floor_line == 3:
                selected_move = (mid, fid, tgrab)
                break

        if selected_move == None:
            selected_move = random.choice(moves)

        return selected_move
