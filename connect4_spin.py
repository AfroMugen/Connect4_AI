from copy import deepcopy
import sys
"""
MiniMax algorithm starts on line 331. (miniMax, maximum, and minimum)
"""

# Global containers used in functions
rows = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
columns = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4}
rowLabels = ["a", "b", "c", "d", "e", "f", "g", "h"]
columnLabels = ["1", "2", "3", "4", "5"]
flipOptions = ["n", "1", "2", "3", "4", "5"]
playerName = {"R": "Red", "Y": "Yellow"}
playerAI = {"R": "Y", "Y": "R"}
color = {"R": "\033[91m", "Y": "\033[93m", "E": "\033[0m"}

def main():
    # Check for proper arg amount
    if len(sys.argv) != 1:
        print("Warning: %s does not take arguments." % (sys.argv[0]))
        return

    # Keep prompting user until acceptable player symbol is entered
    while True:
        player = input("Which player would you like to play (R/Y)? ")
        if player in ("R", "Y", "r", "y"):
            break

    if player == "r":
        player = "R"
    elif player == "y":
        player = "Y"

    playConnect4(player)


def playConnect4(player):
    """
    Begin connect four game
    Arguments:
        @player: Player symbol of starting player
    Returns:
        None
    """
    board = createStartBoard()

    if player == "R":
        print("\nNo moves yet")
        printBoard(board)

    curPlayer = "R"
    terminal = False
    winner = None
    while not terminal:
        if curPlayer == player:
            move = input("Please enter your move (format row-column-flip_column): ")
            while not isValidMove(board, move):
                move = input("Please enter your move (format row-column-flip_column): ")
        
        else:
            move = miniMax(board, curPlayer)

        updateBoard(board, move, curPlayer)
        print("\n%s moves " % (playerName[curPlayer]) + move)
        printBoard(board)

        curPlayer = playerAI[curPlayer]
        terminal, winner = isTerminal(board)

    if winner:
        print("\n%s wins! Game Over" % playerName[winner])
    else:
        print("\nDraw! Game Over")


def createStartBoard():
    """
    Create empty board
    Arguments:
        None
    Returns:
        None
    """
    return [["E"]*5 for _ in range(8)]


def printBoard(board:list):
    """
    Print the current game board
    Arguments:
        @board: Current state of the game
    Returns:
        None
    """
    print("  1 2 3 4 5 ")
    print(" +-+-+-+-+-+")
    for row in range(len(board)):
        printString = rowLabels[row] + "|"
        for column in range(len(board[row])):
            printString = printString + color[board[row][column]] + board[row][column] + "\033[0m" + "|"
        print(printString)
        print(" +-+-+-+-+-+")


def isValidMove(board: list, move:str):
    """
    Checks if given move is valid
    Arguments:
        @board: Current state of the game
        @move: Move being checked
    Returns:
        True if move is valid, False otherwise
    """
    moves = move.split("-")
    if ((len(moves) != 3) or (moves[0] not in rowLabels) or (moves[1] not in columns) or 
    (moves[2] not in columns and moves[2] != "n") or (board[rows[moves[0]]][columns[moves[1]]] != "E")):
        return False

    return True


def updateBoard(board:list, move:str, player:str):
    """
    Updates the board with given move
    Arguments:
        @board: Current state of the game
        @move: Move being processed
        @player: Player symbol being placed on the board
    """
    moves = move.split("-")
    board[rows[moves[0]]][columns[moves[1]]] = player
    flipColumn(board, moves[2])


def flipColumn(board: list, column: str):
    """
    Flips given column in game board
    Arguments:
        @board: Current state of board
        @column: Column label
    Returns:
        None
    """
    if column == "n":
        return
    for i in range(len(board)//2):
        temp = board[i][columns[column]]
        board[i][columns[column]] = board[len(board) - 1 - i][columns[column]]
        board[len(board) - 1 - i][columns[column]] = temp


def isTerminal(board: list):
    """
    Check if current state of board is a "Game Over!"
    Arguments:
        @board: Current state of the game
    Returns:
        Tuple (isTerminal, winner)
    """
    axis = [(0, 1), (1, 1), (1, 0), (-1, 1)]
    tie = True
    rWin = None
    yWin = None
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == "E":
                tie = False
            for line in axis:
                pos = (row + line[0], column + line[1])
                pos1 = (row + line[0]*2, column + line[1]*2)
                pos2 = (row + line[0]*3, column + line[1]*3)
                if ((0 <= pos2[0] < len(board)) and (0 <= pos2[1] < len(board[row]))):
                    if (board[row][column] == board[pos[0]][pos[1]] == board[pos1[0]][pos1[1]] == board[pos2[0]][pos2[1]] == "R"):
                        rWin = "R"
                    elif (board[row][column] == board[pos[0]][pos[1]] == board[pos1[0]][pos1[1]] == board[pos2[0]][pos2[1]] == "Y"):
                        yWin = "Y"

    if rWin and yWin:
        return (True, None)
    if rWin:
        return (True, rWin)
    if yWin:
        return (True, yWin)

    return (tie, None)


def calcScore(board: list, player: str):
    """
    Heuristic function: Calculates the score of the current state of the
    board (player twos and threes - opponent twos and threes)
    Arguments:
        @board: Current state of the game
        @player: Player symbol being checked as max
    Returns:
        The score of the current board mentioned above
    """
    ai = playerAI[player]
    threeScore = checkThrees(board, ai)
    twoScore = checkTwos(board, ai)

    playerThreeScore = checkThrees(board, player)
    playerTwoScore = checkTwos(board, player)

    return (threeScore + twoScore) - (playerThreeScore + playerTwoScore)


def checkThrees(board: list, player: str):
    """
    Find total number of patterns that could potentially result in a win
    Arguments:
        @board: Current state of the game
        @player: Player symbol being checked in patterns
    Returns:
        Total number of three patterns in the current state of the board
    """
    threes = 0
    axis = [(0, 1), (1, 1), (1, 0), (-1, 1)]
    for row in range(len(board)):
        for column in range(len(board[row])):
            for line in axis:
                pos = (row + line[0], column + line[1])
                pos1 = (row + line[0]*2, column + line[1]*2)
                neg = (row - line[0], column - line[1])
                neg1 = (row - line[0]*2, column - line[1]*2)
                # Three spots are available to be checked: (xXx) where X is board[row][column]
                if ((board[row][column] == player) and (0 <= pos[0] < len(board)) and 
                (0 <= pos[1] < len(board[row])) and (0 <= neg[0] < len(board)) and 
                (0 <= neg[1] < len(board[row]))):
                    # Four spots are available to be checked: (xXxx)
                    if ((0 <= pos1[0] < len(board)) and (0 <= pos1[1] < len(board[row]))):
                        # Check for pattern (xXex)
                        if (player == board[neg[0]][neg[1]] == board[pos1[0]][pos1[1]] and 
                        board[pos[0]][pos[1]] == "E"):
                            # print("xXex")
                            threes += 1

                        # Check for pattern (xXxe)
                        if (player == board[neg[0]][neg[1]] == board[pos[0]][pos[1]] and 
                        board[pos1[0]][pos1[1]] == "E"):
                            # print("xXxe")
                            threes += 1

                    # Four spots are available to be checked: (xxXx)
                    if ((0 <= neg1[0] < len(board)) and (0 <= neg1[1] < len(board[row]))):
                        # Check for pattern (xeXx)
                        if (player == board[pos[0]][pos[1]] == board[neg1[0]][neg1[1]] and 
                        board[neg[0]][neg[1]] == "E"):
                            # print("xeXx")
                            threes += 1
                        
                        # Check for pattern (exXx)
                        if (player == board[neg[0]][neg[1]] == board[pos[0]][pos[1]] and 
                        board[neg1[0]][neg1[1]] == "E"):
                            # print("exXx")
                            threes += 1

    return threes


def checkTwos(board: list, player: str):
    """
    Find total number of patterns that could potentially result in a "three in a row"
    Arguments:
        @board: Current state of the game
        @player: Player symbol being checked in patterns
    Returns:
        Total number of two patterns in the current state of the board
    """
    twos = 0
    axis = [(0, 1), (1, 1), (1, 0), (-1, 1)]
    for row in range(len(board)):
        for column in range(len(board[row])):
            for line in axis:
                pos = (row + line[0], column + line[1])
                pos1 = (row + line[0]*2, column + line[1]*2)
                # Three spots are available to check: (Xxx) where X = board[row][column]
                if ((0 <= pos1[0] < len(board)) and (0 <= pos1[1] < len(board[row]))):
                    # Check for pattern (Xxe)
                    if (player == board[row][column] == board[pos[0]][pos[1]] and board[pos1[0]][pos1[1]] == "E"):
                        twos += 1

                    # Check for pattern (Exx)
                    elif (board[row][column] == "E" and board[pos[0]][pos[1]] == board[pos1[0]][pos1[1]] == player):
                        twos += 1

                    # Check for pattern (Xex)
                    elif (player == board[row][column] == board[pos1[0]][pos1[1]] and board[pos[0]][pos[1]] == "E"):
                        twos += 1

    return twos


def findPlayableMoves(board: list):
    """
    Finds playable moves for the current board including flips
    Arguments:
        @board: Current state of the game
    Returns:
        List of moves that are worth traversing
    """
    moves = []
    for row in rowLabels:
        for column in columnLabels:
            if board[rows[row]][columns[column]] != "E":
                continue
            for flip in flipOptions:
                if flip != "n" and not worthFlip(board, flip):
                    continue
                moves.append(row + "-" + column + "-" + flip)

    return moves


def worthFlip(board: list, flip: str):
    """
    Helper function: Determines if column would change if flipped
    Arguments:
        @board: Current state of the game
        @flip: Column label
    Returns:
        True if column changes when flipped and False otherwise
    """
    for row in range(len(board)//2):
        if board[row][columns[flip]] != board[len(board) - 1 - row][columns[flip]]:
            return True

    return False
            

def miniMax(board: list, ai: str):
    """
    Start minimax algorithm
    Arguments:
        @board: Current state of the game
        @ai: AI's player icon
    Returns:
        Optimal move for max player (AI)
    """
    tempBoard = deepcopy(board)
    return maximum(tempBoard, 3, -sys.maxsize, sys.maxsize, ai)[0]


def maximum(board: list, depth: int, alpha: int, beta: int, ai: str):
    """
    Find optimal move for max (AI)
    Arguments:
        @board: Current state of the game
        @depth: Current depth of search tree
        @alpha: Alpha pruning value for max
        @beta: Beta pruning value for min
        @ai: AI's player icon
    Returns:
        Tuple (max optimal move, heuristic score of current state)
    """
    terminal, winner = isTerminal(board)

    if terminal:
        if winner == ai:
            return (None, sys.maxsize)
        elif winner == playerAI[ai]:
            return (None, -sys.maxsize)
        else:
            return (None, 0)

    if depth == 0:
        return (None, calcScore(board, ai))
    
    moves = findPlayableMoves(board)
    value = -sys.maxsize
    ret = moves[0]
    for move in moves:
        tempBoard = deepcopy(board)
        updateBoard(tempBoard, move, ai)
        score = minimum(tempBoard, depth - 1, alpha, beta, playerAI[ai])[1]
        if score > value:
            value = score
            ret = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return (ret, value)


def minimum(board: list, depth: int, alpha: int, beta: int, player: str):
    """
    Find optimal move for min (player)
    Arguments:
        @board: Current state of the game
        @depth: Current depth of search tree
        @alpha: Alpha pruning value for max
        @beta: Beta pruning value for min
        @ai: AI's player icon
    Returns:
        Tuple (min optimal move, heuristic score of current state)
    """
    terminal, winner = isTerminal(board)

    if terminal:
        if winner == player:
            return (None, -sys.maxsize)
        elif winner == playerAI[player]:
            return (None, sys.maxsize)
        else:
            return (None, 0)

    if depth == 0:
        return (None, calcScore(board, playerAI[player]))
    
    moves = findPlayableMoves(board)
    value = sys.maxsize
    ret = moves[0]
    for move in moves:
        tempBoard = deepcopy(board)
        updateBoard(tempBoard, move, player)
        score = maximum(tempBoard, depth - 1, alpha, beta, playerAI[player])[1]
        if score < value:
            value = score
            ret = move
        beta = min(beta, score)
        if beta <= alpha:
            break

    return (ret, value)
                

if __name__ == "__main__":
    main()