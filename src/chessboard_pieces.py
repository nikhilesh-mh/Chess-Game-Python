from typing import Literal, Union

# Piece Representation
REPRESENT_PIECE_WITH = 'Symbol' # 'Symbol' or 'Letters'

PIECE_SYMBOLS = {
    'Symbol':{'Pawnb': "[♟︎]", 'Knightb': "[♞]", 'Bishopb': "[♝]", 'Rookb': "[♜]", 'Queenb': "[♛]", 'Kingb': "[♚]",
              'Pawnw': "[♙]", 'Knightw': "[♘]", 'Bishopw': "[♗]", 'Rookw': "[♖]", 'Queenw': "[♕]", 'Kingw': "[♔]"},
    'Letter':{'Pawnb': "[P]", 'Knightb': "[N]", 'Bishopb': "[B]", 'Rookb': "[R]", 'Queenb': "[Q]", 'Kingb': "[K]",
              'Pawnw': "[p]", 'Knightw': "[n]", 'Bishopw': "[b]", 'Rookw': "[r]", 'Queenw': "[q]", 'Kingw': "[k]"},
}

# Used For bots
PIECE_SQUARE_TABLES = {
    'Pawn': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,], 
        [0.3, 0.7, 0.7, 1.0, 1.0, 0.7, 0.7, 0.3,], 
        [0.3, 0.3, 0.7, 0.7, 0.7, 0.3, 0.3, 0.3,],
        [0.3, 0.3, 0.3, 0.7, 0.7, 0.3, 0.3, 0.3,],
        [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,],
        [0.0, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.0,],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,],
    ],
    'Knight': [
        [-1.0, -0.8, -0.6, -0.6, -0.6, -0.6, -0.8, -1.0,],
        [-0.8, -0.4, 0.0, 0.0, 0.0, 0.0, -0.4, -0.8,],
        [-0.6, 0.0, 0.2, 0.3, 0.3, 0.2, 0.0, -0.6,],
        [-0.6, 0.1, 0.3, 0.4, 0.4, 0.3, 0.1, -0.6,],
        [-0.6, 0.0, 0.3, 0.4, 0.4, 0.3, 0.0, -0.6,],
        [-0.6, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, -0.6,],
        [-0.8, -0.4, 0.0, 0.0, 0.0, 0.0, -0.4, -0.8,],
        [-1.0, -0.8, -0.6, -0.6, -0.6, -0.6, -0.8, -1.0,],
        ],
    'Bishop': [
        [-1.0, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -1.0,],
        [-0.5, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, -0.5,],
        [-0.5, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, -0.5,],
        [-0.5, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, -0.5,],
        [-0.5, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, -0.5,],
        [-0.5, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, -0.5,],
        [-0.5, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, -0.5,],
        [-1.0, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -1.0,],
        ],
    'Rook': [
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0,],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5,],
        [0.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 0.0,],
        [0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0,],
        [0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0,],
        [0.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 0.0,],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0,],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,],
        ],
    'Queen': [
        [-1.0, -0.5, -0.5, 0.0, 0.0, -0.5, -0.5, -1.0,],
        [-0.5, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, -0.5,],
        [-0.5, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, -0.5,],
        [0.0, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, 0.0,],
        [0.0, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, 0.0,],
        [-0.5, 0.2, 0.5, 0.5, 0.5, 0.5, 0.2, -0.5,],
        [-0.5, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, -0.5,],
        [-1.0, -0.5, -0.5, 0.0, 0.0, -0.5, -0.5, -1.0,],
        ],
    'King': [
        [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6,],
        [-0.6, -0.6, -0.8, -1.0, -1.0, -0.8, -0.6, -0.6,],
        [-0.6, -0.6, -0.8, -1.0, -1.0, -0.8, -0.6, -0.6,],
        [-0.6, -0.6, -0.8, -1.0, -1.0, -0.8, -0.6, -0.6,],
        [-0.4, -0.4, -0.6, -0.8, -0.8, -0.6, -0.4, -0.4,],
        [-0.2, -0.2, -0.4, -0.6, -0.6, -0.4, -0.2, -0.2,],
        [0.4, 0.4, 0.2, 0.0, 0.0, 0.2, 0.4, 0.4,],
        [0.4, 0.4, 0.2, 0.0, 0.0, 0.2, 0.4, 0.4,],
    ]
}

class Pawn:
    ident = "Pawn"  # Identity
    cap_score = 1  # capturing score
    is_in_doip = False  # danger of in passing
    
    def __init__(self, color: Literal["b", "w"], position: str):
        self.symbol = PIECE_SYMBOLS[REPRESENT_PIECE_WITH][f"{self.ident}{color}"]
        self.color = "white" if color == "w" else "black"
        self.position = position

    def __repr__(self) -> str:
        return self.symbol

    def __add__(self, new_position: str) ->  Union['Queen','Knight' ,'Rook' ,'Bishop' , None]:
        if new_position == "x":
            self.is_in_doip = False
            return None
        
        old_n, new_n = int(self.position[1]), int(new_position[1])
        if abs(new_n - old_n) == 2:
            self.is_in_doip = True
        else:
            self.is_in_doip = False
            
        if "=" in new_position:
            new_pos, choice = new_position.split("=")
            new_pos = new_pos.strip().lower()
            choice = choice.strip().upper()
            
            self.position = new_pos
            
            n = int(new_pos[1])
            if (n == 1 and self.symbol == '[♟︎]') or (n == 8 and self.symbol == '[♙]'):
                player =  "w" if n == 8 else "b"
                choices = [Queen(player, self.position), Knight(player, self.position), Rook(player, self.position), Bishop(player, self.position)] 
                
                choice_no = 0 if  choice == "Q" else 1 if choice == "N" else 2 if choice ==  "R" else 3 if choice ==  "B" else 1
                return choices[choice_no]
        else:
            self.position = new_position
            
            n = int(new_position[1])
            if (n == 1 and self.symbol == '[♟︎]') or (n == 8 and self.symbol == '[♙]'):
                # Pawn promotion if it reaches the last rank
                print('Your Pawn has reached its last rank! Promote it now.\nEnter a number to promote [1 - 4]')
                player =  "w" if n == 8 else "b"
                choices = [Queen(player, self.position), Knight(player, self.position), Rook(player, self.position), Bishop(player, self.position)] 

                while True:
                    print(*list(f"[{i+1} => {choices[i].symbol[1]} ] " for i in range(4)))
                    choice_no = input('>>>> ')
                    if choice_no.isdigit():
                        choice_no = int(choice_no)
                        if 1 <= choice_no <= 4:
                            return choices[choice_no - 1]
                        else:
                            print("Invalid Number! Please choose a number between 1 and 4.")
                    else:
                        print("Invalid input! Please enter a number.")
            return None

    def define_coor(self) -> tuple[str, str, str]:
        return (self.ident, self.color, self.symbol)
    
    def __neg__(self) -> Literal['white', 'black']:
        return "white"  if self.color == "black" else "black"

    @property
    def steps(self) -> list[list[str]]:
        steps =  [[(0, 1), (0,2)], [(-1, 1)], [(1, 1)]] if  self.color == "white" else [[(0, -1), (0,-2)], [(-1, -1)], [(1, -1)]]
        if self.position[1] != "2" and self.color == "white":
            steps[0].remove((0,2))
        elif self.position[1] != "7" and self.color == "black":
            steps[0].remove((0,-2))
        return  steps

class Knight:
    ident = "Knight"  # Identity
    cap_score = 3  # capturing score

    def __init__(self, color: Literal["b", "w"], position: str):
        self.symbol = PIECE_SYMBOLS[REPRESENT_PIECE_WITH][f"{self.ident}{color}"]
        self.color = "white" if color == "w" else "black"
        self.position = position

    def __repr__(self) -> str:
        return self.symbol

    def __add__(self, new_position: str):
        self.position = new_position

    def define_coor(self) -> tuple[str, str, str]:
        return (self.ident, self.color, self.symbol)

    def __neg__(self):
        return "white"  if self.color == "black" else "black"
    
    @property
    def steps(self) ->  list[list[str]]:
        return [[(2, 1)], [(2, -1)], [(-2, 1)], [(-2, -1)], [(1, 2)], [(1, -2)], [(-1, 2)], [(-1, -2)]]

class Bishop:
    ident = "Bishop"  # Identity
    cap_score = 3  # capturing score
    
    def __init__(self, color: Literal["b", "w"], position: str):
        self.symbol = PIECE_SYMBOLS[REPRESENT_PIECE_WITH][f"{self.ident}{color}"]
        self.color = "white" if color == "w" else "black"
        self.position = position

    def __repr__(self) -> str:
        return self.symbol

    def __add__(self, new_position: str):
        self.position = new_position

    def define_coor(self) -> tuple[str, str, str]:
        return (self.ident, self.color, self.symbol)

    def __neg__(self):
        return "white"  if self.color == "black" else "black"
    
    @property
    def steps(self) ->  list[str]:
        return [[(s1*a, s2*a) for a in range(1, 8)] for s1,s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]

class Rook:
    ident = "Rook"  # Identity
    cap_score = 5  # capturing score

    def __init__(self, color: Literal["b", "w"], position: str):
        self.symbol = PIECE_SYMBOLS[REPRESENT_PIECE_WITH][f"{self.ident}{color}"]
        self.color = "white" if color == "w" else "black"
        self.position = position 
        self.is_rook_moved =  False

    def __repr__(self) -> str:
        return self.symbol

    def __add__(self, new_position: str):
        self.position = new_position
        self.is_rook_moved =  True

    def define_coor(self) -> tuple[str, str, str]:
        return (self.ident, self.color, self.symbol)

    def __neg__(self):
        return "white"  if self.color == "black" else "black"
    
    @property
    def steps(self) ->  list[str]:
        return [[(s1*a, s2*a) for a in range(1, 8)] for s1,s2 in [(0, 1), (0, -1), (1, 0), (-1, 0)]]

class Queen:
    ident = "Queen"  # Identity
    cap_score = 9  # capturing score

    def __init__(self, color: Literal["b", "w"], position: str):
        self.symbol = PIECE_SYMBOLS[REPRESENT_PIECE_WITH][f"{self.ident}{color}"]
        self.color = "white" if color == "w" else "black"
        self.position = position

    def __repr__(self) -> str:
        return self.symbol

    def __add__(self, new_position: str):
        self.position = new_position

    def define_coor(self) -> tuple[str, str, str]:
        return (self.ident, self.color, self.symbol)
    
    def __neg__(self):
        return "white"  if self.color == "black" else "black"
    
    @property
    def steps(self) ->  list[str]:
        return [[(s1*a, s2*a) for a in range(1, 8)] for s1,s2 in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]]

class King:
    ident = "King"  # Identity
    cap_score = 104  # capturing score
    is_king_moved =  False
    
    def __init__(self, color: Literal["b", "w"], position: str):
        self.symbol = PIECE_SYMBOLS[REPRESENT_PIECE_WITH][f"{self.ident}{color}"]
        self.color = "white" if color == "w" else "black"
        self.position = position

    def __repr__(self) -> str:
        return self.symbol

    def __add__(self, new_position: str):
        self.position = new_position
        self.is_king_moved =  True

    def define_coor(self) -> tuple[str, str, str]:
        return (self.ident, self.color, self.symbol)
    
    def __neg__(self):
        return "white"  if self.color == "black" else "black"
    
    @property
    def steps(self) ->  list[str]:
        return [[(0, 1)], [(0, -1)], [(1, 0)], [(-1, 0)], [(1, 1)], [(1, -1)], [(-1, -1)], [(-1, 1)]]

class Empty:
    ident = "Empty"  # Identity
    color = None 
    cap_score = 0  # capturing score
    
    def __init__(self, position: str):
        self.symbol = "[_]"
        self.position = position 

    def __repr__(self) -> str:
        return self.symbol

    def __add__(self, new_position: str):
        self.position = new_position
        
    def define_coor(self) -> tuple[str, str, str]:
        return (self.ident, self.color, self.symbol)
    
    @property
    def steps(self) ->  list[str]:
        return []
 
class None_Piece:
    ident = None  # Identity
    def __init__(self):
        self.symbol = "[?]"

    def __repr__(self) -> str:
        return self.symbol

    def define_coor(self) -> tuple[str, str]:
        return (None, None, self.symbol)

class repr_piece:
    """
    ### Representive Piece
            
    #### These classes is used to store all the data related to Pawn Piece in real life
    #### Special Perperties :-
    #### `Pawn`:
    - `is_in_doip [bool]` : Return bool on the fact that the Pawn is in the danger of EnPassing move (used in generating EnPassng moves)
    #### `King`:
    - `is_king_moved [bool]` : Return bool on the fact that the King is move (used in generating Castling moves)
    #### `Rook`:
    - `is_rook_moved [bool]` : Return bool on the fact that the Rook is move (used in generating Castling moves)
            
    ##### Perperties :-
    - `cap_score [int= 1]` : Capturing Score of This Piece
    - `ident [str= 'Pawn']` : Identity of This Piece
    - `steps` [list[tupr[int, int]]]: Returns squares/coordinates difference of from and to square
            
    ##### Methods :-
    - `'+' Operator` : return either `None` or `Instance of Promoted piece`
    - `define_coor [tuple(str)]`: 3 Visual/Main Properties `[ident, color, symbol]` of This piece
    - `neg()` or `-(x)` ['white', 'black'] : Returns Opposite color of this piece [Eg. -Pawn('w', 'i0') -> 'black']
    - `repr()` or `representation` [str]: return symbol of this piece (used in print or formating str)
            
    ##### Special Piece Types :-
    - `Empty \'[_]\'`: To Repressent Empty Pieces
    - `None_piece\'[?]\'`: To Repressent None Pieces or Piece with Impossible Coordinates
    """

    def create_new(self, Instance: Pawn | Knight | Bishop | Rook | Queen | King, color: Literal['w', 'b'], position: str)\
        -> Pawn | Knight | Bishop | Rook | Queen | King:
        return Instance(color, position)

    def eval_position(piece: Pawn | Knight | Bishop | Rook | Queen | King):
        """Evaluate the position of a piece on the board. Returns a value between -1 and 1, where -1 is the worst position and 1 is the best position."""
        piece_square_table = PIECE_SQUARE_TABLES[piece.ident]
        col = ord(piece.position[0]) - ord('a')
        row = 8 - int(piece.position[1])
        return piece_square_table[row][col] if piece.color == 'white' else list(reversed(piece_square_table))[row][col]
# Examples Usage
if __name__ == '__main__':

        
    # Creating Instances White Pawn, Black Rook And White King with Some Imaginary positions 
    pawn1 = repr_piece().create_new(Pawn, color='w', position='e2') # or Pawn('w', 'e2')
    rook1 = repr_piece().create_new(Rook, color='b', position='i4')
    king1 = repr_piece().create_new(King, color='w', position='i0')
    
    print('(1)')
    print(pawn1.define_coor()) # -> ('Pawn', 'white', '[♟︎]')
    print(rook1.define_coor()) # -> ('Rook', 'black', '[♜]')
    print(king1.define_coor()) # -> ('King', 'white', '[♔]')
    
    print() # Gap for Visual Clarity
    
    print('(2)')
    print("Old Position[Before Adding]:", pawn1.position) 
    pawn1 + 'e4' 
    print("New Position[After Adding \'e4\']:", pawn1.position) 
    print("Is in the danger of En Passing move:", pawn1.is_in_doip)
    pawn1 + 'x' # reseting Pawn
    print("Is in the danger of En Passing move[after reset, ie., + \'x\']:", pawn1.is_in_doip)
    
    print() # Gap for Visual Clarity
    
    print('(3)')
    # Assigning new position[having numeric component '8' as it's white] with choice[to avoid asking choice from user]
    promoted_piece = pawn1 + "e8 =Q" 
    """Comment-out above and below ones to see another output"""
    # promoted_piece = pawn1 + 'e8'
    print("promoted_piece =>", promoted_piece)
    
    print() # Gap for Visual Clarity
    
    print('(4)')
    king1 + 'i1'
    rook1 + 'j4'
    print('is_king_moved after adding new position to king [>>>> king1 + \'i1\']:',king1.is_king_moved)
    print('is_rook_moved after adding new position to rook [>>>> rook1 + \'j1\']:',rook1.is_rook_moved)

    print() # Gap for Visual Clarity
    print('(5)')
    print('Actual Color:', king1.color)
    print('Opposite Color:', -king1)
    
    print()# Gap for Visual Clarity
    
    print('(6)')
    print(Empty('a3').define_coor())# Print properties of Instances Empty piece
    print(None_Piece().define_coor()) # Print properties of Instances None_Piece piece
    