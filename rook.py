from chess import Chess

class Rook(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    def __init__(self, side, name=None) -> None:
        super().__init__(side)
        self.type = 'Archer'
        self.name = name
        self.x = (0 if self.side == 'w' else 7)
        self.y = (0 if self.name == 'L' else 7) if name else 0
    def __str__(self) -> str:
        white_rook = '♖'
        black_rook = '♜'
        return f"{white_rook if self.side == 'w' else black_rook}Rook"
    
    direction = Chess.direction[:4]        