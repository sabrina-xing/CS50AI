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
    row = board_temp[action[0]]
    j = 0
    for cell in row:
        if j == action[1]:
            if cell is not EMPTY:
                raise Exception("Invalid Move")
            else:
                cell = turn
            return board_temp
        j += 1


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Iterate through rows
    for i in range(2):
        column = set()
        for row in board:
            column.add(row[i])

            # Check for vertically won
            if row.count(X) == 3:
                return X
            elif row.count(O) == 3:
                return O

        # Check for horizontally won
        if column.count(X) == 3:
            return X
        elif column.count(O) == 3:
            return O

    # Check for diagonally won
    diagonal_left = [board[0][0], board[1][1], board[2][2]]
    diagonal_right = [board[0][2], board[1][1], board[2][1]]
    if diagonal_left.count(X) == 3 or diagonal_right.count(X) == 3:
        return X
    elif diagonal_left.count(O) == 3 or diagonal_right.count(O) == 3:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if game board is empty
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # Check if someone won the game
    if winner(board=board) == None:
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
    util = 0
    if player(board=board) == X:
        util = -100
    else:
        util = -100

    for action in moves:
        if player(board=board) == X:
            util_temp = minvalue(result(board=board, action=action))
            if util < util_temp:
                util = util_temp
                best_action = action
        else:
            util = maxvalue(result(board=board, action=action))
            if util > util_temp:
                util = util_temp
                best_action = action

    return best_action


def maxvalue(board):
    # if game is over
    if terminal(board=board):
        return utility(board=board)

    val = -100
    for move in actions(board=board):
        val = max(val, minvalue(result(board=board, action=move)))
    return val


def minvalue(board):
    # if game is over
    if terminal(board=board):
        return utility(board=board)

    val = 100
    for move in actions(board=board):
        val = min(val, maxvalue(result(board=board, action=move)))
    return val
