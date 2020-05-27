# This file will be used in the competition
# Please make sure the following functions are well defined

from advance_model import *
from utils import *
from copy import *


class myPlayer(AdvancePlayer):

    # initialize
    # The following function should not be changed at all
    def __init__(self, _id):
        super().__init__(_id)

    # Each player is given 5 seconds when a new round started
    # If exceeds 5 seconds, all your code will be terminated and 
    # you will receive a timeout warning
    def StartRound(self, game_state):
        return None

    # Each player is given 1 second to select next best move
    # If exceeds 5 seconds, all your code will be terminated, 
    # a random action will be selected, and you will receive 
    # a timeout warning
    def SelectMove(self, moves, game_state):
        # return random.choice(moves)
        score = -1
        best_move = None
        for mid, fid, tgrab in moves:
            # perform the move in a copy of game_state
            gs_copy = deepcopy(game_state)
            gs_copy.ExecuteMove(self.id, (mid, fid, tgrab))
            ps = gs_copy.players[self.id]
            # only put to floor
            if tgrab.pattern_line_dest == -1:
                pattern_score = 0
            # patter line 1
            elif tgrab.pattern_line_dest == 0:
                pattern_score = 1 - ps.lines_number[0]
                ps.AddToPatternLine(0, pattern_score, tgrab.tile_type)
            # patter line 2
            elif tgrab.pattern_line_dest == 1:
                pattern_score = 2 - ps.lines_number[1]
                ps.AddToPatternLine(1, pattern_score, tgrab.tile_type)
            # patter line 3
            elif tgrab.pattern_line_dest == 2:
                pattern_score = 3 - ps.lines_number[2]
                ps.AddToPatternLine(2, pattern_score, tgrab.tile_type)
            # patter line 4
            elif tgrab.pattern_line_dest == 3:
                pattern_score = 4 - ps.lines_number[3]
                ps.AddToPatternLine(3, pattern_score, tgrab.tile_type)
            # patter line 5
            elif tgrab.pattern_line_dest == 4:
                pattern_score = 5 - ps.lines_number[4]
                ps.AddToPatternLine(4, pattern_score, tgrab.tile_type)

            additional_score = ps.ScoreRound()[0] + ps.EndOfGameScore()
            # heuristic func
            if additional_score - pattern_score > score:
                score = pattern_score + additional_score
                best_move = (mid, fid, tgrab)

        return best_move