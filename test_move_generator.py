from move_generator import generate_moves
import numpy as np

board_1 = [
    ['b_r', 'b_n', 'b_b', 'b_q', 'b_k', 'b_b', 'b_n', 'b_r'],
    ['b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p'],
    ['w_r', 'w_n', 'w_b', 'w_q', 'w_k', 'w_b', 'w_n', 'w_r']
]

def test_pawns():
    """
    Tests pawn movements.

    Parameters: None

    Returns: None
    """
    print("Testing Pawns")
    for i in range(8):
        test_case = [6, i, [[5, i], [4, i]]]
        moves = generate_moves(board_1, test_case[0], test_case[1])
        if moves[0] == test_case[2][0] and moves[1] == test_case[2][1]:
            print("PASS")
        else:
            print("FAIL")

def test_knights():
    """
    Tests knight movements.

    Parameters: None

    Returns: None
    """
    print("Testing Knights")
    test_cases = [
        [0, 1, [[2, 0], [2, 2], [1, 3]]],
        [0, 6, [[2, 5], [2, 7], [1, 4]]],
        [7, 1, [[5, 0], [5, 2], [6, 3]]],
        [7, 6, [[5, 5], [5, 7], [6, 4]]]
    ]
    for test_case in test_cases:
        pass_test = True
        moves = generate_moves(board_1, test_case[0], test_case[1])
        if len(moves) == len(test_case[2]):
            for move in test_case[2]:
                if move not in moves:
                    pass_test = False
                    print("FAIL")
            if pass_test:
                print("PASS")
        else:
            print(f"FAILED ALL KNIGHT MOVES FOR KNIGHT AT {test_case[0]},{test_case[1]}")

def test_rooks():
    """
    Tests rook movements.

    Parameters: None

    Returns: None
    """
    print("Testing Rooks")
    test_cases = generate_rook_test_cases()
    for test_case in test_cases:
        pass_test = True
        moves = generate_moves(board_1, test_case[0], test_case[1])
        if len(moves) == len(test_case[2]):
            for move in test_case[2]:
                if move not in moves:
                    pass_test = False
                    print("FAIL")
            if pass_test:
                print("PASS")
        else:
            print(f"FAILED ALL ROOK MOVES FOR ROOK AT {test_case[0]},{test_case[1]}")

def generate_rook_test_cases():
    """
    Generates test cases for rook movements.

    Parameters: None

    Returns: A list of test cases, where each test case is a list containing the row and column of the piece and a list of its expected moves.
    """
    return generate_bqr_test_cases("rook")

def test_bishops():
    """
    Tests bishop movements.

    Parameters: None

    Returns: None
    """
    print("Testing Bishops")
    test_cases = generate_bishop_test_cases()
    for test_case in test_cases:
        pass_test = True
        moves = generate_moves(board_1, test_case[0], test_case[1])
        if len(moves) == len(test_case[2]):
            for move in test_case[2]:
                if move not in moves:
                    pass_test = False
                    print("FAIL")
            if pass_test:
                print("PASS")
        else:
            print(f"FAILED ALL BISHOP MOVES FOR BISHOP AT {test_case[0]},{test_case[1]}")

def generate_bishop_test_cases():
    """
    Generates test cases for bishop movements.

    Parameters: None

    Returns: A list of test cases, where each test case is a list containing the row and column of the piece and a list of its expected moves.
    """
    return generate_bqr_test_cases("bishop")

def test_queens():
    """
    Tests queen movements.

    Parameters: None

    Returns: None
    """
    print("Testing Queens")
    test_cases = generate_queen_test_cases()
    for test_case in test_cases:
        pass_test = True
        moves = generate_moves(board_1, test_case[0], test_case[1])
        if len(moves) == len(test_case[2]):
            for move in test_case[2]:
                if move not in moves:
                    pass_test = False
                    print("FAIL")
            if pass_test:
                print("PASS")
        else:
            print(f"FAILED ALL QUEEN MOVES FOR QUEEN AT {test_case[0]},{test_case[1]}")

def generate_queen_test_cases():
    """
    Generates test cases for queen movements.

    Parameters: None

    Returns: A list of test cases, where each test case is a list containing the row and column of the piece and a list of its expected moves.
    """
    return generate_bqr_test_cases("queen")

def generate_bqr_test_cases(piece_name):
    """
    Generates test cases for bishop, queen, or rook movements.

    Parameters:
    piece_name (str): The name of the piece to generate test cases for. Can be 'rook', 'bishop', or 'queen'.

    Returns: A list of test cases, where each test case is a list containing the row and column of the piece and a list of its expected moves.
    """
    test_cases = []
    if piece_name == 'rook':
        starting_positions = [[0, 0], [0, 7], [7, 0], [7, 7]]
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    elif piece_name == 'bishop':
        starting_positions = [[0, 2], [0, 5], [7, 2], [7, 5]]
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    elif piece_name == 'queen':
        starting_positions = [[0, 3], [7, 3]]
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    else:
        raise ValueError('Invalid piece name')

    for row, col in starting_positions:
        moves = []
        for direction in directions:
            for i in range(1, 8):
                new_row = row + direction[0] * i
                new_col = col + direction[1] * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    moves.append([new_row, new_col])
                else:
                    break
        test_cases.append([row, col, moves])

    return test_cases

test_pawns()
test_knights()
test_rooks()
test_bishops()
test_queens()