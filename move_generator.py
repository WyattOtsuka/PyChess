import move_checker

def generate_all_legal_moves_for_color(board, color, flip=False, en_passant_square=None, castling=None, exit_early=False):
    moves = {}
    is_white_turn = color == 'w'
    for row_idx, row in enumerate(board):
        for col_idx, square in enumerate(row):
            if square != '' and square[0] == color:
                moves[f"{row_idx},{col_idx}"] = generate_all_legal_moves_for_piece(board, row_idx, col_idx, is_white_turn, square, flip, en_passant_square, castling, exit_early)
    return moves


def generate_all_legal_moves_for_piece(board, row, col, is_white_turn, piece=None, flip=False, en_passant_square=None, castling=None, exit_early=False):
    if piece == None:
        piece = board[row][col]
    moves = generate_moves(board, row, col, piece, flip, en_passant_square, castling, exit_early)
    legal_moves = []
    for move in moves:
        if move_checker.is_valid_move(board, [[row, col], move], piece, is_white_turn, flip, en_passant_square):
            legal_moves.append(move)
    
    return legal_moves


def generate_moves(board, row, col, piece=None, flip=False, en_passant_square=None, castling=None, exit_early=False):
    if piece == None:
        piece = board[row][col]
    color = piece[0]
    piece_type = piece[2]

    if piece_type == 'p':
        return generate_pawn_moves(board, row, col, color, flip, en_passant_square)
    elif piece_type == 'r':
        return generate_rook_moves(board, row, col, exit_early)
    elif piece_type == 'n':
        return generate_knight_moves(board, row, col)
    elif piece_type == 'b':
        return generate_bishop_moves(board, row, col, exit_early)
    elif piece_type == 'q':
        return generate_queen_moves(board, row, col, exit_early)
    elif piece_type == 'k':
        if castling == None:
            raise Exception("Castling can't be none for king moves")
        return generate_king_moves(row, col, castling)


def build_moves(board, row, col, directions, exit_early):
    moves = []
    for direction in directions:
        for i in range(1, 8):
            new_row = row + direction[0] * i
            new_col = col + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if exit_early and board[new_row][new_col] != '':
                    moves.append([new_row, new_col])
                    break

                moves.append([new_row, new_col])
            else:
                break
    return moves

def generate_rook_moves(board, row, col, exit_early):
    return build_moves(board, row, col, [[0, 1], [0, -1], [1, 0], [-1, 0]], exit_early)

def generate_bishop_moves(board, row, col, exit_early):
    return build_moves(board, row, col, [[1, 1], [1, -1], [-1, 1], [-1, -1]], exit_early)

def generate_queen_moves(board, row, col, exit_early):
    return build_moves(board, row, col, [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]], exit_early)

def generate_pawn_moves(board, row, col, color, flip, en_passant_sqaure):
    moves = []
    if color == 'w' and not flip or (color != 'w' and flip):
        if row > 0:
            if row == 1:
                for piece in ["q", "r", "n", "b"]:
                    moves.append([row-1, col, piece])
            else:
                moves.append([row-1, col,])
                if row == 6 and board[row-2][col] == '' and board[row-1][col] == '':
                    moves.append([row-2, col])
        if col > 0 and board[row-1][col-1] != '' and board[row-1][col-1][0] == 'b':
            moves.append([row-1, col-1])
        if col < 7 and board[row-1][col+1] != '' and board[row-1][col+1][0] == 'b':
            moves.append([row-1, col+1])
    else:
        if row < 7:
            if row == 6:
                for piece in ["q", "r", "n", "b"]:
                    moves.append([row+1, col, piece])
            else:
                moves.append([row+1, col])
                if row == 1 and board[row+2][col] == '' and board[row+1][col] == '':
                    moves.append([row+2, col])
        if col > 0 and board[row+1][col-1] != '' and board[row+1][col-1][0] == 'w':
            moves.append([row+1, col-1])
        if col < 7 and board[row+1][col+1] != '' and board[row+1][col+1][0] == 'w':
            moves.append([row+1, col+1])

    if en_passant_sqaure != None and abs(en_passant_sqaure[0] - row) == 1 and abs(en_passant_sqaure[1] - col) == 1:
        moves.append(en_passant_sqaure)

    return moves

def generate_knight_moves(board, row, col):
    moves = []
    knight_moves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
    for move in knight_moves:
        new_row = row + move[0]
        new_col = col + move[1]
        if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            moves.append([new_row, new_col])
    return moves

def generate_king_moves(row, col, castling):
    moves = []
    king_moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for move in king_moves:
        new_row = row + move[0]
        new_col = col + move[1]
        if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            moves.append([new_row, new_col])

    if castling[0]:
        moves.append([row - 2, col])
    if castling[1]:
        moves.append([row + 2, col])

    return moves