import tictactoe as ttt

X = ttt.X
O = ttt.O
EMPTY = ttt.EMPTY

board = ttt.board


#
def test_player():
    """
    Test the player function to ensure it returns the correct player based on the board state.
    """
    # Reset the board to initial state
    board = ttt.initial_state()

    # Check if player returns X when it's X's turn
    assert (
        ttt.player(board) == X
    ), "Test failed: player should return X when it's X's turn."

    # Make a move and check if player returns O
    board[0][0] = X
    assert ttt.player(board) == O, "Test failed: player should return O after X's move."

    # Make another move and check if player returns X
    board[1][1] = O
    assert ttt.player(board) == X, "Test failed: player should return X after O's move."

    # When the board is full, player should return None
    full_board = [[X, O, X], [O, X, O], [O, X, O]]
    assert (
        ttt.player(full_board) is None
    ), "Test failed: player should return None when the board is full."


def test_actions():
    """
    Test the actions function to ensure it returns all empty cells as possible actions.
    """
    # Reset the board to initial state
    board = ttt.initial_state()

    # Check if actions returns all empty cells
    expected_actions = {(i, j) for i in range(3) for j in range(3)}
    assert (
        ttt.actions(board) == expected_actions
    ), "Test failed: actions did not return all empty cells."


def test_actions_no_empty():
    """
    Test the actions function when there are no empty cells.
    """
    # Board is completely filled
    full_board = [[X, O, X], [O, X, O], [X, O, X]]
    assert (
        ttt.actions(full_board) == set()
    ), "Test failed: actions should return an empty set when no cells are empty."


def test_action_all_but_one():
    """
    Test the actions function when all but one cell is filled.
    """
    # Board has only one empty cell left
    almost_full_board = [[X, O, X], [O, X, O], [X, O, EMPTY]]
    assert ttt.actions(almost_full_board) == {
        (2, 2)
    }, "Test failed: actions did not return the correct single empty cell."


def test_result():
    """
    Test the result function to ensure it correctly updates the board after a move.
    """
    # Reset the board to initial state
    board = ttt.initial_state()

    # Make a valid move
    new_board = ttt.result(board, (0, 0))

    # Check if the move was applied correctly
    expected_board = [[X, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert (
        new_board == expected_board
    ), "Test failed: result did not apply the move correctly."

    # Attempt to make an invalid move (should raise an error)
    try:
        ttt.result(new_board, (0, 0))  # Cell already occupied by X
        assert False, "Test failed: result should raise an error for an invalid move."
    except ValueError:
        pass  # Expected behavior


def test_winner_X():
    """
    Test the winner function to ensure it correctly identifies the winner.
    """
    # Test horizontal win
    horizontal_win_board = [[X, X, X], [O, O, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert (
        ttt.winner(horizontal_win_board) == X
    ), "Test failed: winner did not identify horizontal win correctly."

    # Test vertical win
    vertical_win_board = [[X, O, EMPTY], [X, O, EMPTY], [X, EMPTY, EMPTY]]
    assert (
        ttt.winner(vertical_win_board) == X
    ), "Test failed: winner did not identify vertical win correctly."

    # Test diagonal win
    diagonal_win_board = [[X, O, O], [O, X, EMPTY], [EMPTY, EMPTY, X]]
    assert (
        ttt.winner(diagonal_win_board) == X
    ), "Test failed: winner did not identify diagonal win correctly."

    # Test no winner
    no_winner_board = [[X, O, X], [O, X, O], [O, X, O]]
    assert (
        ttt.winner(no_winner_board) is None
    ), "Test failed: winner should return None when there is no winner."


def test_winner_O():
    """
    Test the winner function to ensure it correctly identifies the winner for O.
    """
    # Test horizontal win
    horizontal_win_board = [[O, O, O], [X, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert (
        ttt.winner(horizontal_win_board) == O
    ), "Test failed: winner did not identify horizontal win for O correctly."

    # Test vertical win
    vertical_win_board = [[O, X, EMPTY], [O, X, EMPTY], [O, EMPTY, EMPTY]]
    assert (
        ttt.winner(vertical_win_board) == O
    ), "Test failed: winner did not identify vertical win for O correctly."

    # Test diagonal win
    diagonal_win_board = [[O, X, X], [X, O, EMPTY], [EMPTY, EMPTY, O]]
    assert (
        ttt.winner(diagonal_win_board) == O
    ), "Test failed: winner did not identify diagonal win for O correctly."


def test_terminal():
    """
    Test the terminal function to ensure it correctly identifies if the game is over.
    """
    # Test game over with a winner
    winning_board = [[X, X, X], [O, O, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert (
        ttt.terminal(winning_board) is True
    ), "Test failed: terminal should return True when there is a winner."

    # Test game over with a tie
    tie_board = [[X, O, X], [O, X, O], [O, X, O]]
    assert (
        ttt.terminal(tie_board) is True
    ), "Test failed: terminal should return True when the game is a tie."

    # Test game not over
    not_over_board = [[X, O, EMPTY], [O, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert (
        ttt.terminal(not_over_board) is False
    ), "Test failed: terminal should return False when the game is not over."


def test_utility():
    """
    Test the utility function to ensure it returns the correct score for the board state.
    """
    # Test utility for X win
    x_win_board = [[X, X, X], [O, O, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert (
        ttt.utility(x_win_board) == 1
    ), "Test failed: utility should return 1 for X win."

    # Test utility for O win
    o_win_board = [[O, O, O], [X, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert (
        ttt.utility(o_win_board) == -1
    ), "Test failed: utility should return -1 for O win."

    # Test utility for tie
    tie_board = [[X, O, X], [O, X, O], [O, X, O]]
    assert (
        ttt.utility(tie_board) == 0
    ), "Test failed: utility should return 0 for a tie."

    # Test utility for non-terminal state
    not_terminal_board = [[X, O, EMPTY], [O, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert ttt.utility(not_terminal_board) == 0
