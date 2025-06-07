"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    If there are no EMPTY cells, it returns None
    """
    x_count = 0
    o_count = 0
    empty_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
            else:
                empty_count += 1
    if empty_count == 0:
        return None
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    for rows in board:
        for cell in rows:
            if cell == EMPTY:
                return {
                    (i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY
                }
    return set()  # No available actions if all cells are filled


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action: Cell is already occupied.")

    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O

    # Check columns
    for col_index in range(3):
        column = [board[row_index][col_index] for row_index in range(3)]
        if all(cell == X for cell in column):
            return X
        elif all(cell == O for cell in column):
            return O

    # Check diagonals
    # Top-left to bottom-right
    diag1 = [board[i][i] for i in range(3)]
    if all(cell == X for cell in diag1):
        return X
    elif all(cell == O for cell in diag1):
        return O

    # Top-right to bottom-left
    diag2 = [board[i][2 - i] for i in range(3)]
    if all(cell == X for cell in diag2):
        return X
    elif all(cell == O for cell in diag2):
        return O

    return None  # No winner yet


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there's a winner, the game is over
    if winner(board) is not None:
        return True

    # If no winner, check if the board is full (a tie game)
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False  # Found an empty cell, game is not over yet

    # If no winner and no empty cells, the board is full, so it's a tie game (terminal state)
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0  # No winner, so utility is 0 (tie or ongoing game)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
