import pygame
import sys
from move_checker import is_valid_move, is_capture, can_castle
from move_generator import generate_moves

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS
PIECE_FONT = pygame.font.Font(None, 40) 

# Set up the display
screen = pygame.display.set_mode((WIDTH + 100, HEIGHT))  # Add extra width for the button
pygame.display.set_caption('Chess')

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PURPLE = (102, 0, 204)
PINK = (255, 192, 203)  

class Board:

    def __init__(self):
        # Set up the font for the labels
        self.font = pygame.font.Font(None, 24)

        # Create the button
        self.button = pygame.Rect(WIDTH, HEIGHT // 2 - 25, 100, 50)
        pygame.draw.rect(screen, WHITE, self.button)
        self.flip_text = self.font.render("Flip", True, BLACK)
        screen.blit(self.flip_text, (WIDTH + 35, HEIGHT // 2 - 15))

        # True if playing as black
        self.flip_board = False

        # Starting chess position
        self.board = [
            ['b_r', 'b_q', '', '', 'b_k', '', '', 'b_r'],
            ['b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p'],
            ['w_r', 'b_q', '', '', 'w_k', '', '', 'w_r']
        ]

        standard_board = [
            ['b_r', 'b_n', 'b_b', 'b_q', 'b_k', 'b_b', 'b_n', 'b_r'],
            ['b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p', 'b_p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p', 'w_p'],
            ['w_r', 'w_n', 'w_b', 'w_q', 'w_k', 'w_b', 'w_n', 'w_r']
        ]
        self.is_white_turn = True
        self.dragging_piece = None
        self.previous_position = []
        self.last_pawn_move_double = None

        self.rook_b_a_moved = False
        self.rook_b_h_moved = False
        self.rook_w_a_moved = False
        self.rook_w_h_moved = False

    '''
    ** BOARD DRAW FUNCTIONS **
    '''
    def draw_squares(self, flip=False):
        """
        Draws the squares of the chessboard on the screen.

        Args:
            flip (bool, optional): Whether to flip the board. Defaults to False.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if flip:
                    color = WHITE if (row + COLS - col - 1) % 2 == 0 else BLACK
                else:
                    color = WHITE if (row + col) % 2 == 0 else BLACK

                if flip:
                    pygame.draw.rect(screen, color, ((COLS - col - 1) * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_labels(self, flip=False):
        """
        Draws the row and column labels on the chessboard.

        Args:
            flip (bool, optional): Whether to flip the board. Defaults to False.
        """
        for i in range(ROWS):
            label_color = BLACK if i % 2 == 0 else WHITE  
            label = self.font.render(str(ROWS - i), True, label_color)  
            if flip:
                screen.blit(label, (10, (ROWS - i - 1) * SQUARE_SIZE + 10)) 
            else:
                screen.blit(label, (10, i * SQUARE_SIZE + 10)) 

        for i in range(COLS):
            label_color = WHITE if i % 2 == 0 else BLACK  
            label = self.font.render(chr(ord('a') + i), True, label_color)  
            if flip:
                screen.blit(label, ((COLS - i - 1) * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 30)) 
            else:
                screen.blit(label, (i * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 30)) 

    def fix_label_colors(self, flip=False):
        """
        Fixes the colors of the row and column labels based on the current state of the board.

        Args:
            flip (bool, optional): Whether to flip the board. Defaults to False.
        """
        if flip:
            for i in range(ROWS):
                label_color = WHITE if i % 2 == 0 else BLACK  
                label = self.font.render(str(ROWS - i), True, label_color)  
                screen.blit(label, (10, (ROWS - i - 1) * SQUARE_SIZE + 10)) 

            for i in range(COLS):
                label_color = BLACK if i % 2 == 0 else WHITE  
                label = self.font.render(chr(ord('a') + i), True, label_color)  
                screen.blit(label, ((COLS - i - 1) * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 30)) 


    def draw_pieces(self, flip=False):
        """
        Draws the pieces on the chessboard based on the given board configuration.

        Args:
            board (list): A 2D list representing the chessboard, where each element is a string representing a piece or an empty square.
            flip (bool, optional): Whether to flip the board. Defaults to False.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != '':
                    if piece[0] == 'b':
                        piece_color = DARK_PURPLE
                    else:
                        piece_color = PINK

                    piece_label = PIECE_FONT.render(piece[2], True, piece_color)  
                    screen.blit(piece_label, (col * SQUARE_SIZE + SQUARE_SIZE // 2 - 10, row * SQUARE_SIZE + SQUARE_SIZE // 2 - 20)) 

    def draw_moves(self, row, col):
        """
        Draws semi-transparent circles on the board to represent possible moves
        for the piece at the given position.

        Args:
            board (list): The current state of the board.
            row (int): The row of the piece.
            col (int): The column of the piece.
        """
        # Calculate all possible moves for the piece
        possible_moves = generate_moves(self.board, row, col, self.dragging_piece, self.flip_board, self.last_pawn_move_double, castling)
        if self.dragging_piece[2] == 'k':
            color = self.dragging_piece[0]
            castling = can_castle(self.board, color, self.rook_b_a_moved, self.rook_b_h_moved)

            if color == 'b':
                rank = 0
            else:
                rank = 7

            if castling[0]:
                possible_moves.append([rank,2])
            if castling[1]:
                possible_moves.append([rank, 6])


        # Draw semi-transparent circles on the board to represent the possible moves
        for move in possible_moves:
            if is_capture(self.board, move[0], move[1], self.dragging_piece, self.previous_position[0], self.previous_position[1], self.last_pawn_move_double):
                # Draw a semi-transparent open circle for capture moves
                pygame.draw.circle(screen, (255, 0, 0), ((move[1] + 0.5) * SQUARE_SIZE, (move[0] + 0.5) * SQUARE_SIZE), SQUARE_SIZE // 2, 2)
            else:
                # Draw a semi-transparent closed circle for non-capture moves
                pygame.draw.circle(screen, (0, 255, 0), ((move[1] + 0.5) * SQUARE_SIZE, (move[0] + 0.5) * SQUARE_SIZE), SQUARE_SIZE // 2, 2)

    def draw_dragged_piece(self, event):
        """
        Draws the piece being dragged by the user.

        Args:
            event (pygame.event.Event): The mouse motion event.

        This function draws the piece at the current mouse position.
        """
        if self.dragging_piece is not None:
            if self.dragging_piece[0] == 'b':
                piece_color = DARK_PURPLE
            else:
                piece_color = PINK
            piece_label = PIECE_FONT.render(self.dragging_piece[2], True, piece_color)  
            screen.blit(piece_label, (event.pos[0] - 10, event.pos[1] - 15))
            self.draw_moves(self.previous_position[0], self.previous_position[1])

    def draw_board(self, flip=False):
        self.draw_squares(flip)
        self.draw_labels(flip)
        self.fix_label_colors(flip)
        self.draw_pieces(flip)

    def draw_screen(self):
        """
        Draws the entire screen.

        This function clears the screen, draws the flip board button, and draws the chessboard with pieces.
        """
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.button)
        screen.blit(self.flip_text, (WIDTH + 35, HEIGHT // 2 - 15))
        self.draw_board(self.flip_board)


    '''
    ** LOOP FUNCTIONS **
    '''
    def main_loop(self, ):
        """
        The main event loop of the game.

        This function handles all events, including quitting the game, mouse clicks, and drawing the screen.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
            self.draw_screen()
            self.draw_dragged_piece(event)

    # Event handlers
    def handle_mouse_down(self, event):
        """
        Handles mouse down events.

        Args:
            event (pygame.event.Event): The mouse down event.

        This function checks if the user clicked on the flip board button or a piece on the board. If a piece is clicked, it is picked up and removed from the board.
        """
        if self.button.collidepoint(event.pos):
            self.flip_board = not self.flip_board
            for i in range(len(self.board)):
                self.board[i].reverse()
            self.board.reverse()
        else:
            row = event.pos[1] // SQUARE_SIZE
            col = event.pos[0] // SQUARE_SIZE
            if self.board[row][col] != '':
                self.dragging_piece = self.board[row][col]
                self.previous_position = [row, col]
                self.board[row][col] = ''
                print(f"Picked up piece at ({row},{col})")

    def handle_mouse_up(self, event):
        """
        Handles mouse up events.

        Args:
            event (pygame.event.Event): The mouse up event.

        This function checks if the user was dragging a piece and places it back on the board at the new location.
        """
        if self.dragging_piece is not None:
            new_row = event.pos[1] // SQUARE_SIZE
            new_col = event.pos[0] // SQUARE_SIZE
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                move = [self.previous_position, [new_row, new_col]]
                valid_move = None

                # Only allow for one player to move pieces at a time
                if (self.dragging_piece[0] == 'w') != self.is_white_turn:
                    valid_move = False

                # Allow for castling
                if self.dragging_piece[2] == 'k' and valid_move == None:
                        if self.dragging_piece[0] == 'b':
                            castling = can_castle(self.board, self.dragging_piece[0], self.rook_b_a_moved, self.rook_b_h_moved)
                        else:
                            castling = can_castle(self.board, self.dragging_piece[0], self.rook_w_a_moved, self.rook_w_h_moved)

                        if new_col - self.previous_position[1] == -2 and castling[0]: # Long castle
                            self.board[new_row][0] = ''
                            self.board[new_row][3] = 'w_r' if self.is_white_turn else 'b_r'
                            valid_move = True
                        
                        elif new_col - self.previous_position[1] == 2 and castling[1]: # Short castle
                            self.board[new_row][7] = ''
                            self.board[new_row][5] = 'w_r' if self.is_white_turn else 'b_r'
                            valid_move = True

                if valid_move == None:
                    valid_move = is_valid_move(self.board, move, self.dragging_piece, self.is_white_turn, self.flip_board, self.last_pawn_move_double, castling)

                print(valid_move)
                if valid_move:
                    # En passant capture
                    if [new_row, new_col] == self.last_pawn_move_double:
                        self.board[new_row + 1 if self.last_pawn_move_double[0] == 2 else new_row - 1][new_col] = ''

                    # En passant check
                    if self.dragging_piece[2] == 'p' and abs(self.previous_position[0] - new_row) == 2:
                            self.last_pawn_move_double = [new_row + 1 if self.is_white_turn else new_row - 1, new_col]
                    else:
                        self.last_pawn_move_double = None

                    self.board[new_row][new_col] = self.dragging_piece
                    self.is_white_turn = not self.is_white_turn

                    # Handle castling checks
                    self.handle_rook_castling()     
                else:
                    self.board[self.previous_position[0]][self.previous_position[1]] = self.dragging_piece
            self.dragging_piece = None

    def handle_rook_castling(self):
        if self.previous_position == [0, 0]:
            self.rook_b_a_moved == True
        elif self.previous_position == [0, 7]:
            self.rook_b_a_moved
        elif self.previous_position == [0, 4]:
            self.rook_b_a_moved = True
            self.rook_b_h_moved = True

        elif self.previous_position == [7, 0]:
            self.rook_w_a_moved
        elif self.previous_position == [7, 7]:
            self.rook_w_h_moved
        elif self.previous_position == [7, 4]:
            self.rook_w_a_moved
            self.rook_w_h_moved

b = Board()
while True:
    b.main_loop()
    pygame.display.update() 

# TODO:
    # Pawn Promotions
    # Checks
        # Pinned Pieces    --- Done
        # Is king in check --- Done
        # Only valid move is to get king out of check else mate
    # Add in API for code to make a move