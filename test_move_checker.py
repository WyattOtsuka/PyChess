from move_checker import *
import unittest 


def generate_board(pieces):
    """Helper to create a board layout from a list of piece positions.
       Example: pieces = ['w_r 0,0', 'b_k 7,7']
    """
    board = [['' for _ in range(8)] for _ in range(8)]
    for piece_and_pos in pieces:
        piece, pos = piece_and_pos.split(' ')
        row, col = pos.split(',')
        board[int(row)][int(col)] = piece
    return board

class TestKnightMoves(unittest.TestCase):
    def test_valid_moves(self):
        self.assertTrue(is_valid_knight_move((0, 0), (2, 1)))
        self.assertTrue(is_valid_knight_move((3, 3), (5, 4)))
        self.assertTrue(is_valid_knight_move((4, 4), (6, 3))) 
        self.assertTrue(is_valid_knight_move((7, 7), (5, 6)))

    def test_invalid_moves(self):
        self.assertFalse(is_valid_knight_move((0, 0), (1, 1)))
        self.assertFalse(is_valid_knight_move((3, 3), (4, 4))) 
        self.assertFalse(is_valid_knight_move((4, 4), (4, 5)))
        self.assertFalse(is_valid_knight_move((7, 7), (7, 6))) 

class TestRookMoves(unittest.TestCase):
    def test_horizontal_valid(self):
        board = generate_board(['w_r 4,3'])
        self.assertTrue(is_valid_rook_move(board, (4, 3), (4, 7))) 

    def test_vertical_valid(self):
        board = generate_board(['b_r 3,1'])
        self.assertTrue(is_valid_rook_move(board, (3, 1), (0, 1)))

    def test_horizontal_blocked(self):
        board = generate_board(['b_r 5,7', 'w_p 3,7'])
        self.assertFalse(is_valid_rook_move(board, (5, 7), (0, 7)))

    def test_vertical_blocked(self):
        board = generate_board(['w_r 6,4', 'w_p 4,4'])
        self.assertFalse(is_valid_rook_move(board, (6, 4), (1, 4)))

    def test_capture(self):
        board = generate_board(['w_r 3,2', 'b_n 6,2'])
        self.assertTrue(is_valid_rook_move(board, (3, 2), (6, 2)))

    def test_invalid_move(self):
        board = generate_board(['w_r 7,1'])
        self.assertFalse(is_valid_rook_move(board, (7, 1), (4, 4)))

class TestBishopMoves(unittest.TestCase):
    def test_valid_empty(self):
        board = generate_board(['b_b 0,0'])
        self.assertTrue(is_valid_bishop_move(board, (0, 0), (7, 7))) 

    def test_invalid(self):
        board = generate_board(['b_b 0,0'])
        self.assertFalse(is_valid_bishop_move(board, (0, 0), (7, 6)))

    def test_blocked(self):
        board = generate_board(['b_b 0,0', 'w_p 3,3'])
        self.assertFalse(is_valid_bishop_move(board, (0, 0), (7, 7)))

    def test_capture(self):
        board = generate_board(['b_b 0,0', 'w_p 7,7'])
        self.assertTrue(is_valid_bishop_move(board, (0, 0), (7, 7)))

class TestQueenMoves(unittest.TestCase):

    def test_valid_horizontal_move(self):
        """Test a valid horizontal queen move with no obstacles"""
        board = generate_board(['w_q 4,3'])  # Place only a white queen
        self.assertTrue(is_valid_queen_move(board, (4, 3), (4, 7))) 

    def test_valid_vertical_move(self):
        """Test a valid vertical queen move with no obstacles"""
        board = generate_board(['w_q 4,3'])
        self.assertTrue(is_valid_queen_move(board, (4, 3), (0, 3))) 

    def test_valid_diagonal_move(self):
        """Test a valid diagonal queen move with no obstacles"""
        board = generate_board(['w_q 4,3'])
        self.assertTrue(is_valid_queen_move(board, (4, 3), (1, 0))) 

    def test_invalid_blocked_move(self):
        """Test a move blocked by another piece"""
        board = generate_board(['w_q 4,3', 'b_p 4,5'])  # Add a blocking black pawn
        self.assertFalse(is_valid_queen_move(board, (4, 3), (4, 6)))  

    def test_invalid_non_linear_move(self):
        """Test a move that is not horizontal, vertical or diagonal """
        board = generate_board(['w_q 4,3'])
        self.assertFalse(is_valid_queen_move(board, (4, 3), (5, 5))) 

class TestCanCastleUnderAttack(unittest.TestCase):
    def test_long_castle_no_attackers(self):
        board = generate_board(['w_k 7,4'])  
        result = attack_stopping_castling(board, 'w', 'long')
        self.assertFalse(result) 

    def test_short_castle_no_attackers(self):
        board = generate_board(['w_k 7,4'])  
        result = attack_stopping_castling(board, 'w', 'short')
        self.assertFalse(result) 

    def test_long_castle_bishop_attack(self):
        board = generate_board(['w_k 7,4', 'b_b 6,4'])
        result = attack_stopping_castling(board, 'w', 'long')
        self.assertTrue(result)

    def test_short_castle_bishop_attack(self):
        board = generate_board(['w_k 7,4', 'b_b 6,4'])
        result = attack_stopping_castling(board, 'w', 'short')
        self.assertTrue(result)

    def test_short_castle_blocked_attack(self):
        board = generate_board(['w_k 7,4', 'b_r 1,5', 'w_p 6,5'])  # White pawn blocking the black rook's attack
        result = attack_stopping_castling(board, 'w', 'short')
        self.assertFalse(result)  # A blocked attack shouldn't prevent castling

    def test_short_castle_attack_next_to_king(self):
        board = generate_board(['w_k 7,4', 'b_b 5,5'])
        result = attack_stopping_castling(board, 'w', 'short')
        self.assertFalse(result)

    def test_short_castle_queen_attack(self):
        board = generate_board(['w_k 7,4', 'b_q 5,6'])
        result = attack_stopping_castling(board, 'w', 'short')
        self.assertTrue(result)

    def test_long_castle_rook_attack(self):
        board = generate_board(['w_k 7,4', 'b_r 5,3'])
        result = attack_stopping_castling(board, 'w', 'long')
        self.assertTrue(result)

    def test_short_castle_rook_attack(self):
        board = generate_board(['w_k 7,4', 'b_r 5,5'])
        result = attack_stopping_castling(board, 'w', 'short')
        self.assertTrue(result)

    def test_long_castle_knight_attack(self):
        tests = [(f'b_n {i},{j}') for i in range(5,7) for j in range(8)]
        for i, piece in enumerate(tests):
            board = generate_board(['w_k 7,4', piece])
            result = attack_stopping_castling(board, 'w', 'long')
            if i <= 7:
                if i % 8 in [1,2,3,4,5]:
                    self.assertTrue(result, f"Failed when {piece} attacks long castle")
                else:
                    self.assertFalse(result, f"Failed when {piece} doesn't attack long castle")
            else:
                if i % 8 in [0,1,2,4,5,6]:
                    self.assertTrue(result, f"Failed when {piece} attacks long castle")
                else:
                    self.assertFalse(result, f"Failed when {piece} doesn't attack long castle")


    def test_short_castle_knight_attack(self):
        tests = [(f'b_n {i},{j}') for i in range(5,7) for j in range(8)]
        for i, piece in enumerate(tests):
            board = generate_board(['w_k 7,4', piece])
            result = attack_stopping_castling(board, 'w', 'short')
            if i <= 7:
                if i % 8 in [3,4,5,6,7]:
                    self.assertTrue(result, f"Failed when {piece} attacks short castle")
                else:
                    self.assertFalse(result, f"Failed when {piece} doesn't attack short castle")
            else:
                if i % 8 in [2,3,4,6,7]:
                    self.assertTrue(result, f"Failed when {piece} attacks short castle")
                else:
                    self.assertFalse(result, f"Failed when {piece} doesn't attack short castle")    

    def test_short_castle_pawn_attack(self):
        tests = [(f'b_p 6,{i}') for i in range(8)]
        for i, piece in enumerate(tests):
            board = generate_board(['w_k 7,4', piece])
            result = attack_stopping_castling(board, 'w', 'short')
            if i in [3,4,5,6,7]:
                self.assertTrue(result, f"Failed when {piece} attacks short castle")
            else:
                self.assertFalse(result, f"Failed when {piece} doesn't attack short castle")

    def test_long_castle_pawn_attack(self):
        tests = [(f'b_p 6,{i}') for i in range(8)]
        for i, piece in enumerate(tests):
            board = generate_board(['w_k 7,4', piece])
            result = attack_stopping_castling(board, 'w', 'long')
            if i in [1,2,3,4,5]:
                self.assertTrue(result, f"Failed when {piece} attacks long castle")
            else:
                self.assertFalse(result, f"Failed when {piece} doesn't attack long castle")

    def test_short_castle_king_attack(self):
        tests = [(f'b_k 6,{i}') for i in range(8)]
        for i, piece in enumerate(tests):
            board = generate_board(['w_k 7,4', piece])
            result = attack_stopping_castling(board, 'w', 'short')
            if i in [3,4,5,6,7]:
                self.assertTrue(result, f"Failed when {piece} attacks short castle")
            else:
                self.assertFalse(result, f"Failed when {piece} doesn't attack short castle")

    def test_long_castle_king_attack(self):
        tests = [(f'b_k 6,{i}') for i in range(8)]
        for i, piece in enumerate(tests):
            board = generate_board(['w_k 7,4', piece])
            result = attack_stopping_castling(board, 'w', 'long')
            if i in [1,2,3,4,5]:
                self.assertTrue(result, f"Failed when {piece} attacks long castle")
            else:
                self.assertFalse(result, f"Failed when {piece} doesn't attack long castle")

if __name__ == '__main__':
    unittest.main()