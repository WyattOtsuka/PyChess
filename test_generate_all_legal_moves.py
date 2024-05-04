import move_generator
import fen_converter
import time

start_time = time.time()

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
    num_moves = 0
    if depth_to_go == 1:
        for square in squares_to_moves:
            num_moves += len(squares_to_moves[square])
            
            if print_nodes:
                for move in squares_to_moves[square]:
                    if print_fen:
                        print(f"{chr(97+int(square[2]))}{8-int(square[0])}{chr(97+int(move[1]))}{8-move[0]}: 1  --- {fen_converter.board_to_fen(board)} {'w' if color == 'b' else 'b'}")
                    else: 
                        print(f"{chr(97+int(square[2]))}{8-int(square[0])}{chr(97+int(move[1]))}{8-move[0]}: 1")
        return num_moves


    for square in squares_to_moves:
        # Make the move
        for move in squares_to_moves[square]:
            en_passant_square = None
            if board[int(square[0])][int(square[2])] != '' and board[int(square[0])][int(square[2])][2] == 'p' and abs(int(square[0]) - move[0]) == 2:
                en_passant_square = [(int(square[0]) + move[0]) // 2, move[1]]

            destination_piece = board[move[0]][move[1]]
            board[move[0]][move[1]] = board[int(square[0])][int(square[2])]
            board[int(square[0])][int(square[2])] = ''


            squares_to_moves_2 = move_generator.generate_all_legal_moves_for_color(board, 'w' if color == 'b' else 'b', en_passant_square=en_passant_square)
            new_move_count = calculate_moves(board, squares_to_moves_2, depth_to_go - 1, 'w' if color == 'b' else 'b')
            if print_nodes:
                if print_fen:
                   print(f"{chr(97+int(square[2]))}{8-int(square[0])}{chr(97+int(move[1]))}{8-move[0]}: {new_move_count}  --- {fen_converter.board_to_fen(board)} {'w' if color == 'b' else 'b'}")
                else:
                   print(f"{chr(97+int(square[2]))}{8-int(square[0])}{chr(97+int(move[1]))}{8-move[0]}: {new_move_count}")
                   
            num_moves += new_move_count

            board[int(square[0])][int(square[2])] = board[move[0]][move[1]]
            board[move[0]][move[1]] = destination_piece

    return num_moves

# print(calculate_moves(squares_to_moves, 3, color='w', print_nodes=True))

board_2, is_white_turn = fen_converter.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")

color = 'w' if is_white_turn else 'b'
squares_to_moves_2 = move_generator.generate_all_legal_moves_for_color(board_2, color)

print(calculate_moves(board_2, squares_to_moves_2, 4, color=color, print_nodes=False, print_fen=False))


print(f"Finished in {time.time()-start_time} s")