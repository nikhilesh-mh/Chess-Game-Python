from typing import Union
from chessboard_pieces import *
class Scoreboard:
    """
    #### `Scoreboard` Class is used for storing the pieces who were captured and it `also count their Capturing Scores`
    ##### Features :-
    - `'+' Operator`: To add the Captured Pieces and by using their `color` attribute/property to append them to their corresponding list
    """
    def __init__(self):
        """#### `Scoreboard` Class is used for storing the pieces who were captured and it `also count their Capturing Scores`
        """
        self.whites_win_pieces = []
        self.cap_scored_w = 0
        self.blacks_win_pieces = []
        self.cap_scored_b = 0

    def print(self) -> None:
        """
        ### This function displays the pieces of the player who wins.
        """
        # Simplified alignment and formatting
        white_score = f"{self.cap_scored_w}".rjust(2)
        black_score = f"{self.cap_scored_b}".rjust(2)
        
        print(f"White Captured({white_score}): -{''.join(self.whites_win_pieces)}-")
        print(f"Black Captured({black_score}): -{''.join(self.blacks_win_pieces)}-")

    def __add__(self, captured_piece: Union['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']) -> str:
        """
        ### This method adds captured pieces to the respective player's score.
        ### Note: '+' operators message like `"\\nMessage\\n"`
        ### Returns :-
        - `str`: `A message of Capturing a piece`
        """
        if captured_piece.color == "white":
            self.blacks_win_pieces.append(captured_piece.symbol)
            self.cap_scored_b += captured_piece.cap_score
            return f"\n--Black Won `{captured_piece.symbol} ` from '{captured_piece.position}'.--"
        elif captured_piece.color == "black":
            self.whites_win_pieces.append(captured_piece.symbol)
            self.cap_scored_w += captured_piece.cap_score
            return f"\n--White Won `{captured_piece.symbol} ` from '{captured_piece.position}'.--"
        return self
    
    def reset(self):
        """### Reset everything from scoreboard [used in reseting game]
        """
        self.whites_win_pieces = []
        self.blacks_win_pieces = []
        self.cap_scored_b =  0
        self.cap_scored_w = 0

# Example Usage
if __name__ == '__main__':
    sc = Scoreboard() # Creating new instance of Scoreboard
    
    captured_w_piece1 = Pawn('w', "i0")  # White Pawn with an Imaginary position and have '1' integer as capturing score
    captured_w_piece2 = Queen('w', "i0") # White Queen with an Imaginary position and have '9' integer as capturing score
    captured_b_piece1 = Bishop('b', "i0") # Black Bishop with an Imaginary position and have '3' integer as capturing score
    captured_b_piece2 = Knight('b', "i0") # Black Knight with an Imaginary position and have '3' integer as capturing score
    
    # Print Capturing Messages ('+' operators message like "\nMessage\n")
    print("Note1", sc + captured_w_piece1) 
    print("Note2", sc + captured_w_piece2)
    print("Note3", sc + captured_b_piece1)
    print("Note4", sc + captured_b_piece2)
    
    print() # Gap for Visual Clarity
    sc.print() # Display Catured Pieces with Capturing Scores
    
    print() # Gap for Visual Clarity
    sc.reset() # Reset All Catured Pieces and Capturing Score
    sc.print() # Display reset/zero Catured Pieces with Capturing Scores
    