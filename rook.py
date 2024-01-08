from chess import Chess

class Rook(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    def __init__(self,side,name=None,extendedLine=None) -> None:
        super().__init__(side,move=None,take=None,defend=None,Defender=None)
        self.type = 'Archer'
        self.name = name
        self.extendedLine = extendedLine
        self.x = (0 if self.side == 'w' else 7)
        self.y = (0 if self.name == 'L' else 7) if name else 0
    def __str__(self) -> str:
        white_rook = '♖'
        black_rook = '♜'
        return f"{white_rook if self.side == 'w' else black_rook}Rook"
    
    direction = Chess.direction[:4]        