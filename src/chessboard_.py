from chessboard_pieces      import *
from chessboard_scoreboard  import Scoreboard
from chessboard_history     import History
from chessboard_mini        import MiniChessboard
from typing                 import Literal, Union
from prettytable            import PrettyTable
import os

# SOME IMPORTANT VARIABLES
MAKE_RECORD_OF_MOVES_IN_OTHER_FILE = True   # Enables file recording
MOVES_HISTORY_PATH = 'moves_his.txt'        # Default file path
USER_COLOR_CHOICE  = 'white'                # user's color choice to compete with chess bot # 2nd option: 'black'
PLAYER_NAMES = { 
    'white': "Magnus Carlsen",
    'black': "Hikaru Nakamura"
}

# UI - Settings
UI_SETTINGS = {
    "Player's Name On Corner": True,
    "Display Colored Board": True,
}
R, G, B = (0 ,0, 0) # Adjust these values (r >= 60, g >= 20, b >= 80)

class ChessBoard: 
    tabular_history = PrettyTable(['Moves no.', 'Detailed Notation', 'Actual Notation', 'Move Type', 'Player'])
    score_board = Scoreboard()
    history = History()
    player_turn = 'white'
    no_turns = 0
    
    def __init__(self, board_notation='default',
             have_history: bool = True,
             have_score_board: bool = True):
        """ 
        ### Initialize the chessboard with a given board notation. ###

        #### Args: ####
            
        `board_notation (str, optional)`: Notation of the board. Defaults to 'default'.
            - 'default': The board will be initialized with a default chess setup.
            - 'e': An empty board will be initialized.
            - Other notations: The board will be initialized based on the given notation 
                (e.g., RNBQKBq1/PPP4P/3P2P1/5P2/2b1p3/8/pppp1ppp/rnb1k1nr for a custom configuration, 
                or 8/8/8/8/8/8/8/8 for a completely empty board).
            
        `have_history (bool, optional)`: Determines whether to maintain a history of moves.
            - If True, moves will be stored as tuples of the form `(start_position, end_position)`.
            - Defaults to True.
            
        `have_score_board (bool, optional)`: Determines whether to maintain a scoreboard.
            - If True, the scoreboard will track captured pieces and the capture scores for each player.
            - Defaults to True.
        """
        self.board = [[] for _ in range(8)]
        self.have_history = have_history
        self.have_score_board = have_score_board
        self.setup_notation(notations=board_notation)

    def print_board(self):
        """#### Print Chessboard Current State"""
        print(f"{f'[{PLAYER_NAMES[self.player_turn][0].upper()}]' if UI_SETTINGS["Player's Name On Corner"] else '   '}|a||b||c||d||e||f||g||h|")
        if not UI_SETTINGS["Display Colored Board"]:
            for i, row in enumerate(self.board):
                row_str = "".join(str(piece) for piece in row)
                print(f"{8 - i}--{row_str}")
        else:
            for i in range(8):
                print(f"{8 - i}--", end="")
                for j in range(8):
                    if (i + j) % 2 == 0:
                        # Dark square
                        print(f"\033[48;2;{40+R};{40+G};{40+B}m\033[38;2;255;255;255m{self.board[i][j]}\033[0m", end="")
                    else:
                        # Light square
                        print(f"\033[48;2;{100+R};{100+G};{100+B}m\033[38;2;255;255;255m{self.board[i][j]}\033[0m", end="")
                print()
    
    def change_player_turn(self):
        """
        #### Change the current player turn. #####
        """
        self.player_turn = 'white' if self.player_turn == 'black' else 'black'
        
    def place_pieces(self, lst: list[Union[Pawn, Knight, Bishop, Rook, Queen, King]]):
        """
        Place Pieces on the Board

        This function places chess pieces on the board based on their `position` attributes.

        Args:
            - `lst` (list): A list of chess piece objects. Each object should be an instance of a piece datatype 
            (e.g., `Pawn`, `Knight`, `Bishop`, `Rook`, `Queen`, `King`, `Empty`) with a `position` attribute.
            The `position` attribute specifies the piece's location on the board using chess notation 
            (e.g., "e8", "e2", "a1", etc.).

        Behavior:
            - Updates the board to reflect the placement of all pieces in the list.
            - Assumes all pieces have valid and non-conflicting positions.
        """
        for piece in lst:
            col = ord(piece.position[0]) - ord('a')
            row = 8 - int(piece.position[1])
            self.board[row][col] = piece
    
    def apply_history(self, mv_list: list, print_each_state=False, make_record=False):
        """
        Apply History of Moves

        This function applies a sequence of moves to the board, updating the game state accordingly.

        Args:
            - `mv_list (list)`: A list of moves represented as tuples of strings, in the format `(from, to)`.
            Each move indicates the starting and ending positions of a piece in standard chess notation 
            (e.g., `("e2", "e4")`).
            - `print_each_state (bool, optional)`: If `True`, prints the board state and additional information 
            after applying each move. Defaults to `False`.
            - `make_record (bool, optional)`: If `True`, adds the applied moves to the game's history record. 
            Defaults to `False`.

        Behavior:
            - Updates `self.board` for each move in `mv_list`.
            - Handles exceptions during move application and prints the error report along with the current move history.
            - Optionally prints each board state during the process if `print_each_state` is enabled.
            - Optionally updates the move history and tabular record if `make_record` is enabled.
            - Switches the player turn after each move.

        Additional Features:
            - If `MAKE_RECORD_OF_MOVES_ON_OTHER_FILE` is enabled, writes the complete move history to a file
            specified by `MOVES_HISTORY_PATH`.
            
        Example:
            ```
            cb = ChessBoard()
            cb.apply_history (
                [('e2', 'e4'), ('e7', 'e5'), ('d1', 'h5'), ('g7', 'g6'), ('h5', 'e5'),
                ('f8', 'e7'), ('e5', 'h8'), ('e7', 'f8'), ('h8', 'g8'), ('f7', 'f5'),
                ('f1', 'c4'), ('d7', 'd6'), ('g8', 'f7')],
                print_each_state=True,
                make_record=True,
                )
            ```
        """

        for mv in mv_list:
            try:
                note, d_n, a_n, m_t = self + mv
            except:
                print("ERR0R_REP0RT:",self.history)
            if print_each_state:
                self.clear_term()
                self.print_board()
                print(note)
                self.score_board.print()
                input("[Press enter to continue...]")
            if make_record:
                self.no_turns +=1
                self.tabular_history.add_row([self.no_turns, d_n, a_n, m_t, self.player_turn.title()])
            self.change_player_turn()
            
        if MAKE_RECORD_OF_MOVES_IN_OTHER_FILE:
            with open(MOVES_HISTORY_PATH, 'w') as f: f.write(str(self.tabular_history) + '\n')
        
        
    def setup_notation(self, notations: str='RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr'):
        """
        Set Up Chess Board Using FEN-Like Notation

        This method initializes the chessboard based on a string of notation that resembles FEN (Forsyth-Edwards Notation). 
        The notation specifies the arrangement of chess pieces and empty squares on the board.

        Args:
            - `notations (str, optional)`: A string describing the arrangement of pieces on the board.
            Defaults to the standard chess starting position:
            `'RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr'`.

            - Each row is separated by a `/`.
            - Uppercase letters (`R`, `N`, `B`, `Q`, `K`, `P`) represent black pieces.
            - Lowercase letters (`r`, `n`, `b`, `q`, `k`, `p`) represent white pieces.
            - Numbers (e.g., `8`) represent consecutive empty squares.

        Special Inputs:
            - `'e'`: Sets up an empty board (`8/8/8/8/8/8/8/8`).
            - `'default'`: Sets up the standard starting position.

        Behavior:
            - Clears the current board and initializes it with the specified setup.
            - Each piece is instantiated using its corresponding class (`King`, `Queen`, etc.).
            - Empty squares are represented by instances of the `Empty` class.
            - Each piece is assigned a `color` ('b' for black, 'w' for white) and a `position` in chess notation (e.g., `"e4"`).

        Implementation Details:
            - Ensures the board has exactly 8 rows and 8 columns, adding `Empty` pieces where necessary.
            - Positions are calculated using chess notation where rows range from `1` to `8` (bottom to top),
            and columns range from `a` to `h` (left to right).

        Example:
            ```python
            board = ChessBoard()
            
            # Sets up the board with the standard initial position.
            board.setup_notation('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
            board.print_board()
            
            # Sets up an empty board.
            board.setup_notation('e')
            board.print_board()
            ```
        """

        if notations == 'e':
            notations = '8/8/8/8/8/8/8/8'
        if notations == 'default':
            notations = 'RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr'
        
        piece_classes = {
            "K": King,
            "Q": Queen,
            "N": Knight,
            "B": Bishop,
            "R": Rook,
            "P": Pawn
        }
        notations = notations.strip().strip('/').split('/')
        
        # Clear the board and ensure exactly 8 rows
        self.board = [[] for _ in range(8)]
        
        for i, notation in enumerate(notations):
            row = []
            for j, not_ in enumerate(notation):
                # Place Black pieces
                if not_.isupper():
                    row.append(piece_classes[not_](color='b', position=f"{chr(ord('a') + j)}{8 - i}"))
                # Place White pieces
                elif not_.islower():
                    row.append(piece_classes[not_.upper()](color='w', position=f"{chr(ord('a') + j)}{8 - i}"))
                # Place Empty pieces (e.g., '8' represents 8 empty squares)
                elif not_.isdigit():
                    for c in range(int(not_)):
                        row.append(Empty(f"{chr(ord('a') + j)}{8 - i}"))
            
            # Ensure the row has exactly 8 columns
            while len(row) < 8:
                row.append(Empty(f"{chr(ord('a') + len(row))}{8 - i}"))
            
            self.board[i] = row  # Place the row in the board

    def setup_pieces(self, **cord_piece_pairs):
        """### Purpose of setup_pieces
        The function allows you to set up a customized board layout by placing specific pieces at specified coordinates. This is especially useful in scenarios such as:

        - Setting up custom board states (like puzzles or partial games).
        - Initializing non-standard chess games.
        - Testing specific configurations.
        
        #### Example: `ChessBoard(a5='Qb', a7='Pw', c2='Nw', c6='Rb', e4='Pb', e5='Kb', f4='Bb', f6='Pb', h3='Qw', h5='Kw'')`
        ##### Explaination notation:
        - `a5='Qb'`: A `black queen` (Qb) is `on square a5`.
        - `a7='Pw'`: A `white pawn` (Pw) is `on square a7`.
        - `c2='Nw'`: A `white Knight` (Nw) is `on square c2`.
        """
        # Mapping of piece type to class
        piece_classes = {
            "K": King,
            "Q": Queen,
            "N": Knight,
            "B": Bishop,
            "R": Rook,
            "P": Pawn
        }

        pieces = []
        for piece_cord, piece_type_color in cord_piece_pairs.items():
            piece_type, piece_color = piece_type_color[0].upper(), piece_type_color[1].lower()
            # Check if piece type exists in the mapping
            if piece_type in piece_classes:
                piece_class = piece_classes[piece_type]
                piece = piece_class(piece_color, piece_cord)
                pieces.append(piece)
        
        self.place_pieces(pieces)

    @property
    def board_notation(self):
        """
        Generate FEN-Like Board Notation

        This property generates and returns a string representing the current state of the chessboard 
        in a format similar to FEN (Forsyth-Edwards Notation). The notation describes the arrangement 
        of pieces and empty squares on the board.

        Returns:
            - `str`: A FEN-like string where:
                - Uppercase letters (`K`, `Q`, `N`, `B`, `R`, `P`) represent black pieces.
                - Lowercase letters (`k`, `q`, `n`, `b`, `r`, `p`) represent white pieces.
                - Digits represent consecutive empty squares.

        Behavior:
            - Iterates through each row of the board.
            - For each square:
                - If the square is empty, it increments the count of consecutive empty squares.
                - If the square contains a piece, it appends the corresponding piece notation 
                (based on the `piece_notations` mapping) to the string.
            - Appends a `/` at the end of each row (except the last one).
            - Strips trailing slashes from the final result.

        Notes:
            - This function assumes each `piece` on the board has attributes:
                - `ident`: A string identifying the piece type (e.g., 'King', 'Pawn').
                - `color`: A string representing the piece's color ('white' or 'black').
        """
        notation = '/'
        piece_notations = {
            'King': "K",
            'Queen': "Q",
            'Knight': "N",
            'Bishop': "B",
            'Rook': "R",
            'Pawn': "P",
        }
        
        for row in self.board:
            for piece in row:
                if isinstance(piece, Empty):
                    if notation[-1].isdigit():
                        notation = notation[:-1] + str(int(notation[-1]) + 1)
                    else:
                        notation += '1'
                    continue

                notation += piece_notations[piece.ident].lower() if piece.color == 'white' else piece_notations[piece.ident]
            notation += '/'
            
        return notation.strip('/')

    def piece_at(self, cord: str) -> Union[Pawn, Knight, Bishop, Rook, Queen, King, Empty, None_Piece]:
        """Gives Piece at Given Coordinates

        #### Args:
        - cord (str): Coordinates of Required Piece 

        #### Returns:
        - Union[Pawn, Knight, Bishop, Rook, Queen, King, Empty, None_piece]: Returns Piece as it
        """
        try:
            col = ord(cord[0]) - ord('a')
            row = 8 - int(cord[1])
            return self.board[row][col]
        except IndexError:
            return None_Piece()
    
    @staticmethod
    def filter_mv(cord: str) -> str:
        """#### Removes all decorations from only one coordinate

        #### Args:
        - cord (str): Coordinate with or without decoration

        #### Returns:
        - str: Coordinate without decoration
        """
        if len(cord) == 2:
            return cord
        elif len(cord) == 4:
            return cord[1:3]
        elif len(cord) == 3:
            return cord[:-1]
    
    def filter_moves(self, list_of_moves: list[str], merged: bool = False) -> list[str]:
        """#### Removes all decorations from list of coordinates and categorize them into 3lists
        `[ie. Normal, Attacking, Special]`

        #### Args:
        - cord (list[str]): List of Coordinates with or without decorations
        - merged (bool, [Optional]): When Only One Combined List requires

        #### Returns:
        - list[str]: List of Coordinate without decoration
        """
        normal, attack, special = [], [], []
        
        for mv in list_of_moves:
            if len(mv) == 2:
                normal.append(mv)
            elif len(mv) == 4:
                if mv.startswith("<") and mv.endswith(">"):
                    attack.append(self.filter_mv(mv))
                elif mv.startswith("|") and mv.endswith("|"):
                    special.append(self.filter_mv(mv))
            else:
                special.append(self.filter_mv(mv))

        if merged:
            return sorted(set(normal + attack + special))
        else:
            return sorted(set(normal)), sorted(set(attack)), sorted(set(special))

    def is_mv_safe_for_king(self, cords: tuple[str] = tuple()) -> bool:
        """Try the given move in imaginary chess board and returns true flse

        #### Args:
        - cords (tuple[str], optional): Tuple of coordinate to check or Empty to check based on current state of Chessboard. Defaults to tuple().

        #### Returns:
        - bool: is king safe or not
        """
        return MiniChessboard(board_not=self.board_notation).is_king_safe(self.player_turn, cords)
                  
    def get_valid_mv(self,  position: str, deco: bool = True) -> list[str]:
        """Generate `list of All Valid Moves` with some `Decorations`
        
        #### Args:
        - position (str): Postion of piece whose moves are reqiured
        - deco (bool, [optional]): Add `Decorations`. Defaults to True.

        #### Decorations:
        -  __   : For Normal moves    [Eg. e4  ]
        - <__>  : For Attacking moves [Eg. <d5>]
        - |__|  : For Castling moves  [Eg. |g1|]
        -  __'  : For EnPassing moves [Eg. <d5>]
        #### Returns:
        - list[str]: List of all moves
        """
        if any(isinstance(position, kind) for kind in [Pawn, Knight, Bishop, Rook, Queen, King]):
            position = position.position

        C, N = ord(position[0]), int(position[1])
        
        moves_lst = []
        for cons_steps in self.piece_at(position).steps:
            for step in cons_steps:
                new_c = chr(C + step[0])
                new_n = N + step[1]
                if  1 <= new_n <= 8 and  'a' <= new_c <= 'h':
                    if isinstance(self.piece_at(f"{new_c}{new_n}"), Empty):
                        if self.is_mv_safe_for_king((position, f"{new_c}{new_n}")):
                            if isinstance(self.piece_at(position), Pawn):
                                if new_c == chr(C):
                                    moves_lst.append(f"{new_c}{new_n}")
                                continue
                            moves_lst.append(f"{new_c}{new_n}")
                    elif self.piece_at(f"{new_c}{new_n}").color !=  self.piece_at(position).color:
                        if isinstance(self.piece_at(position), Pawn) and new_c == chr(C):
                            continue
                        if self.is_mv_safe_for_king((position, f"{new_c}{new_n}")):
                            moves_lst.append(f"<{new_c}{new_n}>" if  deco else f"{new_c}{new_n}")
                        break
                    else:
                        break
        # Adds  castling moves FOR  KING ONLY
        if isinstance(self.piece_at(position), King):
            # Check if the king has not moved
            if not self.piece_at(position).is_king_moved:
                
                # Queenside castling (left side of the board for white)
                for i in range(-3, 0, 1):
                    new_c = chr(C + i)
                    if isinstance(self.piece_at(f"{new_c}{N}"), Empty):
                        if f"{new_c}{N}" in MiniChessboard(board_not=self.board_notation).get_pseudo_legal_mvs(target_player=-self.piece_at(position)):
                            break
                        continue
                    else:
                        break
                else:
                    if isinstance(self.piece_at(f"{chr(C - 4)}{N}"), Rook) and not self.piece_at(f"{chr(C - 4)}{N}").is_rook_moved:
                        moves_lst.append(f"|{chr(C - 2)}{N}|" if  deco else f"{new_c}{new_n}")
                
                # Kingside castling (right side of the board for white)
                for i in range(1, 3):
                    new_c = chr(C + i)
                    if isinstance(self.piece_at(f"{new_c}{N}"), Empty):
                        if f"{new_c}{N}" in MiniChessboard(board_not=self.board_notation).get_pseudo_legal_mvs(target_player=-self.piece_at(position)):
                            break
                        continue
                    else:
                        break
                else:
                    # Check if the rook on the kingside has not moved and is in the correct position
                    if isinstance(self.piece_at(f"{chr(C + 3)}{N}"), Rook) and not self.piece_at(f"{chr(C + 3)}{N}").is_rook_moved:
                        moves_lst.append(f"|{chr(C + 2)}{N}|" if  deco else f"{new_c}{new_n}")

        if isinstance(self.piece_at(position), Pawn):
            player = self.piece_at(position).color
            (from_num, to_num) = ("5", "6") if player == "white" else ("4", "3")
            
            if self.piece_at(position).position[1] == from_num:
                for dir in [-1, 1]:
                    new_c = chr(C + dir)
                    adjacent_piece = self.piece_at(f"{new_c}{from_num}")
                    if adjacent_piece.ident:
                        if adjacent_piece.color != player and isinstance(adjacent_piece, Pawn) and adjacent_piece.is_in_doip:
                            if isinstance(self.piece_at(f"{new_c}{to_num}"), Empty):
                                if self.is_mv_safe_for_king((position, f"{new_c}{new_n}")):
                                    moves_lst.append(f"{new_c}{new_n}'" if  deco else f"{new_c}{new_n}")

        for move in moves_lst:
            mv= self.filter_mv(move)
            if not self.is_mv_safe_for_king((position,mv)):
                moves_lst.remove(move)
        return moves_lst

    def n(self, cord:  str) -> str:
        """`Notation of an Piece`

        #### Args:
        - cord (str): Cordinate of Pieces

        #### Returns:
        - str: The String of their notations 
        """
        pc = self.piece_at(cord)
        if  isinstance(pc, Empty): return ""
        elif isinstance(pc, Pawn): return "P"
        elif isinstance(pc, Knight): return "N"
        elif isinstance(pc, Bishop): return "B"
        elif isinstance(pc, Rook): return "R"
        elif isinstance(pc, Queen): return "Q"
        elif isinstance(pc, King): return "K"
    
    def find_all_piece(self, prop: Union[str, list, tuple]=['King', 'black'], first_occurence: bool = False) ->\
        list[Union[Pawn, Knight, Bishop, Rook, Queen, King, Empty, None_Piece]]:
        """Returns All the list of `Pieces` on Chessboard that satisfies Given Properties
        #### Args:
        - prop: Property(ies) of Pieces
        - first_occurence(bool, [Optional]): To Return Piece on it's first occurence otherwise list
        """
        lst = []
        for i in range(0, 8):
            for j in range(1, 9):
                c = chr(ord('a') + i)
                n = str(j)
                piece_properties = self.piece_at(f"{c}{n}").define_coor()

                if isinstance(prop, (tuple, list)):
                    # Ensure all properties are satisfied
                    if all(p in piece_properties for p in prop):
                        if first_occurence: 
                            return self.piece_at(f"{c}{n}")
                        lst.append(self.piece_at(f"{c}{n}"))
                else:
                    # If single property, check it
                    if prop in piece_properties:
                        if first_occurence:
                            return self.piece_at(f"{c}{n}")
                        lst.append(self.piece_at(f"{c}{n}"))
        return lst
        
    def reset_pawns(self, new_pos: str):
        for pawn in self.find_all_piece("Pawn"):
            if pawn.position != new_pos:
                pawn + "x"
                
    def __add__(self, cords: tuple[str, str]) -> str:
        """
        Make Moves Using the '+' Operator

        This method allows chess moves to be performed using the `+` operator. It handles all types of chess moves, 
        including normal moves, attacks, promotions, castling, and en passant.

        Args:
            cords (tuple[str, str]): A tuple of coordinates in the format (from_square, to_square), 
                                    where each square is represented as a string (e.g., "e2", "e4").

        Returns:
            str: A descriptive string providing information about the move made. The returned string varies based 
                on the type of move performed, or provides an error message for invalid moves.

        Move Types Handled:
        - **Promotion**: Handles pawn promotion when the destination square includes an "=" followed by the 
        desired piece (e.g., "e8=Q" for promoting to a queen).
        - **En Passant**: Allows en passant captures by pawns.
        - **Castling**: Supports both kingside and queenside castling.
        - **Normal Moves**: Handles standard piece movement or attacks.
        - **Invalid Moves**: Returns an error message for moves that violate chess rules.

        Side Effects:
        - Updates the board state by moving the pieces.
        - Adjusts internal attributes like the piece's position and history if `self.have_history` is enabled.
        - Handles pawn promotion and resetting en passant flags for pawns.
        - Updates the score board (if enabled) when pieces are captured.

        Examples:
            ```python
            # Normal move
            board + ("e2", "e4")
            # Attack move
            board + ("e2", "e4") # Not <e4>
            # Castling (Kingside)
            board + ("e1", "g1") # NOT |g1|
            # En Passant
            board + ("e5", "d6") # NOT d6'
            # Promotion
            board + ("e7", "e8=Q")
            ```

        Notes:
            - This method assumes the existence of several helper methods and attributes:
                - `piece_at()`: Retrieves the piece at a given position.
                - `place_pieces()`: Places or replaces pieces on the board.
                - `reset_pawns()`: Resets pawn-specific attributes.
                - `self.history`: Tracks move history if enabled.
                - `self.have_score_board`: Checks whether a scoring system is active.
                - `MiniChessboard`: Used to validate king safety.
        """

        prev, new_pos = cords
        piece_f, piece_t = self.piece_at(prev), self.piece_at(new_pos)
        a_n, d_n, m_t = '', '', ''

        # Handle promotion case
        if "=" in new_pos:
            pos_w_choice = new_pos
            new_pos, choice = new_pos.split("=")
            new_pos = new_pos.strip().lower()
            choice = choice.strip().upper()
            piece_t = self.piece_at(new_pos)
            if self.have_history is True: self.history + (cords[0], f"{new_pos} ={choice}")
            
            d_n = f"P{prev} to {self.n(new_pos)}{new_pos}"
            self.place_pieces([Empty(piece_f.position)])
            
            promoted_piece = piece_f + pos_w_choice
            self.place_pieces([promoted_piece or piece_f])

            if isinstance(piece_t, Empty):
                note = f"{piece_f.symbol}, {prev}) moved to ({piece_t.symbol}, {new_pos})."
                a_n, m_t = f"P{new_pos} ={choice}", "Promotion"
            else:
                if self.have_score_board: note = self.score_board + piece_t
                else: note=''
                a_n, m_t = f"Px{new_pos} ={choice}", "Attack & Promotion"
            
            self.reset_pawns(new_pos)
            a_n += '+' if not MiniChessboard(board_not=self.board_notation).is_king_safe() else ''
            return note, d_n, a_n, m_t

        # Handle en passant
        if isinstance(piece_f, Pawn):
            from_num, to_num = ("5", "6") if piece_f.color == "white" else ("4", "3")
            if piece_f.position[1] == from_num and new_pos[1] == to_num:
                for dir in [-1, 1]:
                    adj_pos = f"{chr(ord(prev[0]) + dir)}{from_num}"
                    adjacent_piece = self.piece_at(adj_pos)
                    if isinstance(adjacent_piece, Pawn) and adjacent_piece.is_in_doip:
                        m_t = "In Passing"
                        self.place_pieces([Empty(adj_pos), Empty(prev)])
                        piece_f + new_pos
                        self.place_pieces([piece_f])
                        if self.have_score_board: self.score_board + adjacent_piece

                        if self.have_history is True: self.history + cords
                        self.reset_pawns(new_pos)
                        d_n, a_n = f"{self.n(piece_f.position)}{prev} ~ {self.n(piece_t.position)}{new_pos}", f"{prev[0]}x{new_pos} e.p."
                        a_n += '+' if not MiniChessboard(board_not=self.board_notation).is_king_safe() else ''
                        return f"En passant: {piece_f.symbol} moved to {new_pos}.", d_n, a_n, m_t

        # Handle castling
        if isinstance(piece_f, King) and not piece_f.is_king_moved:
            C_prev, C_new = ord(prev[0]), ord(new_pos[0])
            if abs(C_new - C_prev) == 2:  # Castling move
                if C_new > C_prev:  # Kingside
                    a_n, m_t = "O-O", "K-Side Castling"
                    rook_pos, new_rook_pos = f"{chr(C_prev + 3)}{prev[1]}", f"{chr(C_new - 1)}{new_pos[1]}"
                else:  # Queenside
                    a_n, m_t = "O-O-O", "Q-Side Castling"
                    rook_pos, new_rook_pos = f"{chr(C_prev - 4)}{prev[1]}", f"{chr(C_new + 1)}{new_pos[1]}"

                rook_piece = self.piece_at(rook_pos)
                if isinstance(rook_piece, Rook) and not rook_piece.is_rook_moved:
                    self.place_pieces([Empty(prev), Empty(rook_pos)])
                    piece_f + new_pos
                    rook_piece + new_rook_pos
                    self.place_pieces([piece_f, rook_piece])
                    
                    self.reset_pawns(new_pos)
                    if self.have_history is True: self.history + cords
                    a_n += '+' if not MiniChessboard(board_not=self.board_notation).is_king_safe() else ''
                    return f"King castled to {new_pos} with rook at {new_rook_pos}.", d_n, a_n, m_t

        # Normal move
        if isinstance(piece_f, Empty):
            return "Invalid Move! That spot does not contain any piece."
        if piece_f.color in ["white", "black"]:
            if isinstance(piece_t, Empty) or piece_f.color != piece_t.color:
                d_n = f"{self.n(piece_f.position)}{piece_f.position} to {self.n(new_pos)}{new_pos}"
                a_n = f"{self.n(piece_f.position)}{new_pos}"
                m_t = "Normal"
                self.place_pieces([Empty(piece_f.position)])
                
                promoted_piece = piece_f + new_pos  # Move to new position, check for promotion
                self.place_pieces([promoted_piece or piece_f])

                if isinstance(piece_t, Empty):
                    note = f"{piece_f.symbol}, {prev}) moved to ({piece_t.symbol}, {new_pos})."
                else:
                    if self.have_score_board: note = self.score_board + piece_t
                    else: note = ''
                    a_n = f"{self.n(piece_f.position)}x{piece_t.position}"
                    m_t = "Attack"
                
                if promoted_piece:
                    a_n = f"Px{piece_t.position} ={self.n(promoted_piece.position)}"
                    m_t = "Attack & Promotion" if m_t == "Attack" else "Promotion"
                    if self.have_history is True: self.history + (prev, new_pos + f" ={self.n(promoted_piece.position)}")
                else:
                    if self.have_history is True: self.history + cords

                self.reset_pawns(new_pos)
                a_n += '+' if not MiniChessboard(board_not=self.board_notation).is_king_safe() else ''
                return note, d_n, a_n, m_t
            else:
                return "You cannot capture your own pieces."

        return "<------ Invalid Move ----->"
        
    def get_from_position(self) -> str:
        """Get `From square` from User 

        #### Returns:
        - str: From square coordinate
        """
        bgRed = "\033[1m\033[3m\033[48;2;244;146;130m\033[38;2;60;60;60m"
        bgYel = "\033[1m\033[3m\033[48;2;234;200;130m\033[38;2;60;60;60m"
        bgGrn = "\033[1m\033[3m\033[48;2;138;234;146m\033[38;2;60;60;60m"
        r = "\033[0m"
        while True:
            frm = input("Enter the square of the piece `from` which to move: ").strip()
            
            if frm == "--cmd":
                return frm
            
            if len(frm) == 2 and frm[0].isalpha() and frm[1].isdigit():
                c, n = frm[0], int(frm[1])
                if 'a' <= c <= 'h' and 1 <= n <= 8:
                    if self.piece_at(frm).color == self.player_turn.lower():
                        valid_moves = self.get_valid_mv(frm)
                        if valid_moves:
                            print(f"|{bgGrn}Recommended Moves for {self.piece_at(frm).ident} [{frm},{self.piece_at(frm).symbol[1]} ]:{r+bgYel} {', '.join(valid_moves)} {r}|")
                            return frm
                        print(f"|{bgRed}ZERO_MOVES:{r+bgYel} No valid moves for the selected piece.{r}|")
                    else:
                        print(f"|{bgRed}WRONG_COLOR:{r+bgYel} You selected the wrong color piece.{r}|")
                else:
                    print(f"|{bgRed}INVALID_INPUT:{r+bgYel} Invalid square coordinates.{r}|")
            else:
                print(f"|{bgRed}INVALID_INPUT:{r+bgYel} Square notation should be a letter (a-h) followed by a number (1-8).{r}|")
            if '--' in frm or all(f in "--cmd" for f in frm):
                print(f"\n|{bgGrn}Do you mean {bgYel}'--cmd'?{r}|")
                
    def get_destinations(self) -> tuple[str]:
        """Get `To square` from User and also `From square` coodinates using `.get_from_position()` method

        #### Returns:
        - tuple[str]: `Tuple of from and to squares` coordinates
        """
        bgRed = "\033[1m\033[3m\033[48;2;244;146;130m\033[38;2;60;60;60m"
        bgYel = "\033[1m\033[3m\033[48;2;234;200;130m\033[38;2;60;60;60m"
        bgGrn = "\033[1m\033[3m\033[48;2;138;234;146m\033[38;2;60;60;60m"
        r = "\033[0m"

        from_sq = self.get_from_position()
        if "--cmd" == from_sq:
            return from_sq
        
        valid_moves = self.get_valid_mv(from_sq)
        note = f"|{bgGrn}Recommended Moves for {self.piece_at(from_sq).ident} [{from_sq},{self.piece_at(from_sq).symbol[1]} ]:{r+bgYel} {', '.join(valid_moves)} {r}|"
        
        valid_moves = self.filter_moves(valid_moves, True)
        
        while True:
            to_sq_with_choice = ""
            to_sq = input("Enter the square to move the piece `to`: ").strip()
            if to_sq == "--cmd":
                return to_sq

            # Handle pawn promotion (e.g., a8=Q)
            if "=" in to_sq:
                to_sq_with_choice = to_sq
                to_sq, choice = to_sq.split("=")
                to_sq = to_sq.strip()
                choice = choice.strip().upper()

                if choice not in ["Q", "R", "B", "N"]:
                    print(f"|{bgRed}INVALID_INPUT:{r+bgYel} Invalid choice. Please choose one of the following: Q, R, B, N.{r}|\nFor example: {to_sq}=Q")
                    continue

            # Validate that the input is in the correct form (e.g., "e4")
            if len(to_sq) == 2:
                column, row = to_sq[0], to_sq[1]

                if column.isalpha() and 'a' <= column <= 'h':
                    if row.isdigit() and 1 <= int(row) <= 8:
                        # If valid, check if it's one of the recommended moves
                        if to_sq in valid_moves:
                            if "=" in to_sq_with_choice:
                                return (from_sq, to_sq_with_choice)
                            return (from_sq, to_sq)
                        else:
                            print(f"|{bgRed}INVALID_MOVE:{r+bgYel} Choose another destination square from the recommended moves.{r}|")
                            print(note)
                    else:
                        print(f"|{bgRed}INVALID_INPUT:{r+bgYel} Invalid row number (must be between 1 and 8).{r}|")
                else:
                    print(f"|{bgRed}INVALID_INPUT:{r+bgYel} Invalid column (must be a letter from 'a' to 'h').{r}|")
            else:
                print(f"|{bgRed}INVALID_INPUT:{r+bgYel} Square notation should be a letter followed by a number (e.g., 'e4').{r}|")
    
            if any(l in to_sq for l in ['<', '>', "'", "|"]):
                print(f"\n|{bgGrn}Note:{r+bgYel} You don't have to put {'<', '>', "'", "|"} in your input.{r}|\n")
                
            if '--' in to_sq or all(f in "--cmd" for f in to_sq):
                print(f"\n|{bgGrn}Do you mean {bgYel}'--cmd'?{r}|")
                
    def find_all_cords(self, prop: Union[str, list, tuple]=['King', 'black'], first_occurence: bool = False) -> list[str]:
        """Returns All the list of `Coordinate` of pieces on Chessboard that satisfies Given Properties
        #### Args:
        - `prop`: Property(ies) of Pieces
        - `first_occurence`(bool, [Optional]): To Return Piece on it's first occurence otherwise list
        #### Returns:
        - `List[str]` on True OR `str` on False of `first_occurence`
        """
        lst = []
        for i in range(0, 8):
            for j in range(1, 9):
                c = chr(ord('a') + i)
                n = str(j)
                piece = self.piece_at(f"{c}{n}")
                piece_properties = piece.define_coor()

                if isinstance(prop, (tuple, list)):
                    # Ensure all properties are satisfied
                    if all(p in piece_properties for p in prop):
                        if first_occurence:
                            return f"{c}{n}"
                        if piece.ident == 'Pawn' and piece.position[1] in '18':
                            for choice in [' =Q', ' =B', ' =N', ' =R']:
                                lst.append(f"{c}{n}{choice}")
                        else:
                            lst.append(f"{c}{n}")
                else:
                    # If single property, check it
                    if prop in piece_properties:
                        if first_occurence:
                            return f"{c}{n}"
                        if piece.ident == 'Pawn' and piece.position[1] in '18':
                            for choice in [' =Q', ' =B', ' =N', ' =R']:
                                lst.append(f"{c}{n}{choice}")
                        else:
                            lst.append(f"{c}{n}")
        return lst
        
    def pair_of_all_mvs(self, target_player: Literal["b", "w"] = "w") -> set:
        """Get all the posible/valid coordinates of targeted player in tuple form 
        it also includes pawn promotion with every choice

        #### Args:
        - target_player (Literal[&quot;b&quot;, &quot;w&quot;], optional): 'W' for white anf 'b' for black. Defaults to "w".

        #### Returns:
        - set: all the posible/valid coordinates of targeted player
        """
        pairs = set(
                [(pos, self.filter_mv(move)) for pos in self.find_all_cords("black" if target_player == "b" or target_player == "black"  else "white") for move in self.get_valid_mv(pos)],
        )
        pairs = sorted(pairs)
        new_pairs = []
        for pair in pairs:
            if isinstance(self.piece_at(pair[0]), Pawn) and pair[1][1] in '18':
                for choice in [" =Q", " =R", ' =K', ' =B']:
                    pairs_w_choice = (pair[0], pair[1] + choice)
                    new_pairs.append(pairs_w_choice)
            else:
                new_pairs.append(pair)
        return new_pairs
        
    def check_board(self) -> tuple[bool, str]:
        """
        Checks the state of the game for checkmate, win, draw, or continuation based on the kings and other pieces.
        #### Returns:
        - tuple[bool, str]: A tuple indicating if the game should continue (True/False) and a message.
        """
        if not self.pair_of_all_mvs(self.player_turn[0]):
            return False, f"MATCH_OVER: Our Winner is {'Black' if self.player_turn == 'white' else 'White'}".title()
        
        black_king = bool(self.find_all_cords(["King", "black"]))
        white_king = bool(self.find_all_cords(["King", "white"]))

        # Get all the remaining pieces on the board
        pieces_left = {item.symbol for row in self.board for item in row}

        # Common draw conditions for insufficient material
        insufficient_material = [
            {"[_]", "[♚]", "[♔]"},  # Only kings
            {"[_]", "[♚]", "[♔]", "[♙]"},  # Kings and one white pawn
            {"[_]", "[♚]", "[♔]", "[♟︎]"},  # Kings and one black pawn
            {"[_]", "[♚]", "[♔]", "[♘]"},  # Kings and a knight
            {"[_]", "[♚]", "[♔]", "[♗]"},  # Kings and a bishop
            {"[_]", "[♚]", "[♔]", "[♗]", "[♝]"},  # Kings and opposite-colored bishops
            {"[_]", "[♚]", "[♔]", "[♘]", "[♙]"},  # Kings, knight, and white pawn
            {"[_]", "[♚]", "[♔]", "[♘]", "[♟︎]"},  # Kings, knight, and black pawn
        ]
        # Check for insufficient material draw
        if any(pieces_left == condition for condition in insufficient_material):
            return False, 'GAME_DRAW: Insufficient material for either side to win.'

        # Check if one side has won
        if black_king and not white_king:
            return False, 'GAME_OVER: Black wins.'
        elif white_king and not black_king:
            return False, 'GAME_OVER: White wins.'

        # Otherwise, the game continues
        return True, f'Now it\'s {self.player_turn.title()}\'s turn.'
    
    @staticmethod
    def clear_term():
        """#### Clear Terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def reset_game(self):
        self.setup_notation()
        self.history.moves = []
        self.player_turn = 'white'
        self.score_board.reset()
        self.no_turns = 0
        self.tabular_history.clear_rows()
        
    def undo_a_move(self):
        """Undo a move and tranfer the player turn
        #### Returns (only 1 of these 2)
        - None: When there is no Moves to undo
        ###### OR
        - List: List of move history without last move / undone move
        """
        if self.history:
            new_his = self.history.moves[:-1]
            self.reset_game()
            self.apply_history(new_his)
            return self.history
        else:
            return None
    
    def open_cmd(self):
        """
        Interactive Command Panel for Chess Game Control

        This method provides a command-line interface for managing the state of the chess game. 
        It offers several commands to perform actions such as resetting the game, viewing the move history, 
        toggling board color display, and checking game status.

        Returns:
            bool: A flag indicating whether the game should continue (`True`) or end (`False`).

        Commands:
            --back  : Close the command panel and return to the main game loop.
            --end   : End the game immediately and declare a winner based on capturing scores.
            --undo  : Undo the last move, if available.
            --rsg   : Reset the game to its initial state.
            --his   : Display the move history.
            --colo  : Toggle the chessboard color display (on/off).
            --bn    : Show the current board notation.
            --mvs   : Display all possible moves for the current player.
            --mve   : Display all possible moves for the opponent.
            ---     : Check if the current player is in checkmate and declare a winner if so.

        Behavior:
            - The method clears the terminal screen and presents a list of available commands.
            - Processes user input to execute corresponding game actions.
            - Handles invalid or unknown commands gracefully by prompting the user to try again.
            - Provides interactive feedback for each command, such as showing results or updating the game state.

        Side Effects:
            - Updates the internal game state based on the command executed (e.g., resetting the game, undoing moves).
            - May print game-related information to the console (e.g., board notation, move history).

        Examples:
            # Access the command panel during the game
            game.cmd_panel()

            # Example command flow:
            # Enter "--his" to view move history
            # Enter "--end" to terminate the game and declare a winner
            # Enter "--back" to exit the command panel and resume the game

        Notes:
            - The method assumes the presence of several helper methods and attributes:
                - `self.undo_a_move()`: Handles undoing the last move.
                - `self.reset_game()`: Resets the game to its starting state.
                - `self.history`: Stores the history of moves.
                - `self.board_notation`: Returns the current board notation.
                - `self.pair_of_all_mvs(color)`: Retrieves all possible moves for the specified player.
                - `UI_SETTINGS`: A dictionary controlling UI preferences, such as board coloring.
        """

        game_flag = True
        while True:
            self.clear_term()
            print("Commands:")
            print(" --back => Close the command panel and return to the main game loop.")
            print(" --end  => End the game immediately and declare a winner based on capturing scores.")
            print(" --undo => Undo the last move, if available.")
            print(" --rsg  => Reset the game to its initial state.")
            print(" --his  => Display the move history.")
            print(" --colo => Toggle the chessboard color display (on/off).")
            print(" --bn   => Show the current board notation.")
            print(" --mvs  => Display all possible moves for the current player.")
            print(" --mve  => Display all possible moves for the opponent.")
            print(" ---    => Check if the current player is in checkmate and declare a winner if so.")

            command = input("\nEnter command: ").lower()
            
            match command:
                case "--back":
                    break
                
                case "--end":
                    winner = "White Wins" if self.score_board.cap_scored_w > self.score_board.cap_scored_b else \
                            "Black Wins" if self.score_board.cap_scored_w < self.score_board.cap_scored_b else "Draw"
                    print(f"GAME_END: {winner.title()} [by comparing Capturing Scores].")
                    print(self.history)
                    game_flag=False
                    break
                
                case "--undo":
                    if not self.undo_a_move():
                        print("There are no moves to undo.")
                    break
                
                case "--rsg":
                    self.reset_game()
                    break
                
                case "--his":
                    print(self.history)
                    input("[Press Enter to continue...]")
                
                case "--bn":
                    print(self.board_notation)
                    input("[Press Enter to continue...]")
                    
                case "--colo":
                    UI_SETTINGS["Display Colored Board"] = not UI_SETTINGS["Display Colored Board"]
                    print("Chessboard is now", "colored" if UI_SETTINGS["Display Colored Board"] else "not colored")
                    input("[Press Enter to continue...]")
                    break
                
                case "--mvs":
                    print(self.pair_of_all_mvs(self.player_turn[0]))
                    input("[Press Enter to continue...]")
                
                case "--mve":
                    print(self.pair_of_all_mvs("b" if self.player_turn[0] == "w" else 'w'))
                    input("[Press Enter to continue...]")

                case "---":
                    if not self.pair_of_all_mvs(self.player_turn):
                        print(f"CHECKMATE: {"White" if self.player_turn[0] == 'b' else "Black"} wins!")
                        game_flag=False
                        break
                    else:
                        print("No winner yet.")
                    input("[Press Enter to continue...]")
                    break
                case _:
                    print("Unknown command. Please enter a valid command.")
                    input("[Press Enter to continue...]")
                    continue

        return game_flag
    
    def launch_chess_game(self):
        """
        Run All the functions in such a manner to run a Chess Match between 2 players(Users)
        """
        game_flag, message1 = self.check_board()
        while self.check_board()[0]:
            if not game_flag: 
                print(message1)
                break
            self.clear_term()
            print(message1, end='   ')
            input("[Press Enter to continue...]\n")

            self.clear_term()
            self.print_board()
            self.score_board.print()
            
            cords = self.get_destinations()
            if cords == "--cmd":
                t = self.open_cmd()
                game_flag, message1 = self.check_board()
                game_flag &= t
                if not game_flag:
                    message1 = "Game Ends!"
                continue
            note, d_n, a_n, m_t = self + cords
            self.no_turns +=1

            print(note)
            
            input("[Press Enter to continue...]")
            self.tabular_history.add_row([self.no_turns, d_n, a_n, m_t, self.player_turn.title()])
            if (MAKE_RECORD_OF_MOVES_IN_OTHER_FILE and self.have_history):
                with open(MOVES_HISTORY_PATH, 'w') as f:
                    f.write(str(self.tabular_history) + '\n')

            self.change_player_turn()
            game_flag, message1 = self.check_board()
            
        if (MAKE_RECORD_OF_MOVES_IN_OTHER_FILE and self.have_history):
            with open(MOVES_HISTORY_PATH, '+a') as f:
                f.writelines(f'\n{self.history}\n')
            print(message1)

    # For Bots
    def set_of_all_mvs(self, target_player: Literal["b", "w"] = "w") -> set:
        """Get all the posible/valid coordinates of targeted player
        #### Args:
        - target_player (Literal[&quot;b&quot;, &quot;w&quot;], optional): 'W' for white anf 'b' for black. Defaults to "w".

        #### Returns:
        - set: all the posible/valid coordinates of targeted player
        """
        nor_moves = set(
            self.filter_moves(
                [move for coordinates in self.find_all_cords("black" if target_player == "b" or target_player == "black"  else "white") for move in self.get_valid_mv(coordinates)],
                True
                )
            )
        return nor_moves
    
if __name__ == "__main__":
    # Display the mission objective to the user
    print("Mission: Find a move for a checkmate")
    input("[Press Enter to continue...]")
    
    # Initialize the chessboard
    board = ChessBoard()
    
    # Apply a sequence of moves to the board
    # Moves are represented as tuples ('start_square', 'end_square')
    board.apply_history(
        [
            ('e2', 'e4'), ('e7', 'e5'), 
            ('d1', 'h5'), ('g7', 'g6'),
            ('h5', 'e5'), ('f8', 'e7'),
            ('e5', 'h8'), ('e7', 'f8'),
            ('h8', 'g8'), ('f7', 'f5'), 
            ('f1', 'c4'), ('d7', 'd6'),
            # Uncomment the following move if needed:
            # ('g8', 'f7'),
        ],
        print_each_state=False,  # Disable state printing for clarity
        make_record=True         # Enable move recording for future analysis
    )
    
    # Launch the interactive chess game
    board.launch_chess_game()
