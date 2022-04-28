"""
Tic Tac Toe Player
"""
import copy
import math

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
    a = []
    set_r = range(len(board))
    for i in set_r:
        for j in set_r:
            a.append(board[i][j])
    if a.count(X) > a.count(O):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    a = []
    set_r = range(len(board))
    for i in set_r:
        for j in set_r:
            if board[i][j] == EMPTY:
                a += [(i, j)]
    return a


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception

    play = player(board)
    cboard = copy.deepcopy(board)
    cboard[i][j] = play
    return cboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    def check(val):
        if val == 'XXX':
            return 'X'
        elif val == 'OOO':
            return 'O'
        else:
            return None

    a = ''
    for i in range(len(board)):
        for j in range(len(board)):
            a += str(board[i][j])
        if check(a) is not None:
            return check(a)
        a = ''

    for i in range(len(board)):
        for j in range(len(board)):
            a += str(board[j][i])
        if check(a) is not None:
            return check(a)
        a = ''

    a = str(board[0][0]) + str(board[1][1]) + str(board[2][2])
    if check(a) is not None:
        return check(a)

    a = str(board[0][2]) + str(board[1][1]) + str(board[2][0])
    if check(a) is not None:
        return check(a)

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    set_r = range(len(board))
    if winner(board) is not None:
        return True
    for i in set_r:
        for j in set_r:
            if board[i][j] == EMPTY:
                return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    if winner(board) == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def maxval(state):
        if terminal(state) == True:
            return utility(state)
        v = -5
        for action in actions(state):
            v = max(v, minval(result(state, action)))
        return v

    def minval(state):
        if terminal(state) == True:
            return utility(state)
        v = 5
        for action in actions(state):
            v = min(v, maxval(result(state, action)))
        return v

    if player(board) == O:
        a = 5
        for action in actions(board):
            if minval(board) == min(a, maxval(result(board, action))):
                return action
    if player(board) == X:
        a = -5
        for action in actions(board):
            if maxval(board) == max(a, minval(result(board, action))):
                return action


"""
dummy = [[X, X, O], [X, X, O], [O, O, EMPTY]]
print(dummy[0][0], dummy[1][0], dummy[2][0])
print(dummy[0][1], dummy[1][1], dummy[2][1])
print(dummy[0][2], dummy[1][2], dummy[2][2])

print(minimax(dummy))
"""
