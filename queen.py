from chess import Chess

class Queen(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self, side, name=None) -> None:
        super().__init__(side)
        self.type = 'Archer'
        self.name = name
        self.x = (0 if self.side == 'w' else 7)
        self.y = 3
    def __str__(self) -> str:
            black_queen = '♛'
            white_queen = '♕'
            return f"{white_queen if self.side == 'w' else black_queen}Queen"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
    def possibleMoves(self, tableDict):
         return super().possibleMoves(tableDict)