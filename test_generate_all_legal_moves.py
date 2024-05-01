import move_generator

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

squares_to_moves = move_generator.generate_all_legal_moves_for_color(board, 'w')

num_moves = 0
for square in squares_to_moves:
    num_moves += len(squares_to_moves[square])

print(num_moves)

def calculate_moves(squares_to_moves, depth_to_go, color='b'):
    num_moves = 0
    for square in squares_to_moves:
        # Make the move
        for move in squares_to_moves[square]:
            en_passant_square = None
            if board[int(square[0])][int(square[2])][2] == 'p' and abs(int(square[0]) - move[0]) == 2:
                en_passant_square = [(int(square[0]) + move[0]) // 2, move[1]]

            board[move[0]][move[1]] = board[int(square[0])][int(square[2])]
            board[int(square[0])][int(square[2])] = ''
            squares_to_moves_2 = move_generator.generate_all_legal_moves_for_color(board, color, en_passant_square=en_passant_square)

            if depth_to_go == 0:
                for square_2 in squares_to_moves_2:
                    num_moves += len(squares_to_moves_2[square_2])
            else:
                num_moves += calculate_moves(squares_to_moves_2, depth_to_go - 1, 'w' if color == 'b' else 'b')
            
            board[int(square[0])][int(square[2])] = board[move[0]][move[1]]
            board[move[0]][move[1]] = ''

    return num_moves

# print(calculate_moves(squares_to_moves, 0))
print(calculate_moves(squares_to_moves, 1)) 