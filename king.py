from chess import Chess
from actions import Actions

class King(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<   
    def __init__(self,side,castling=False) -> None:
        super().__init__(side,move=set(),take=set(),defend=set())
        self.type = 'Warrior'
        self.castling = castling
        self.x = (0 if self.side == 'w' else 7)
        self.y = 4
 
    def __str__(self) -> str:
        white_king = '♔'
        black_king = '♚'
        return f"{white_king if self.side == 'w' else black_king}King"        