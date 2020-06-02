# This file will be used in the competition
# Please make sure the following functions are well defined

from advance_model import *
from heapq import heappop, heappush, heapify
from utils import *

# if you want to use random, you have to import it here
import random

# if you want to import other py file in the same directory as your myPlayer.py
import sys
sys.path.append("players/my_team_name/")

class myPlayer(AdvancePlayer):
    NUMBER_FACTORIES = [5, 9, 7]

    #check
    # initialize
    # You can add your own data initilazation here, just make sure nothing breaks
    def __init__(self,_id):
        super().__init__(_id)
        self.availableMoveHistory = []
        self.previousMoves = None

        self.blueMoves = [[], [], [], [], []]
        self.yellowMoves = [[], [], [], [], []]
        self.redMoves = [[], [], [], [], []]
        self.blackMoves = [[], [], [], [], []]
        self.whiteMoves = [[], [], [], [], []]

        self.fstlineMoves = [[], [], [], [], []]
        self.sndlineMoves = [[], [], [], [], []]
        self.trdlineMoves = [[], [], [], [], []]
        self.fthlineMoves = [[], [], [], [], []]
        self.fiflineMoves = [[], [], [], [], []]

    # Each player is given 5 seconds when a new round started
    # If exceeds 5 seconds, all your code will be terminated and 
    # you will receive a timeout warning
   # def StartRound(self, game_state):
    #    return None

    # Each player is given 1 second to select next best move
    # If exceeds 5 seconds, all your code will be terminated, 
    # a random action will be selected, and you will receive 
    # a timeout warning
    # check
    def SelectMove(self, moves, game_state):
        starttime = time.time()
        self.categorizeMoves(moves)
        curPlayerState = self.getCurPlayerState(game_state)
        if self.isFirstRound(curPlayerState):
            if self.isRoundJustStart(curPlayerState):
                return self.selectFirstInitialMoves(moves, game_state)
            else:
                bestStateScore = -10000
                moveStatePairs = self.breadthFirstSearch(game_state)
                bestmove = None
                for state in moveStatePairs:
                    # if time.time() - starttime > 0.9:
                    #     break
                    if self.evaluateGameState(state) > bestStateScore:
                        bestStateScore = self.evaluateGameState(state)
                        bestmove = moveStatePairs[state]
                if bestmove == None:
                    bestmove = random.choice(moves)
                return bestmove
        else:
            bestStateScore = -10000
            moveStatePairs = self.breadthFirstSearch(game_state)
            bestmove = None
            for state, move in moveStatePairs.items():
                if self.evaluateGameState(state) > bestStateScore:
                    bestStateScore = self.evaluateGameState(state)
                    bestmove = moveStatePairs[state]
            if bestmove == None:
                bestmove = random.choice(moves)
            return bestmove

        """
        self.categorizeMoves(moves)
        curPlayerState = self.getCurPlayerState(game_state)
        bestScore = 0
        if self.isFirstRound(curPlayerState):
            if self.isRoundJustStart(curPlayerState):
                bestScore = self.maxScoreForRound(game_state)
                return self.selectFirstInitialMoves(moves, game_state)
            else:
                bestStateScore = -10000
                moveStatePairs = self.Astar(game_state, bestScore)
                for state in moveStatePairs:
                    if self.evaluateGameState(state) > bestStateScore:
                        bestStateScore = self.evaluateGameState(state)
                        bestMove = moveStatePairs[state]
                return bestMove

        elif self.isRoundJustStart(curPlayerState):
            bestScore = self.maxScoreForRound(game_state)
            bestStateScore = -10000
            moveStatePairs = self.Astar(game_state, bestScore)
            for state in moveStatePairs:
                if self.evaluateGameState(state) > bestStateScore:
                    bestStateScore = self.evaluateGameState(state)
                    bestMove = moveStatePairs[state]
            return bestMove

        else:
            bestStateScore = -10000
            moveStatePairs = self.Astar(game_state, bestScore)
            for state in moveStatePairs:
                if self.evaluateGameState(state) > bestStateScore:
                    bestStateScore = self.evaluateGameState(state)
                    bestMove = moveStatePairs[state]
            return bestMove
        """

    #check
    def categorizeMoves(self, moves):
        for(moveType, factory, tileGrab) in moves:
            if tileGrab.tile_type == Tile.BLUE:
                self.blueMoves[tileGrab.pattern_line_dest].append((moveType, factory, tileGrab))
            elif tileGrab.tile_type == Tile.YELLOW:
                self.yellowMoves[tileGrab.pattern_line_dest].append((moveType, factory, tileGrab))
            elif tileGrab.tile_type == Tile.RED:
                self.redMoves[tileGrab.pattern_line_dest].append((moveType, factory, tileGrab))
            elif tileGrab.tile_type == Tile.BLACK:
                self.blackMoves[tileGrab.pattern_line_dest].append((moveType, factory, tileGrab))
            elif tileGrab.tile_type == Tile.WHITE:
                self.whiteMoves[tileGrab.pattern_line_dest].append((moveType, factory, tileGrab))

            self.fstlineMoves[Tile.BLUE] = self.blueMoves[0]
            self.fstlineMoves[Tile.YELLOW] = self.yellowMoves[0]
            self.fstlineMoves[Tile.RED] = self.redMoves[0]
            self.fstlineMoves[Tile.BLACK] = self.blackMoves[0]
            self.fstlineMoves[Tile.WHITE] = self.whiteMoves[0]

            self.sndlineMoves[Tile.BLUE] = self.blueMoves[1]
            self.sndlineMoves[Tile.YELLOW] = self.yellowMoves[1]
            self.sndlineMoves[Tile.RED] = self.redMoves[1]
            self.sndlineMoves[Tile.BLACK] = self.blackMoves[1]
            self.sndlineMoves[Tile.WHITE] = self.whiteMoves[1]

            self.trdlineMoves[Tile.BLUE] = self.blueMoves[2]
            self.trdlineMoves[Tile.YELLOW] = self.yellowMoves[2]
            self.trdlineMoves[Tile.RED] = self.redMoves[2]
            self.trdlineMoves[Tile.BLACK] = self.blackMoves[2]
            self.trdlineMoves[Tile.WHITE] = self.whiteMoves[2]

            self.fthlineMoves[Tile.BLUE] = self.blueMoves[3]
            self.fthlineMoves[Tile.YELLOW] = self.yellowMoves[3]
            self.fthlineMoves[Tile.RED] = self.redMoves[3]
            self.fthlineMoves[Tile.BLACK] = self.blackMoves[3]
            self.fthlineMoves[Tile.WHITE] = self.whiteMoves[3]

            self.fiflineMoves[Tile.BLUE] = self.blueMoves[4]
            self.fiflineMoves[Tile.YELLOW] = self.yellowMoves[4]
            self.fiflineMoves[Tile.RED] = self.redMoves[4]
            self.fiflineMoves[Tile.BLACK] = self.blackMoves[4]
            self.fiflineMoves[Tile.WHITE] = self.whiteMoves[4]

    #check
    def selectFirstInitialMoves(self, moves, game_state):

        tilesTotal = [0, 0, 0, 0, 0]
        tilesHands = [0, 0, 0, 0, 0]

        mostToLine = 0
        returnMove = None

        for factory in game_state.factories:
            for i in range(0, 4):
                tilesTotal[i] += factory.tiles[i]
                tilesHands[i] += 1

        for tile in Tile:
            for moveType, factory, tileGrab in self.fthlineMoves[tile]:
                if tileGrab.num_to_pattern_line > mostToLine:
                    returnMove = (moveType, factory, tileGrab)
                    mostToLine = tileGrab.num_to_pattern_line
            if mostToLine == 4:
                self.previousMoves = returnMove
                return returnMove
            else:
                mostToLine = 0

        for tile in Tile:
            for moveType, factory, tileGrab in self.trdlineMoves[tile]:
                if tileGrab.num_to_pattern_line > mostToLine:
                    returnMove = (moveType, factory, tileGrab)
                    mostToLine = tileGrab.num_to_pattern_line
            if mostToLine == 3:
                self.previousMoves = returnMove
                return returnMove
            else:
                mostToLine = 0

        for tile in Tile:
            for moveType, factory, tileGrab in self.sndlineMoves[tile]:
                if tileGrab.num_to_pattern_line > mostToLine:
                    returnMove = (moveType, factory, tileGrab)
                    mostToLine = tileGrab.num_to_pattern_line
            if mostToLine == 2:
                self.previousMoves = returnMove
                return returnMove
            else:
                mostToLine = 0

        for tile in Tile:
            for moveType, factory, tileGrab in self.fstlineMoves[tile]:
                if tileGrab.num_to_pattern_line > mostToLine:
                    returnMove = (moveType, factory, tileGrab)
                    mostToLine = tileGrab.num_to_pattern_line
            if mostToLine == 1:
                self.previousMoves = returnMove
                return returnMove
            else:
                mostToLine = 0

    #check
    def breadthFirstSearch(self, game_state):
        startTime = time.time()
        gameStateQueue = Queue()
        gameStateQueue.push((None, game_state))
        moveStatePairs = {}
        i = 0
        while(not gameStateQueue.isEmpty()):
            if time.time() - startTime > 0.97:
                break
            prevMove, curGameState = gameStateQueue.pop()
            possibleMoves = self.nextMoves(curGameState)
            if len(possibleMoves) == 0:
                return moveStatePairs
            for move in possibleMoves:
                newGameState = self.stateAfterMove(move, curGameState)
                if i < 1:
                    gameStateQueue.push((move, newGameState))
                    moveStatePairs[newGameState] = move
                else:
                    gameStateQueue.push((prevMove, newGameState))
                    moveStatePairs[newGameState] = prevMove
            i += 1

        return moveStatePairs
        """
        gameStateQueue = Queue()
        gameStateQueue.push(game_state)
        moveStatePairs = []
        while (not gameStateQueue.isEmpty()):
            curGameState = gameStateQueue.pop()
            possibleMoves = self.nextMoves(curGameState)
            if len(possibleMoves) == 0:
                return moveStatePairs
            for move in possibleMoves:
                newGameState = self.stateAfterMove(move, curGameState)
                #gameStateQueue.push(newGameState)
                moveStatePairs.append((move, newGameState))
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
                    heurisitic = self.Heurisitic(newGameState, bestScore)
                    priority = next_cost + heurisitic
                    if i < 1:
                        priorityQueue.push((move, newGameState), priority)
                    else:
                        priorityQueue.push((prevMove, newGameState), priority)
            i += 1

        return moveStatePairs

    #check
    def isFirstRound(self, curState):
        if (curState.grid_state == 0).all():
            return True
        else:
            return False

        """
        if curState.line_tile == [-1]*5:
            return True
        else:
            return False
            """

    #check
    def isRoundJustStart(self, curState):
        if curState.lines_tile == [-1] * 5:
            return True
        else:
            return False
        """
        if len(curPlayerState.player_trace.moves[-1]) == 0:
            return True
        else:
            return False
            """

    def Heurisitic(self, gameState, bestScore):
        return bestScore - self.evaluateGameState(gameState)

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

    #check
    def nextMoves(self, game_state):
        moves = game_state.players[self.id].GetAvailableMoves(game_state)
        possibleMoves = []
        lineIndexPairTileType = []
        targetWallColumns = []
        targetWallRows = []
        patternLineColor = game_state.players[self.id].lines_tile
        patternLineNum = game_state.players[self.id].lines_number
        playerWall = game_state.players[self.id].grid_state

        for i in range(0,4):
            if patternLineColor[i] != -1:
                lineIndexPairTileType.append((i, patternLineColor[i]))

        for lineIndex, tile_type in lineIndexPairTileType:
            targetWallColumns.append((lineIndex + tile_type) % 5)

        for row in range(0,4):
            for col in range(0,4):
                if playerWall[row][col] == 1:
                    targetWallRows.append(row)
                    break

        for moveType, factory, tileGrab in moves:
            if patternLineColor[tileGrab.pattern_line_dest] != -1:
                possibleMoves.append((moveType, factory, tileGrab))
            else:
                if (tileGrab.pattern_line_dest + tileGrab.tile_type) % 5 in targetWallColumns:
                    possibleMoves.append((moveType, factory, tileGrab))
                if tileGrab.pattern_line_dest in targetWallRows:
                    possibleMoves.append((moveType, factory, tileGrab))

        result = self.postProcessPossibleMoves(possibleMoves)
        return result

    #check
    def postProcessPossibleMoves(self, possibleMoves):
        fstLineMost = -1
        secLineMost = -1
        trdLineMost = -1
        fthLineMost = -1
        fifLineMost = -1
        moves = [None, None, None, None, None]
        result = []

        for moveType, factory, tileGrab in possibleMoves:
            if tileGrab.pattern_line_dest == 0:
                if tileGrab.num_to_pattern_line > fstLineMost:
                    moves[0] = (moveType, factory, tileGrab)
                elif tileGrab.num_to_pattern_line == fstLineMost:
                    (_,_,t) = moves[0]
                    if tileGrab.num_to_floor_line < t.num_to_floor_line:
                        moves[0] = (moveType, factory, tileGrab)

            elif tileGrab.pattern_line_dest == 1:
                if tileGrab.num_to_pattern_line > secLineMost:
                    moves[1] = (moveType, factory, tileGrab)
                elif tileGrab.num_to_pattern_line == secLineMost:
                    (_,_,t) = moves[1]
                    if tileGrab.num_to_floor_line < t.num_to_floor_line:
                        moves[1] = (moveType, factory, tileGrab)

            elif tileGrab.pattern_line_dest == 2:
                if tileGrab.num_to_pattern_line > trdLineMost:
                    moves[2] = (moveType, factory, tileGrab)
                elif tileGrab.num_to_pattern_line == trdLineMost:
                    (_,_,t) = moves[2]
                    if tileGrab.num_to_floor_line < t.num_to_floor_line:
                        moves[2] = (moveType, factory, tileGrab)

            elif tileGrab.pattern_line_dest == 3:
                if tileGrab.num_to_pattern_line > fthLineMost:
                    moves[3] = (moveType, factory, tileGrab)
                elif tileGrab.num_to_pattern_line == fthLineMost:
                    (_,_,t) = moves[3]
                    if tileGrab.num_to_floor_line < t.num_to_floor_line:
                        moves[3] = (moveType, factory, tileGrab)

            elif tileGrab.pattern_line_dest == 4:
                if tileGrab.num_to_pattern_line > fifLineMost:
                    moves[4] = (moveType, factory, tileGrab)
                elif tileGrab.num_to_pattern_line == fifLineMost:
                    (_,_,t) = moves[4]
                    if tileGrab.num_to_floor_line < t.num_to_floor_line:
                        moves[4] = (moveType, factory, tileGrab)

        for move in moves:
            if move != None:
                result.append(move)
        return result

    #check
    def stateAfterMove(self, move, curState):
        newState = copy.deepcopy(curState)
        curPlayerState = newState.players[self.id]

        if move[0] == Move.TAKE_FROM_CENTRE:
            tg = move[2]

            if not newState.first_player_taken:
                newState.players[self.id].GiveFirstPlayerToken()
                newState.first_player_taken = True
                newState.next_first_player = self.id

            if tg.num_to_floor_line > 0:
                ttf = []
                for i in range(tg.num_to_floor_line):
                    ttf.append(tg.tile_type)
                newState.players[self.id].AddToFloor(ttf)
                newState.bag_used.extend(ttf)

            if tg.num_to_pattern_line > 0:
                newState.players[self.id].AddToPatternLine(tg.pattern_line_dest, tg.num_to_pattern_line, tg.tile_type)

            newState.centre_pool.RemoveTiles(tg.number, tg.tile_type)

        elif move[0] == Move.TAKE_FROM_FACTORY:
            tg = move[2]
            if tg.num_to_floor_line > 0:
                ttf = []
                for i in range(tg.num_to_floor_line):
                    ttf.append(tg.tile_type)
                newState.players[self.id].AddToFloor(ttf)
                newState.bag_used.extend(ttf)

            if tg.num_to_pattern_line > 0:
                newState.players[self.id].AddToPatternLine(tg.pattern_line_dest, tg.num_to_pattern_line, tg.tile_type)

            fid = move[1]
            fac = newState.factories[fid]
            fac.RemoveTiles(tg.number, tg.tile_type)

            for tile in Tile:
                num_on_fd = fac.tiles[tile]
                if num_on_fd > 0:
                    newState.centre_pool.AddTiles(num_on_fd, tile)
                    fac.RemoveTiles(num_on_fd,tile)
        return newState

    #check
    def evaluateGameState(self, game_state):

        """

        tilesTotal = [0, 0, 0, 0, 0]
        tilesHands = [0,0,0,0,0]
        mostToLine = 0
        returnMove = None
        score_inc = 0

        for factory in game_state.factories:
            for i in range(0,5):
                tilesTotal[i] += factory.tiles[i]
                tilesHands[i] += 1

        patternLineNum = game_state.players[self.id].lines_number
        patternLineType = game_state.players[self.id].lines_tile
        wallScheme = game_state.players[self.id].grid_scheme
        wallState = game_state.players[self.id].grid_state

        for i in range(0,5):
            if patternLineNum[i] == i+1:
                tc = patternLineType[i]
                col = int(wallScheme[i][tc])

                wallState[i][col] = 1
                above = 0
                for j in range(col - 1, -1, -1):
                    val = wallState[i][j]
                    above += val
                    if val == 0:
                        break
                below = 0
                for j in range(col + 1, 5, 1):
                    val = wallState[i][j]
                    below += val
                    if val == 0:
                        break
                left = 0
                for j in range(i - 1, -1, -1):
                    val = wallState[j][col]
                    left += val
                    if val == 0:
                        break
                right = 0
                for j in range(i + 1, 5, 1):
                    val = wallState[j][col]
                    right += val
                    if val == 0:
                        break

                # If the tile sits in a contiguous vertical line of
                # tiles in the grid, it is worth 1*the number of tiles
                # in this line (including itself).
                if above > 0 or below > 0:
                    score_inc += (1 + above + below)

                # In addition to the vertical score, the tile is worth
                # an additional H points where H is the length of the
                # horizontal contiguous line in which it sits.
                if left > 0 or right > 0:
                    score_inc += (1 + left + right)

                # If the tile is not next to any already placed tiles
                # on the grid, it is worth 1 point.
                if above == 0 and below == 0 and left == 0 and right == 0:
                    score_inc += 1

        floor = game_state.players[self.id].floor
        floorScore = [-1, -1, -2, -2, -2, -3, -3]
        penalties = 0
        for i, j in zip(floor, floorScore):
            penalties += i * j

        scoreChange = score_inc + penalties

        if game_state.players[self.id].score + scoreChange < 0:
            score = 0
        else:
            score = game_state.players[self.id].score = scoreChange
        for i in range(0,5):
            if patternLineType[i] != -1 and patternLineNum < i + 1:
                if tilesTotal[patternLineType[i]] < ((i + 1) - patternLineNum[i]):
                    score -= ((i + 1) - patternLineNum[i])
                else:
                    score += 5/tilesHands[patternLineType[i]]
        rows = game_state.players[self.id].GetCompletedRows()
        cols = game_state.players[self.id].GetCompletedColumns()
        sets = game_state.players[self.id].GetCompletedSets()

        bonus = (rows * 2) + (cols * 7) + (sets * 10)

        score += bonus

        return score
        """
        floor = game_state.players[self.id].floor
        floorScore = [-1, -1, -2, -2, -2, -3, -3]
        score = 0
        for i,j in zip(floor, floorScore):
            score += i*j
        patternLineNum = game_state.players[self.id].lines_number
        patternLineType = game_state.players[self.id].lines_tile
        for i in range(0, 4):
            if patternLineNum[i] == i+1:
                score += 1
        return score

    def getCurPlayerState(self, game_state):
        return game_state.players[self.id]

#check
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_,_,item) = heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapify(self.heap)
                break
        else:
            self.push(item,priority)

#check
class Queue:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.insert(0, item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0




