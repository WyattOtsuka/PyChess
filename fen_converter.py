
def board_to_fen(board):
    blank_space_count = 0
    fen_string = ""
    for idx, row in enumerate(board):
        for square in row:
            space_ascii = 0
            if square == '': 
                blank_space_count += 1
                continue
            elif blank_space_count != 0:
                fen_string += str(blank_space_count)
                blank_space_count = 0
            
            space_ascii = 0 if square[0] == 'b' else -32
            space_ascii += ord(square[2])
            fen_string += chr(space_ascii)

        if blank_space_count != 0:
            fen_string += str(blank_space_count)
            blank_space_count = 0
        if idx < 7:
            fen_string += '/'
    
    return fen_string

def fen_to_board(fen_string):
    fen_parts = fen_string.split(" ")

    is_white_turn = None
    if len(fen_parts) > 1:
        is_white_turn = fen_parts[1] == 'w'

    rows = fen_parts[0].split("/")
    board = []
    for row in rows:
        row_to_add = []
        for char in row:
            if char.isdigit():
                for _ in range(int(char)):
                    row_to_add.append('')
            elif ord(char) >= 96:
                row_to_add.append(f'b_{char}')
            else:
                row_to_add.append(f'w_{char.lower()}')
        board.append(row_to_add)
    
    return board, is_white_turn