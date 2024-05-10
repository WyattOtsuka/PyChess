import move_generator
import move_checker
import fen_converter
import time

start_time = time.time()

KING_FILE = 4
A_FILE = 0
H_FILE = 7

b_rook_a_moved = False
b_rook_h_moved = False
w_rook_a_moved = False
w_rook_h_moved = False

board_1 = [
    ['b_r', 'b_n', 'b_b', 'b_q', '', 'b_k', '', 'b_r'],
    ['b_p', 'b_p', '', 'w_p', 'b_b', 'b_p', 'b_p', 'b_p'],
    ['', '', 'b_p', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', 'w_b', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['w_p', 'w_p', 'w_p', '', 'w_k', 'b_k', 'w_p', 'w_p'],
    ['w_r', 'w_n', 'w_b', 'w_q', 'w_k', '', '', 'w_r']
]

starting_board = [
    ['b_r', 'b_n', 'b_b', 'b_q', 'b_k', 'b_b', 'b_n', 'b_r'],
    ['b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p'],
    ['w_r', 'w_n', 'w_b', 'w_q', 'w_k', 'w_b', 'w_n', 'w_r']
]

def calculate_moves(board, squares_to_moves, depth_to_go, color='b', print_nodes = False, print_fen = False):
    global w_rook_a_moved
    global w_rook_h_moved
    global b_rook_a_moved
    global b_rook_h_moved

    num_moves = 0
    if depth_to_go == 1:
        for square in squares_to_moves:
            num_moves += len(squares_to_moves[square])
            
            if print_nodes:
                for move in squares_to_moves[square]:
                    print_node(square, move, 1, board, color, print_fen)

        return num_moves

    for square in squares_to_moves:
        # Make the move
        for move in squares_to_moves[square]:
            rook_moved_status = {'w_rook_a_moved': w_rook_a_moved, 'w_rook_h_moved': w_rook_h_moved, 'b_rook_a_moved': b_rook_a_moved, 'b_rook_h_moved': b_rook_h_moved}
            en_passant_square, was_en_passant, was_castle, prev_rook_a_status, prev_rook_h_status, next_turn_castling, destination_piece = make_move(board, square, move, color, rook_moved_status)

            squares_to_moves_2 = move_generator.generate_all_legal_moves_for_color(board, opposite_color(color), en_passant_square=en_passant_square, castling=next_turn_castling, exit_early=True)
            new_move_count = calculate_moves(board, squares_to_moves_2, depth_to_go - 1, opposite_color(color))
            if print_nodes:
                print_node(square, move, new_move_count, board, color, print_fen)
                   
            num_moves += new_move_count

            if color == 'w':
                w_rook_h_moved = prev_rook_h_status
                w_rook_a_moved = prev_rook_a_status
            else:
                b_rook_a_moved = prev_rook_a_status
                b_rook_h_moved = prev_rook_h_status

            unmake_move(board, square, move, was_castle, was_en_passant, destination_piece)

    return num_moves

def unmake_move(board, start_square, move, was_castle, was_en_passant, destination_piece):
    if was_castle:
        board[move[0]][KING_FILE] = board[move[0]][move[1]]
        if move[1] == 6:
            board[move[0]][H_FILE] = board[move[0]][5]
            board[move[0]][5] = ''
        else:
            board[move[0]][A_FILE] = board[move[0]][3]
            board[move[0]][3] = ''

        board[move[0]][move[1]] = ''

    elif was_en_passant:
        board[int(start_square[0])][move[1]] = destination_piece
        board[int(start_square[0])][int(start_square[2])] = board[move[0]][move[1]]
        board[move[0]][move[1]] = ''

    else:
        if len(move) == 3:
            board[int(start_square[0])][int(start_square[2])] = board[move[0]][move[1]][:2] + "p"
        else:
            board[int(start_square[0])][int(start_square[2])] = board[move[0]][move[1]]
        board[move[0]][move[1]] = destination_piece

def make_move(board, start_square, move, color, rook_moved_status):
    en_passant_square = get_en_passant_square(board, start_square, move)
    was_en_passant, was_castle, destination_piece = move_piece(board, start_square, move)

    prev_rook_a_status, prev_rook_h_status = update_rook_status(rook_moved_status, color, move)
    next_turn_castling = get_next_turn_castling(board, opposite_color(color), rook_moved_status)

    return en_passant_square, was_en_passant, was_castle, prev_rook_a_status, prev_rook_h_status, next_turn_castling, destination_piece

def get_en_passant_square(board, start_square, end_square):
    if board[int(start_square[0])][int(start_square[2])] != '' and board[int(start_square[0])][int(start_square[2])][2] == 'p' and abs(int(start_square[0]) - end_square[0]) == 2:
        return [(int(start_square[0]) + end_square[0]) // 2, end_square[1]]
    else:
        return None

def move_piece(board, start_square, end_square):
    was_en_passant = False
    was_castle = False
    destination_piece = board[end_square[0]][end_square[1]]

    if board[int(start_square[0])][int(start_square[2])][2] == 'k' and abs(int(start_square[2]) - end_square[1]) == 2:
        was_castle = True
        if end_square[1] == 6:
            board[end_square[0]][(int(start_square[2]) + end_square[1]) // 2] = board[end_square[0]][H_FILE]
            board[end_square[0]][H_FILE] = ''

        if end_square[1] == 2:
            board[end_square[0]][(int(start_square[2]) + end_square[1]) // 2] = board[end_square[0]][A_FILE]
            board[end_square[0]][A_FILE] = ''

        board[end_square[0]][end_square[1]] = board[int(start_square[0])][int(start_square[2])]
        board[int(start_square[0])][int(start_square[2])] = ''

    elif board[int(start_square[0])][int(start_square[2])][2] == 'p' and abs(int(start_square[2]) - end_square[1]) == 1 and board[end_square[0]][end_square[1]] == '':
        was_en_passant = True
        board[end_square[0]][end_square[1]] = board[int(start_square[0])][int(start_square[2])]
        board[int(start_square[0])][end_square[1]] = ''
        board[int(start_square[0])][int(start_square[2])] = ''
        
    else:
        if len(end_square) == 3:
            board[end_square[0]][end_square[1]] = board[int(start_square[0])][int(start_square[2])][:2] + end_square[2]
        else:
            board[end_square[0]][end_square[1]] = board[int(start_square[0])][int(start_square[2])]
        board[int(start_square[0])][int(start_square[2])] = ''

    return was_en_passant, was_castle, destination_piece

def update_rook_status(rook_moved_status, color, end_square):
    prev_rook_a_status = None
    prev_rook_h_status = None

    if color == 'w':
        prev_rook_a_status = rook_moved_status['w_rook_a_moved']
        prev_rook_h_status = rook_moved_status['w_rook_h_moved']

        if end_square[0] == 7: # Check if it's on the back rank
            if end_square[1] == A_FILE:
                prev_rook_a_status = rook_moved_status['w_rook_a_moved']
                rook_moved_status['w_rook_a_moved'] = True

            elif end_square[1] == KING_FILE:
                prev_rook_a_status = rook_moved_status['w_rook_a_moved']
                rook_moved_status['w_rook_a_moved'] = True
                prev_rook_h_status = rook_moved_status['w_rook_h_moved']
                rook_moved_status['w_rook_h_moved'] = True

            elif end_square[1] == H_FILE:
                prev_rook_h_status = rook_moved_status['w_rook_h_moved']
                rook_moved_status['w_rook_h_moved'] = True
    else:
        prev_rook_a_status = rook_moved_status['b_rook_a_moved']
        prev_rook_h_status = rook_moved_status['b_rook_h_moved']

        if end_square[0] == 0: # Check if it's on the back rank
            if end_square[1] == A_FILE:
                prev_rook_a_status = rook_moved_status['b_rook_a_moved']
                rook_moved_status['b_rook_a_moved'] = True

            elif end_square[1] == KING_FILE: 
                prev_rook_a_status = rook_moved_status['b_rook_a_moved']
                rook_moved_status['b_rook_a_moved'] = True
                prev_rook_h_status = rook_moved_status['b_rook_h_moved']
                rook_moved_status['b_rook_h_moved'] = True

            elif end_square[1] == H_FILE:
                prev_rook_h_status = rook_moved_status['b_rook_h_moved']
                rook_moved_status['b_rook_h_moved'] = True

    return prev_rook_a_status, prev_rook_h_status

def get_next_turn_castling(board, color, rook_moved_status):
    if color == 'w':
        return move_checker.can_castle(board, color, rook_moved_status['w_rook_a_moved'], rook_moved_status['w_rook_h_moved'])
    else:
        return move_checker.can_castle(board, color, rook_moved_status['b_rook_a_moved'], rook_moved_status['b_rook_h_moved'])

def print_node(square, move, new_move_count, board, color, print_fen):
    move_to_print = f"{chr(97+int(square[2]))}{8-int(square[0])}{chr(97+int(move[1]))}{8-move[0]}"
    if len(move) == 3:
        move_to_print += move[2]

    if print_fen:
        print(f"{move_to_print}: {new_move_count}  --- {fen_converter.board_to_fen(board)} {opposite_color(color)}")
    else:
        print(f"{move_to_print}: {new_move_count}")

def opposite_color(color):
    if color == 'w':
        return 'b'
    else:
        return 'w'

def run_test():
    start_time = time.time()

    board_2, is_white_turn = fen_converter.fen_to_board("rnbq1k1r/pp1Pbppp/2p5/8/2B5/P7/1PP1NnPP/RNBQK2R b")

    color = 'w' if is_white_turn else 'b'

    castling = move_checker.can_castle(board_2, color, False, False)

    squares_to_moves_2 = move_generator.generate_all_legal_moves_for_color(board_2, color, castling=castling, exit_early=True)

    print(calculate_moves(board_2, squares_to_moves_2, 3, color=color, print_nodes=True, print_fen=False))

    print(f"Finished in {time.time()-start_time} s")


if __name__ == "__main__":
    run_test()