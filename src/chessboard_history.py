class History:
  def __init__(self):
    self.moves = []
    
  def __add__(self, move: tuple[str, str]):
    self.moves.append(move)
  
  def __repr__(self) -> str:
    return str(self.moves)
  
  def __iter__(self):
    return iter(self.moves)
  
  def __sub__(self, other: int):
    self.moves = self.moves[:-other]
    return self.moves

if __name__ == "__main__":
  his = History()
  his + ('e2', "e4")
  his + ('d7', "d5")
  his + ('e2', "e4")
  his + ('d7', "d5")
  his + ('e2', "e4")
  his + ('d7', "d5")
  
  print(his)
  his - 2
  print(his)
  
  