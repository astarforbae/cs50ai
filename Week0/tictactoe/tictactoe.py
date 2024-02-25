"""
Tic Tac Toe Player
"""
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
    cnt = 0
    for row in board:
        for place in row:
            if place is not EMPTY:
                cnt += 1
    return X if cnt % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_list.add((i, j))
    return actions_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # 深拷贝列表
    cur_board = copy.deepcopy(board)
    i, j = action
    if i > 2 or i < 0 or j > 2 or j < 0:
        raise Exception("illegal place")
    if cur_board[i][j] is EMPTY:
        cur_board[i][j] = player(cur_board)
    else:
        raise Exception("already taken")
    return cur_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # 检查行
    for i in range(3):
        if board[i][0] is not None and board[i][1] is not None and board[i][2] is not None:
            if board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]

    # 检查列
    for i in range(3):
        if board[0][i] is not None and board[1][i] is not None and board[2][i] is not None:
            if board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]

    # 检查对角线
    if board[0][0] is not None and board[1][1] is not None and board[2][2] is not None:
        if board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]

    if board[0][2] is not None and board[1][1] is not None and board[2][0] is not None:
        if board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        for place in row:
            if place is None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner is None:
        return 0
    elif game_winner == X:
        return 1
    else:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # 获得Player
    cur_player = player(board)
    # 根据Player选择策略
    return max_value(board, 10)[0] if cur_player == X else min_value(board, -10)[0]


def max_value(board, cut_value):
    """
    获得当前board的最大值
    """
    if terminal(board):
        return None, utility(board)
    best_value = -10
    best_action = None
    for action in actions(board):
        _, value = min_value(result(board, action), best_value)
        if value > best_value:
            best_value = value
            best_action = action

        if value > cut_value:
            return None, 1
    return best_action, best_value


def min_value(board, cut_value):
    """
    获得当前board的最小值
    """
    if terminal(board):
        return None, utility(board)

    best_value = 10
    best_action = None
    for action in actions(board):
        _, value = max_value(result(board, action), best_value)
        if value < best_value:
            best_value = value
            best_action = action
        if value < cut_value:
            return None, -1
    return best_action, best_value
