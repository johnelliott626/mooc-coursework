"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Variables to count the number of X and Y values
    xCount = 0
    oCount = 0

    # Iterate through the board
    for row in board:
        for cell in row:
            if cell == X:
                xCount += 1
            elif cell == O:
                oCount += 1

    # If xCount > oCount it is O's turn
    if xCount > oCount:
        return O
    # Else it is X's turn either at the game's start or after O's turn
    else:    
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Set to store all possible actions
    possibleActions = set()

    # Iterate through the board and add empty cells to the set
    for i in range(3):
        for j in range(3):
            cell = board[i][j]
            if cell == EMPTY:
                possibleActions.add((i,j))

    # Return the set
    return possibleActions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Create a newBoard state copy without changing the original 
    newBoard = copy.deepcopy(board)

    # Ensure the action is valid
    if not ((0 <= action[0] and action[0] <= 2) and (0 <= action[1] and action[1] <= 2)):
        raise NameError("Invalid Move Attempt!")
    if newBoard[action[0]][action[1]] != EMPTY:
        raise NameError("Invalid Move Attempt!")

    # The action is valid so implement on the newBoard, by setting the cell to the current player
    newBoard[action[0]][action[1]] = player(board)

    # Return the newBoard state
    return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows for a hoirizontal three in a row winner
    for row in board:
        xWins = all(cell == X for cell in row)
        oWins = all(cell == O for cell in row)
        if xWins:
            return X
        elif oWins:
            return O

    # Check columns for a vertical three in a row winner
    for colIndex in range(3):
        column = [board[0][colIndex], board[1][colIndex], board[2][colIndex]]
        xWins = all(cell == X for cell in column)
        oWins = all(cell == O for cell in column)
        if xWins:
            return X
        elif oWins:
            return O
        
    # Check diagonals for a three in a row winner
    diagonal1 = []
    diagonal2 = []
    for i in range(3):
        diagonal1.append(board[i][i])
        diagonal2.append(board[2 - i][i])

    xWins = all(cell == X for cell in diagonal1)
    oWins = all(cell == O for cell in diagonal1)
    if xWins:
        return X
    elif oWins:
        return O
    
    xWins = all(cell == X for cell in diagonal2)
    oWins = all(cell == O for cell in diagonal2)
    if xWins:
        return X
    elif oWins:
        return O
    
    # There is no winner so return None
    return None
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is over because someone has won
    if winner(board) is not None:
        return True
    
    # Game is over because of a tie
    tieFlag = True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                tieFlag = False
    # If no one has one, it is either a tie or the game is not over
    return tieFlag

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winningPlayer = winner(board)

    if winningPlayer == X:
        return 1
    elif winningPlayer == O:
        return -1 
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Store whose turn it is
    currentPlayer = player(board)

    possibleActions = list(actions(board))

    # Player X is the max player, so choose the possible action that will result in the max outcome
    if currentPlayer == X:
        maxValues = []
        for action in possibleActions:
            boardAfterAction = result(board, action)
            maxValues.append(minValue(boardAfterAction))
        maxOfActions = max(maxValues)
        maxActionIndex = maxValues.index(maxOfActions)
        return possibleActions[maxActionIndex]
    # Else Player O is the min player
    else:
        minValues = []
        for action in possibleActions:
            boardAfterAction = result(board, action)
            minValues.append(maxValue(boardAfterAction))
        minOfActions = min(minValues)
        minActionIndex = minValues.index(minOfActions)
        return possibleActions[minActionIndex]




# Returns the maxValue if the opponent plays optimally (attempts the min value)
def maxValue(board):
    maxOutcome = -2 # A value that will always be the min
    if terminal(board):
        return utility(board)
    else:
        possibleActions = actions(board)
        for action in possibleActions:
            maxOutcome = max(maxOutcome, minValue(result(board, action)))
        return maxOutcome

# Returns the minValue if the opponent plays optimally (attempts the max value)
def minValue(board):
    minOutcome = 2 # A value that will always be the max
    if terminal(board):
        return utility(board)
    else:
        possibleActions = actions(board)
        for action in possibleActions:
            minOutcome = min(minOutcome, maxValue(result(board, action)))
        return minOutcome