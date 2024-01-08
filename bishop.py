from chess import Chess

class Bishop(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None,extendedLine=None) -> None:
        super().__init__(side,move=None,take=None,defend=None,Defender=None)
        self.type = 'Archer'
        self.name = name
        self.extendedLine = extendedLine
        self.x = (0 if self.side == 'w' else 7)
        self.y = (2 if self.name == 'L' else 5)  if name else 0
    def __str__(self) -> str:
        black_bishop = '♝'
        white_bishop = '♗'
        return f"{white_bishop if self.side == 'w' else black_bishop}Bishop"

    direction = Chess.direction[4:]  