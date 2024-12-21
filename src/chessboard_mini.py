from chessboard_pieces import *
import numpy as np

class MiniChessboard:
  def __init__(self, board_not: str = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr") -> None:
    piece_classes = {"K": King, "Q": Queen, "N": Knight, "B": Bishop, "R": Rook, "P": Pawn}
    self.board = []

    for i, row_not in enumerate(board_not.strip().split('/')):
      row = []
      for char in row_not:
        if char.isdigit():
          row.extend([Empty(f"{chr(len(row) + ord('a'))}{8 - i}") for _ in range(int(char))])
        else:
          color = 'b' if char.isupper() else 'w'
          row.append(piece_classes[char.upper()](color=color, position=f"{chr(len(row) + ord('a'))}{8 - i}"))
      while len(row) < 8:
        row.append(Empty(f"{chr(len(row) + ord('a'))}{8 - i}"))
      self.board.append(row)

  def print_board(self):
    print("   |a||b||c||d||e||f||g||h|")
    for i, row in enumerate(self.board):
      print(f"{8 - i}--" + "".join(str(piece) for piece in row))

  def piece_at(self, cord: str):
    return self.board[8 - int(cord[1])][ord(cord[0]) - ord('a')]

  def place_piece(self, piece):
    self.board[8 - int(piece.position[1])][ord(piece.position[0]) - ord('a')] = piece

  def __add__(self, moves: list[tuple[str]]):
    if isinstance(moves, list):
      for move in moves:
        self + move
      return
    frm, to = moves 
    piece = self.piece_at(frm)
    self.place_piece(Empty(frm))
    promoted = piece + to #+ " =Q" if isinstance(self.piece_at(frm), Pawn) and to in "18" else ""
    self.place_piece(promoted or piece)

  def is_king_safe(self, king_turn="black", move=tuple()) -> bool:
    if move:
        self + [move]

    for row in self.board:
        for piece in row:
            if piece.color == king_turn and isinstance(piece, King):
                king_pos = piece.position
                opponent_moves = self.get_valid_mvs("white" if king_turn == "black" else "black")
                return king_pos not in opponent_moves

    return True  # King not found or not in check
  
  def get_pseudo_legal_mvs(self, target_player: str='black') -> set:
    moves = set()
    for row in self.board:
      for piece in row:
        if piece.color == target_player:
          for steps in piece.steps:
            pos = piece.position
            for dx, dy in steps:
              new_c = chr(ord(pos[0]) + dx)
              new_r = int(pos[1]) + dy
              if 'a' <= new_c <= 'h' and 1 <= new_r <= 8:
                target_pos = f"{new_c}{new_r}"
                if isinstance(piece, Pawn) and new_c == pos[0]: continue
                moves.add(target_pos)
                if not isinstance(self.piece_at(target_pos), Empty): break
    return moves
  
  def get_valid_mvs(self, turn: Literal['white', 'black']): #
    moves_lst = []
    postions_of_target_player = []
    for i in range(0, 8):
      for j in range(1, 9):
        c = chr(ord('a') + i)
        if self.piece_at(f"{c}{j}").color == turn:
          postions_of_target_player.append(f"{c}{j}")
          
    for position in postions_of_target_player:
      C, N = ord(position[0]), int(position[1])
      
      for consecutive_steps in self.piece_at(position).steps:
        for step in consecutive_steps:
          new_c = chr(C + step[0])
          new_n = N + step[1]
          if  1 <= new_n <= 8 and  'a' <= new_c <= 'h':
            if isinstance(self.piece_at(position), Pawn) and new_c == chr(C): continue
            moves_lst.append(f"{new_c}{new_n}")
            if not isinstance(self.piece_at(f"{new_c}{new_n}"), Empty): break
            
    return set(moves_lst)
  
  @property
  def board_notation(self):
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

  def is_mv_safe(self, mv: tuple, cord: str= None): #
    self + mv
    return ((mv[1] if not cord else cord) in self.get_valid_mvs(-self.piece_at(mv[1]))) \
      or ((mv[1] if not cord else cord) not in self.get_valid_mvs(-self.piece_at(mv[1])))

class ChessNot:
    def __init__(self, board_notation: str = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr"):
        self.board = self.board_notation_to_board(board_notation)

    def board_notation_to_board(self, board_notation: str):
        board = [[] for _ in range(8)]
        rows = board_notation.split('/')
        for idx, row in enumerate(rows):
            for piece in row:
                if piece.isdigit():
                    for _ in range(int(piece)):
                        board[idx].append('.')
                else:
                    board[idx].append(piece)
        return board

    def __add__(self, moves: tuple[str]):
      if isinstance(moves, list):
        for mv in moves:
          self + mv
        return
      frm, to = moves 
      piece = self.board[8 - int(frm[1])][ord(frm[0]) - ord('a')]
      self.board[8 - int(frm[1])][ord(frm[0]) - ord('a')] = '.'
      promoted = None
      if piece in 'Pp' and (to[1] == '8' or to[1] == '1') and '='in to :
        promoted = to.split('=')[1].strip()
        promoted = promoted.lower() if piece.islower() else promoted.upper()
        
      self.board[8 - int(to[1])][ord(to[0]) - ord('a')] = (promoted or piece)
      
    def __repr__(self) -> str:
        board = ''
        for row in self.board:
            board += ' '.join(row) + '\n'
        return board.strip()
    
    @property
    def board_notation(self) -> str:
        notation = '/'
        for row in self.board:
          for piece in row:
            if piece == '.':
              if notation[-1].isdigit():
                notation = notation[:-1] + str(int(notation[-1]) + 1)
              else:
                notation += '1'
              continue

            notation += piece
          notation += '/'
          
        return notation.strip('/')

if __name__ == "__main__":
  cb = MiniChessboard()
  cn = ChessNot()
  while True:
    cb.print_board()
    print(cn)
    f = input("From: ")
    t = input("To: ")
    cb + (f, t)
    cn + (f, t)
    print(cn.board_notation)
    print('is king[\'w\'] safe', cb.is_king_safe('white'))