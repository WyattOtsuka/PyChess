import copy

def is_valid_move(board, move, piece, is_white_turn, flip, en_passant_square, castling):
    start = move[0]
    end = move[1]

    if not is_move_on_board(start, end):
        return False

    # Check if the start square contains a piece of the current player's color
    if piece[0] == 'b' and is_white_turn:
        return False
    if piece[0] == 'w' and not is_white_turn:
        return False

    # Check if the end square is empty or contains a piece of the opposite color
    if board[end[0]][end[1]] == '' or board[end[0]][end[1]][0] != piece[0]:
        pass
    else:
        return False
    
    # Check if the piece is pinned
    if does_move_cause_check(board, start, end, is_white_turn, en_passant_square):
        return False

    # Check if the move is a valid move for the piece
    if piece[2] == 'p':
        return is_valid_pawn_move(board, start, end, is_white_turn, flip, en_passant_square)
    elif piece[2] == 'n':
        return is_valid_knight_move(start, end)
    elif piece[2] == 'b':
        return is_valid_bishop_move(board, start, end)
    elif piece[2] == 'r':
        return is_valid_rook_move(board, start, end)
    elif piece[2] == 'q':
        return is_valid_queen_move(board, start, end)
    elif piece[2] == 'k':
        return is_valid_king_move(board, start, end, castling)

    return False

def is_valid_pawn_move(board, start, end, is_white_turn, flip, en_passant_square):
    if end == en_passant_square:
        return True

    moving_down = is_white_turn == flip

    # Make sure the pawn is moving in the right direction
    if start[0] < end[0] and not moving_down or start[0] > end[0] and moving_down:
        return False

    # Check if the pawn is moving forward one or two squares
    if start[1] == end[1] and abs(start[0] - end[0]) == 1 and board[end[0]][end[1]] == '':
        return True
    if start[1] == end[1] and abs(start[0] - end[0]) == 2 and board[end[0]][end[1]] == '':
        if start[0] == 6 and not moving_down or start[0] == 1 and moving_down:
            return True
        else:
            return False

    # Check if the pawn is capturing diagonally
    if abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 1:
        # Make sure an enemy peice is there
        if board[end[0]][end[1]] != '' and (board[end[0]][end[1]][0] == 'b') == is_white_turn:
            return True
        else:
            return False

    return False

def is_valid_knight_move(start, end):
    # Check if the knight is moving in an L-shape
    if abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 1:
        return True
    if abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 2:
        return True

    return False

def is_valid_bishop_move(board, start, end):
    # Check if the bishop is moving diagonally
    if abs(start[0] - end[0]) == abs(start[1] - end[1]):
        # Check if the path is clear
        x_dir = 1 if end[0] > start[0] else -1
        y_dir = 1 if end[1] > start[1] else -1
        for i in range(1, abs(start[0] - end[0])):
            if board[start[0] + i * x_dir][start[1] + i * y_dir] != '':
                return False
        return True

    return False

def is_valid_rook_move(board, start, end):
    # Check if the rook is moving horizontally or vertically
    if start[0] == end[0] or start[1] == end[1]:
        # Check if the path is clear
        if start[0] == end[0]:
            dir = 1 if end[1] > start[1] else -1
            for i in range(1, abs(start[1] - end[1])):
                if board[start[0]][start[1] + i * dir] != '':
                    return False
        else:
            dir = 1 if end[0] > start[0] else -1
            for i in range(1, abs(start[0] - end[0])):
                if board[start[0] + i * dir][start[1]] != '':
                    return False
        return True

    return False

def is_valid_queen_move(board, start, end):
    # Check if the queen is moving horizontally, vertically, or diagonally
    if start[0] == end[0] or start[1] == end[1] or abs(start[0] - end[0]) == abs(start[1] - end[1]):
        # Check if the path is clear
        if start[0] == end[0]:
            dir = 1 if end[1] > start[1] else -1
            for i in range(1, abs(start[1] - end[1])):
                if board[start[0]][start[1] + i * dir] != '':
                    return False
        elif start[1] == end[1]:
            dir = 1 if end[0] > start[0] else -1
            for i in range(1, abs(start[0] - end[0])):
                if board[start[0] + i * dir][start[1]] != '':
                    return False
        else:
            x_dir = 1 if end[0] > start[0] else -1
            y_dir = 1 if end[1] > start[1] else -1
            for i in range(1, abs(start[0] - end[0])):
                if board[start[0] + i * x_dir][start[1] + i * y_dir] != '':
                    return False
        return True

    return False

def is_valid_king_move(board, start, end, castling):
    # Check if the king is moving one square in any direction
    if abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1:
        return True
    elif castling[0] and start[0] == end[0] and start[1] - 2 == end[1]:
        return True
    elif castling[1] and start[0] == end[0] and start[1] + 2 == end[1]:
        return True
    return False

def is_move_on_board(start, end):
    if end[0] > 7 or end[0] < 0 or end[1] > 7 or end[1] < 0 \
        or start[0] > 7 or start[0] < 0 or start[1] > 7 or start[1] < 0:
        return False
    return True


def is_capture(board, row, col, piece, start_row, start_col, en_passant_square):
    """
    Checks if a move to the given position would be a capture.

    Args:
        board (list): The current state of the board.
        row (int): The row of the position.
        col (int): The column of the position.
        piece (str): The piece making the move.
        start_row (int): The row of the starting position.
        start_col (int): The column of the starting position.

    Returns:
        bool: True if the move would be a capture, False otherwise.
    """

    # En Passant is always a capture
    if piece[2] == 'p' and en_passant_square == [row, col]:
        return True
    
    # Get the piece at the destination position
    destination_piece = board[row][col]

    # If there is no piece at the destination, it's not a capture
    if destination_piece == '':
        return False


    # If the piece at the destination has the same color as the moving piece, it's not a capture
    piece_color = piece[0]
    if destination_piece[0] == piece_color:
        return False

    # Check if the piece being moved is a pawn
    if piece[2] == 'p':
        # If the pawn is moving diagonally, it's a capture
        if abs(row - start_row) == 1 and abs(col - start_col) == 1:
            return True
        else:
            # If the pawn is moving forward, it's not a capture
            return False

    # If the piece at the destination has a different color than the moving piece, it's a capture
    return True

'''
** CASTLING **
'''

def can_castle(board, color, rook_a_moved, rook_h_moved):
    #TODO: convert to use find_all_attacking
    castling = [None, None]
    castling[0] = not rook_a_moved
    castling[1] = not rook_h_moved

    if not any(castling):
        return castling
    
    back_rank = 7 if color == 'w' else 0

    if board[back_rank][0] == '' or board[back_rank][0][2] != 'r':
        castling[0] = False
    if board[back_rank][7] == '' or board[back_rank][7][2] != 'r':
        castling[1] = False
    if not any(castling):
        return castling 
    
    if blocking_stopping_castling(board, color, 'long') or attack_stopping_castling(board, color, 'long'):
        castling[0] = False
    if not any(castling):
        return castling
    
    if blocking_stopping_castling(board, color, 'short') or attack_stopping_castling(board, color, 'short'):
        castling[1] = False
    return castling


def blocking_stopping_castling(board, color, direction):
    rank = 7
    if color == 'b':
        rank = 0

    # Check if any piece is in between the king and his rook
    if direction == 'long':
        for square in board[rank][1:4]:
            if square != '':
                return True
        return False
    else:
        for square in board[rank][5:7]:
            if square != '':
                return True
        return False


def attack_stopping_castling(board, color, direction):
    """
    Checks if there are any pieces that can attack the king during castling.

    Args:
        board (list): The current state of the board.
        color (str): The color of the king.
        direction (str): The direction of the castling ('long' or 'short').

    Returns:
        bool: True if there are any pieces that can attack the king during castling, False otherwise.
    """
    increment = -1 if color == 'w' else 1
    start_rank = 7 if color == 'w' else 0
    enemy_color = 'b' if color == 'w' else 'w'
    end_rank = 7 - start_rank


    if check_horizontal_attacks(board, start_rank, enemy_color, direction):
        return True

    if check_vertical_attacks(board, color, start_rank, increment, end_rank, direction):
        return True

    if check_diagonal_attacks(board, color, start_rank, increment, end_rank, direction):
        return True

    if check_knight_attacks(board, enemy_color, start_rank, increment, direction):
        return True

    if check_pawn_king_attacks(board, enemy_color, start_rank, increment, direction):
        return True 

    return False

# ----- Helper Functions -----

def check_horizontal_attacks(board, start_rank, enemy_color, direction):
    """Checks for a queen or rook on the back rank"""
    col = 4
    while col >= 0 and col <= 7:
        if board[start_rank][col] == enemy_color + '_q' or board[start_rank][col] == enemy_color + '_r':
            return True

        # We want to check that direction opposite the way we want to castle
        col = col + 1 if direction == 'long' else col - 1
    
def check_vertical_attacks(board, color, start_rank, increment, end_rank, direction):
    """Checks for attacks on the file the king passes through during castling"""
    # Check for attacks from queens
    col = 4
    while col >= 2 and col <= 6:
        for i in range(start_rank + increment, end_rank, increment):
            # Check if the first piece seen is an enemy rook or queen
            if board[i][col] != '':
                if board[i][col][0] != color and (board[i][col][2] == 'q' or board[i][col][2] == 'r'):
                    return True
                else:
                    break

        col = col - 1 if direction == 'long' else col + 1
                    
def check_diagonal_attacks(board, color, start_rank, increment, end_rank, direction):
    """Checks for diagonal attacks from bishops and queens"""
    col = 4
    while col >= 2 and col <= 6:
        right_blocked = False
        left_blocked = False
        for i in range(start_rank + increment, end_rank, increment):
            # Check if the first piece seen is an enemy bishop or queen:
            if not right_blocked and col - start_rank + i >= 0 and col - start_rank + i <= 7:
                if board[i][col - start_rank + i] != '':
                    if  board[i][col - start_rank + i][0] != color and (board[i][col - start_rank + i][2] == 'q' or board[i][col - start_rank + i][2] == 'b'):
                        return True
                    else:
                        right_blocked = True

            if not left_blocked and col + start_rank - i >= 0 and col + start_rank - i <= 7:
                if board[i][col + start_rank - i] != '':
                    if  board[i][col + start_rank - i][0] != color and (board[i][col + start_rank - i][2] == 'q' or board[i][col + start_rank - i][2] == 'b'):
                        return True
                    else:
                        left_blocked = True
            
            if right_blocked and left_blocked:
                break

        col = col - 1 if direction == 'long' else col + 1

def check_knight_attacks(board, enemy_color, start_rank, increment, direction):
    """Checks for attacking knights"""
    if direction == 'long':
        # Only a knight on 0, 1, 2, 4, 5, or 6 of second rank from end could stop a long castle
        curr_rank = start_rank + increment
        if enemy_color + '_n' in board[curr_rank][:3] or enemy_color + '_n' in board[curr_rank][4:7]: 
            return True

        # Checking knights on third to last rank
        curr_rank += increment
        if enemy_color + '_n' in board[curr_rank][1:6]:
            return True
    else:
        # Only a knight on  2, 3, 4, 6, or 7 of second rank from end could stop a short castle
        curr_rank = start_rank + increment  
        if enemy_color + '_n' in board[curr_rank][2:5] or enemy_color + '_n' in board[curr_rank][6:]:
            return True
        
        # Checkin knights on third to last rank
        curr_rank += increment
        if enemy_color + '_n' in board[curr_rank][3:]:
            return True

    return False

def check_pawn_king_attacks(board, enemy_color, start_rank, increment, direction):
    # TODO: Make this return the list of checking pieces. Add is in check func
    """Checks for attacking pawns and the opposing king """
    if direction == 'long':
        if enemy_color + '_p' in board[start_rank + increment][1:6] or enemy_color + '_k' in board[start_rank + increment][1:6]:
            return True
    else:
        if enemy_color + '_p' in board[start_rank + increment][3:] or enemy_color + '_k' in board[start_rank + increment][3:]:
            return True
        
    return False

'''
** ATTACKING **
'''

def find_all_attacking(board, attacked_row, attacked_col, is_white_turn, exit_early = False):
    attacking_pieces_positions = []

    row = None
    col = None
    enemy_color = 'b' if is_white_turn else 'w'
    
    # Queen Rook Bishop checks
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue

            row, col = first_piece_found(board, [attacked_row, attacked_col], [i, j])
            if row == None:
                continue

            if i != 0 and j != 0: # Diagonal, check for bishops and queens
                if board[row][col] == enemy_color + '_b' or board[row][col] == enemy_color + '_q':
                    attacking_pieces_positions.append([row, col])
                    
            else:
                if board[row][col] == enemy_color + '_r' or board[row][col] == enemy_color + '_q':
                    attacking_pieces_positions.append([row, col])

            if exit_early and len(attacking_pieces_positions) != 0:
                return attacking_pieces_positions

    # Knight attacks
    knight_moves = [[-1, -2], [-1, 2], [1, -2], [1, 2], [-2, -1], [-2, 1], [2, -1], [2, 1]]
    for move in knight_moves:
        if attacked_row + move[0] >=0 and attacked_row + move[0] <=7 and attacked_col + move[1] >=0 and attacked_col + move[1] <=7:
            if board[attacked_row + move[0]][attacked_col + move[1]] == enemy_color + '_n':
                attacking_pieces_positions.append([attacked_row + move[0], attacked_col + move[1]])
                if exit_early:
                    return attacking_pieces_positions
            
    # Pawn attacks
    pawns = []
    if is_white_turn:
        if attacked_row - 1 >= 0:
            if attacked_col + 1 <=7:
                pawns.append([attacked_row - 1, attacked_col + 1])
            if attacked_col - 1 >= 0:
                pawns.append([attacked_row - 1, attacked_col - 1])
    else:
        if attacked_row + 1 <= 7:
            if attacked_col + 1 <=7:
                pawns.append([attacked_row + 1, attacked_col + 1])
            if attacked_col - 1 >= 0:
                pawns.append([attacked_row + 1, attacked_col - 1])
    for pawn in pawns:
        if board[pawn[0]][pawn[1]] == enemy_color + '_p':
            attacking_pieces_positions.append([pawn[0], pawn[1]])
    
    return attacking_pieces_positions

def first_piece_found(board, start, direction):
    """
    Find the first piece in a given direction from a specific starting position on a chess board.

    Parameters:
    board (list): A 2D list representing the game board. Each element is either an empty string or a string representing a game piece.
    start (tuple): A tuple containing the row and column indices of the starting position on the board.
    direction (tuple): A tuple containing the row and column offsets for the direction to search.

    Returns:
    tuple: A tuple containing the row and column indices of the first piece found in the given direction. If no piece is found within 8 steps or if the search goes out of the board boundaries, returns (None, None).
    """
    
    new_row = start[0]
    new_col = start[1]
    for i in range(8):
        new_row += direction[0]
        new_col += direction[1]
        if new_row <= 7 and new_row >= 0 and new_col <= 7 and new_col >= 0:
            if board[new_row][new_col] != '':
                return new_row, new_col
        else:
            return None, None




def does_move_cause_check(board, start, end, is_white_turn, en_passant_square = None):
    if end == en_passant_square and board[start[0]][start[1]][2] == 'p':
        prev_piece = board[start[0]][end[1]]

        board[start[0]][end[1]] = ''
        board[end[0]][end[1]] = board[start[0]][start[1]]
        board[start[0]][start[1]] = ''

        ret = is_in_check(board, is_white_turn)

        board[start[0]][start[1]] = board[end[0]][end[1]]
        board[end[0]][end[1]] = ''
        board[start[0]][end[1]] = prev_piece
        
        return ret
    else:
        prev_piece = board[end[0]][end[1]]

        board[end[0]][end[1]] = board[start[0]][start[1]]
        board[start[0]][start[1]] = ''
        
        ret = is_in_check(board, is_white_turn)

        board[start[0]][start[1]] = board[end[0]][end[1]]
        board[end[0]][end[1]] = prev_piece
        return ret

def is_in_check(board, is_white_turn):
    king = 'w_k' if is_white_turn else 'b_k'
    row, col = find_king(board, king)
    checking_pieces = find_all_attacking(board, row, col, is_white_turn, True)
    return len(checking_pieces) >= 1

def is_mate(board, is_white_turn, en_passant_square):
    king = 'w_k' if is_white_turn else 'b_k'

    row, col = find_king(board, king)
    # Check if moving out of check is possible
    for x_del in [-1, 0, 1]:
        for y_del in [-1, 0, 1]:
            if y_del == 0 and x_del == 0:
                continue

            if not does_move_cause_check(board, [row, col], [row + x_del, col + y_del]):
                return False

    # First, find all attackers. If there's only 1, the attack can be stopped with a block or a capture
    attacking_pieces = find_all_attacking(board, row, col, is_white_turn)
    if len(attacking_pieces) == 1:
        # Check if the piece can be captured
        can_capture_checker = find_all_attacking(board, attacking_pieces[0][0], attacking_pieces[0][1], not is_white_turn)
        for position in can_capture_checker:
            if does_move_cause_check(board, position, attacking_pieces[0], not is_white_turn, en_passant_square):
                return False
            
        # Check if the piece can be blocked
        # If the piece is a pawn or knight, it cannot be blocked and is thus checkmate
        if attacking_pieces[0][2] == 'n' or attacking_pieces[0][2] == 'p':
            return True
        


    else:
        # Since a king move is invalid, a double check is checkmate
        return True

    # Check if the attack can be blocked (rook bishop queen)
        
        # If the attack is from a rook or queen, find the direction
    
        # If the attack is from a bishop or queen, find the direction
            
def find_king(board, king):
    for i, board_row in enumerate(board):
        if king in board_row:
            col = board_row.index(king)
            row = i
            return row, col
    
    return -1, -1
    