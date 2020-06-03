# This file will be used in the competition
# Please make sure the following functions are well defined

from advance_model import *
from heapq import heappop, heappush, heapify
from utils import *

# if you want to use random, you have to import it here
import random

# if you want to import other py file in the same directory as your myPlayer.py
# import sys

class myPlayer(AdvancePlayer):
    #check
    # initialize
    # You can add your own data initilazation here, just make sure nothing breaks
    def __init__(self,_id):
        super().__init__(_id)
        self.previousMoves = None

    # Each player is given 5 seconds when a new round started
    # If exceeds 5 seconds, all your code will be terminated and 
    # you will receive a timeout warning
    # bfs don't need the first round
   # def StartRound(self, game_state):
    #    return None

    # Each player is given 1 second to select next best move
    # If exceeds 5 seconds, all your code will be terminated, 
    # a random action will be selected, and you will receive 
    # a timeout warning
    # check
    def SelectMove(self, moves, game_state):
        curPlayerState = game_state.players[self.id]
        bestmove = None
        bestStateScore = -1
        moveStatePairs = self.BFS(game_state)
        for state in moveStatePairs:
            if self.evaluateGameState(state) > bestStateScore:
                bestStateScore = self.evaluateGameState(state)
                bestmove = moveStatePairs[state]
        if bestmove == None:
            bestmove = self.SelectMove_naive(moves, game_state)
        return bestmove


    def SelectMove_naive(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.
        most_to_line = -1
        corr_to_floor = 0

        best_move = None

        for mid,fid,tgrab in moves:
            if most_to_line == -1:
                best_move = (mid,fid,tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
                continue

            if tgrab.num_to_pattern_line > most_to_line:
                best_move = (mid,fid,tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
            elif tgrab.num_to_pattern_line == most_to_line and \
                tgrab.num_to_pattern_line < corr_to_floor:
                best_move = (mid,fid,tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line

        return best_move

    #check
    def BFS(self, game_state):
        startTime = time.time()
        moveStatePairs = {}
        gameStateQueue = Queue()
        gameStateQueue.push((None, game_state))
        justOneLayer = True
        while not gameStateQueue.isEmpty():

            #add the break time
            if time.time() - startTime > 0.95:
                break
            prevMove, curGameState = gameStateQueue.pop()
            possibleMoves = self.nextMoves(curGameState)
            if len(possibleMoves) == 0:
                return moveStatePairs
            for move in possibleMoves:
                newGameState = self.stateAfterMove(move, curGameState)
                if justOneLayer == True:
                    gameStateQueue.push((move, newGameState))
                    moveStatePairs[newGameState] = move
                else:
                    gameStateQueue.push((prevMove, newGameState))
                    moveStatePairs[newGameState] = prevMove
            justOneLayer = False

        return moveStatePairs
    """
        def Astar(self, gameState, bestScore):
        startTime = time.time()
        visitedPlayerState, moveStatePairs, costs, start_cost = [], {}, {}, 0

        costs[gameState.players[self.id]] = 0
        visitedPlayerState.append(gameState.players[self.id])
        priorityQueue = PriorityQueue()
        priorityQueue.push((None, gameState), 0)
        i = 0
        while (not priorityQueue.isEmpty()):
            prevMove, curGameState = priorityQueue.pop()
            curPlayerState = curGameState.players[self.id]
            if time.time() - startTime > 0.9:
                return moveStatePairs

            if not curGameState.TilesRemaining():
                return moveStatePairs

            moves = self.nextMoves(curGameState)
            for move in moves:
                newGameState = self.stateAfterMove(move, curGameState)
                newPlayerState = newGameState.players[self.id]
                newCost = 1
                next_cost = costs[curPlayerState] + newCost

                if newPlayerState not in visitedPlayerState or next_cost < costs[newPlayerState]:
                    visitedPlayerState.append(newPlayerState)
                    if i < 1:
                        moveStatePairs[newGameState] = move
                    else:
                        moveStatePairs[newGameState] = prevMove
                    costs[newPlayerState] = next_cost
                    heurisitic = bestScore - self.evaluateGameState(newGameState)
                    priority = next_cost + heurisitic
                    if i < 1:
                        priorityQueue.push((move, newGameState), priority)
                    else:
                        priorityQueue.push((prevMove, newGameState), priority)
            i += 1

        return moveStatePairs

    def maxScoreForRound(self, game_state):
        startTime = time.time()
        tilesTotal = [0, 0, 0, 0, 0]
        patternLineNum = game_state.players[self.id].line_number
        patternLineType = game_state.players[self.id].line_tile

        possibleMaxScoreStates = []
        bestStateScore = -10000

        for factory in game_state.factories:
            for i in range(0,5):
                tilesTotal[i] += factory.tiles[i]

        for i in range(0,5):
            if patternLineType[i] == -1:
                for tile in Tile:
                    if tilesTotal[tile] >= i+1:
                        possibleState = copy.deepcopy(game_state)
                        possibleState.players[self.id].lines_number[i] = i+1
                        possibleState.players[self.id].line_tile[i] = tile
                        possibleMaxScoreStates.append(possibleState)
            elif tilesTotal[patternLineType[i]] >= (i+1)-patternLineNum[i]:
                possibleState = copy.deepcopy(game_state)
                possibleState.players[self.id].line_number[i] = i+1
                possibleMaxScoreStates.append(possibleState)
        for states in possibleMaxScoreStates:
            if time.time() - startTime > 3.5:
                break
            if self.evaluateGameState(states) > bestStateScore:
                bestStateScore = self.evaluateGameState(states)

        return bestStateScore
    """

    # check
    def nextMoves(self, game_state):
        lineIndexPairTileType = []
        patternLineColor = game_state.players[self.id].lines_tile
        for i in range(0, 4):
            if patternLineColor[i] != -1:
                lineIndexPairTileType.append((i, patternLineColor[i]))

        targetWallColumns = []
        for lineIndex, tile_type in lineIndexPairTileType:
            targetWallColumns.append((lineIndex + tile_type) % 5)

        targetWallRows = []
        playerWall = game_state.players[self.id].grid_state
        for row in range(0, 4):
            for col in range(0, 4):
                if playerWall[row][col] == 1:
                    targetWallRows.append(row)
                    break

        possibleMoves = []
        for moveType, factory, tileGrab in game_state.players[self.id].GetAvailableMoves(game_state):
            if patternLineColor[tileGrab.pattern_line_dest] != -1:
                possibleMoves.append((moveType, factory, tileGrab))
            else:
                if (tileGrab.pattern_line_dest + tileGrab.tile_type) % 5 in targetWallColumns:
                    possibleMoves.append((moveType, factory, tileGrab))
                if tileGrab.pattern_line_dest in targetWallRows:
                    possibleMoves.append((moveType, factory, tileGrab))

        return possibleMoves

    #check
    def stateAfterMove(self, move, curState):
        newState = copy.deepcopy(curState)
        if move[0] == Move.TAKE_FROM_CENTRE:
            if not newState.first_player_taken:
                newState.players[self.id].GiveFirstPlayerToken()
                newState.first_player_taken = True
                newState.next_first_player = self.id

            if move[2].num_to_floor_line > 0:
                ttf = []
                for i in range(move[2].num_to_floor_line):
                    ttf.append(move[2].tile_type)
                newState.players[self.id].AddToFloor(ttf)
                newState.bag_used.extend(ttf)

            if move[2].num_to_pattern_line > 0:
                newState.players[self.id].AddToPatternLine(move[2].pattern_line_dest, move[2].num_to_pattern_line, move[2].tile_type)

            newState.centre_pool.RemoveTiles(move[2].number, move[2].tile_type)

        elif move[0] == Move.TAKE_FROM_FACTORY:
            if move[2].num_to_floor_line > 0:
                temp = []
                for i in range(move[2].num_to_floor_line):
                    temp.append(move[2].tile_type)
                newState.players[self.id].AddToFloor(temp)
                newState.bag_used.extend(temp)

            if move[2].num_to_pattern_line > 0:
                newState.players[self.id].AddToPatternLine(move[2].pattern_line_dest, move[2].num_to_pattern_line, move[2].tile_type)

            fac = newState.factories[move[1]]
            fac.RemoveTiles(move[2].number, move[2].tile_type)

            for tile in Tile:
                num_on_fd = fac.tiles[tile]
                if num_on_fd > 0:
                    newState.centre_pool.AddTiles(num_on_fd, tile)
                    fac.RemoveTiles(num_on_fd,tile)
        return newState

    def evaluateGameState(self, game_state):
        score = 0
        patternLineNum = game_state.players[self.id].lines_number
        for i in range(0, 4):
            if patternLineNum[i] == i + 1:
                score += 1
        floor = game_state.players[self.id].floor
        floorScore = [-1, -1, -2, -2, -2, -3, -3]
        for i,j in zip(floor, floorScore):
            score += i*j
        return score
"""
# impelement the Priority Queue for A*
# this class should have push, pop, and isEmpty
class PriorityQueue:
    def __init__(self):
        self.num = 0
        self.heap = []

    # pop the last item from Queue
    def pop(self):
        _, _, item = heappop(self.heap)
        self.num = self.num - 1
        return item

    # push one item
    def push(self, item, priority):
        heappush(self.heap, (priority, self.num, item))
        self.num = self.num + 1

    # return boolean whether the list is empty
    def isEmpty(self):
        return self.num == 0
"""

    # impelement the Queue for BFS
    # this class should have push, pop, and isEmpty
class Queue:
    def __init__(self):
        self.list = []

    # push one item
    def push(self, item):
        self.list.append(item)

    # pop the last item from Queue
    def pop(self):
        return self.list.pop()

    # return boolean whether the list is empty
    def isEmpty(self):
        return len(self.list) == 0