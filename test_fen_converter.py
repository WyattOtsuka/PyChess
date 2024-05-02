import unittest 
from fen_converter import board_to_fen, fen_to_board

class TestFenConverter(unittest.TestCase):
    def test_starting_position_to_fen(self):
        board = [
            ['b_r', 'b_n', 'b_b', 'b_q', 'b_k', 'b_b', 'b_n', 'b_r'],
            ['b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p'],
            ['w_r', 'w_n', 'w_b', 'w_q', 'w_k', 'w_b', 'w_n', 'w_r']
        ]
        self.assertTrue(board_to_fen(board) == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    def test_starting_position_to_board(self):
        expected_board = [
            ['b_r', 'b_n', 'b_b', 'b_q', 'b_k', 'b_b', 'b_n', 'b_r'],
            ['b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p'],
            ['w_r', 'w_n', 'w_b', 'w_q', 'w_k', 'w_b', 'w_n', 'w_r']
        ]
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

        actual_board = fen_to_board(fen)

        for expected_row, actual_row in zip(expected_board, actual_board):
            for expected_piece, actual_piece in zip(expected_row, actual_row):
                self.assertEqual(expected_piece, actual_piece)


if __name__ == '__main__':
    unittest.main()