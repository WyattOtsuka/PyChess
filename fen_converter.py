
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
