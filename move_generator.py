def generate_moves(board, row, col, piece=None, flip=False, en_passant_sqaure=None):
    if piece == None:
        piece = board[row][col]
    color = piece[0]
    piece_type = piece[2]

    if piece_type == 'p':
        return generate_pawn_moves(board, row, col, color, flip, en_passant_sqaure)
    elif piece_type == 'r':
        return generate_rook_moves(board, row, col)
    elif piece_type == 'n':
        return generate_knight_moves(board, row, col)
    elif piece_type == 'b':
        return generate_bishop_moves(board, row, col)
    elif piece_type == 'q':
        return generate_queen_moves(board, row, col)
    elif piece_type == 'k':
        return generate_king_moves(board, row, col)


def build_moves(board, row, col, directions):
    moves = []
    for direction in directions:
        for i in range(1, 8):
            new_row = row + direction[0] * i
            new_col = col + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                moves.append([new_row, new_col])
            else:
                break
    return moves

def generate_rook_moves(board, row, col):
    return build_moves(board, row, col, [[0, 1], [0, -1], [1, 0], [-1, 0]])

def generate_bishop_moves(board, row, col):
    return build_moves(board, row, col, [[1, 1], [1, -1], [-1, 1], [-1, -1]])

def generate_queen_moves(board, row, col):
    return build_moves(board, row, col, [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]])

def generate_pawn_moves(board, row, col, color, flip, en_passant_sqaure):
    moves = []
    if color == 'w' and not flip or (color != 'w' and flip):
        if row > 0:
            moves.append([row-1, col])
            if row == 6 and board[row-2][col] == '':
                moves.append([row-2, col])
        if col > 0 and board[row-1][col-1] != '' and board[row-1][col-1][0] == 'b':
            moves.append([row-1, col-1])
        if col < 7 and board[row-1][col+1] != '' and board[row-1][col+1][0] == 'b':
            moves.append([row-1, col+1])
    else:
        if row < 7:
            moves.append([row+1, col])
            if row == 1 and board[row+2][col] == '':
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

def generate_king_moves(board, row, col):
    moves = []
    king_moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for move in king_moves:
        new_row = row + move[0]
        new_col = col + move[1]
        if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            moves.append([new_row, new_col])
    return moves