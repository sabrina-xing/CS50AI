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
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0

    for row in board:
        countX += row.count(X)
        countO += row.count(O)

    if countX == countO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    i = 0
    for row in board:
        j = 0
        for cell in row:
            if cell == EMPTY:
                actions.add((i, j))
            j += 1
        i += 1

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # If game is over return error
    if terminal(board=board):
        raise Exception("Invalid move")

    turn = player(board=board)
    board_temp = copy.deepcopy(board)

    # Check if square is empty and fills square
    row, col = action
    if board_temp[row][col] is not EMPTY:
        raise Exception("Invalid move")

    board_temp[row][col] = turn

    return board_temp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Iterate through rows
    for i in range(3):
        if board[i].count(X) == 3:
            return X
        elif board[i].count(O) == 3:
            return O

        # Check columns
        if [board[0][i], board[1][i], board[2][i]].count(X) == 3:
            return X
        elif [board[0][i], board[1][i], board[2][i]].count(O) == 3:
            return O

    # Check diagonals
    if [board[0][0], board[1][1], board[2][2]].count(X) == 3 or [
        board[0][2],
        board[1][1],
        board[2][0],
    ].count(X) == 3:
        return X
    elif [board[0][0], board[1][1], board[2][2]].count(O) == 3 or [
        board[0][2],
        board[1][1],
        board[2][0],
    ].count(O) == 3:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if someone won the game
    if winner(board=board) == X or winner(board=board) == O:
        return True

    # Check if game board is empty
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check winner of game
    winner_player = winner(board=board)

    # Return corresponding utility value
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


# TODO: Implement
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if board is terminal
    if terminal(board=board):
        return None

    moves = actions(board=board)
    best_action = None
    if player(board=board) == X:
        best_val = -math.inf
        for action in moves:
            util_temp = minvalue(result(board=board, action=action))
            if util_temp > best_val:
                best_val = util_temp
                best_action = action
    else:
        best_val = math.inf
        for action in moves:
            util_temp = maxvalue(result(board=board, action=action))
            if util_temp < best_val:
                best_val = util_temp
                best_action = action
    return best_action


def maxvalue(board):
    # if game is over
    if terminal(board=board):
        return utility(board=board)

    val = -math.inf
    for move in actions(board=board):
        val = max(val, minvalue(result(board=board, action=move)))
    return val


def minvalue(board):
    # if game is over
    if terminal(board=board):
        return utility(board=board)

    val = math.inf
    for move in actions(board=board):
        val = min(val, maxvalue(result(board=board, action=move)))
    return val
