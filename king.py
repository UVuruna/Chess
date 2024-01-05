from chess import Chess
from rook import Rook

class King(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<   
    def __init__(self, side) -> None:
        super().__init__(side)
        self.type = 'Warrior'
        self.x = (0 if self.side == 'w' else 7)
        self.y = 4
    def __str__(self) -> str:
        white_king = '♔'
        black_king = '♚'
        return f"{white_king if self.side == 'w' else black_king}King"        

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<   
    def possibleMoves(self, tableDict):
         return super().possibleMoves(tableDict)
       
    def castlingCheck(self,tableDict):
        kingsideWhite, queensideWhite, kingsideBlack, queensideBlack = 0,0,0,0

        if Chess.MovesDict[self]==0:
            for ownRook in Chess.pieces:
                if isinstance(ownRook,Rook) and ownRook.side==self.side and Chess.MovesDict[ownRook]==0:
                    if self.side=='w' and ownRook.name=='R' and tableDict[(0,5)]=='' and tableDict[(0,6)]=='':
                        kingsideWhite = 1
                    elif self.side=='w' and ownRook.name=='L' and tableDict[(0,1)]=='' and tableDict[(0,2)]=='' and tableDict[(0,3)]=='':
                        queensideWhite = 1   
                    elif self.side=='b' and ownRook.name=='R' and tableDict[(7,5)]=='' and tableDict[(7,6)]=='':
                        kingsideBlack = 1
                    elif self.side=='b' and ownRook.name=='L' and tableDict[(7,1)]=='' and tableDict[(7,2)]=='' and tableDict[(7,3)]=='':
                        queensideBlack = 1
            return kingsideWhite, queensideWhite, kingsideBlack, queensideBlack
    
    #castle = '⚜'
    def castling(self,obj,kingWh,queenWh,kingBl,queenBl):
        k = 'Kingside:'
        q = 'Queenside:'
        if obj.name == 'L':
            if queenWh == 1: # Duga rokada - Queenside castling
                self.x = 0 ; self.y = 2
                obj.x = 0 ; obj.y = 3
                Chess.MovesDict[self]+=1 ; Chess.MovesDict[obj]+=1
                transcript = f"{q} white\n"
                moveOutput = f"{q.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript
            elif queenBl == 1: # Duga rokada - Queenside castling
                self.x = 7 ; self.y = 2
                obj.x = 7 ; obj.y = 3
                Chess.MovesDict[self]+=1 ; Chess.MovesDict[obj]+=1
                transcript = f"{q} black\n"
                moveOutput = f"{q.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript
        else:              
            if kingBl == 1: # Kratka rokada - Kingside castling
                self.x = 7 ; self.y = 6
                obj.x = 7 ; obj.y = 5
                Chess.MovesDict[self]+=1 ; Chess.MovesDict[obj]+=1
                transcript = f"{k} black\n"
                moveOutput = f"{k.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript           
            elif kingWh == 1: # Kratka rokada - Kingside castling
                self.x = 0 ; self.y = 6
                obj.x = 0 ; obj.y = 5
                Chess.MovesDict[self]+=1 ; Chess.MovesDict[obj]+=1
                transcript = f"{k} white\n"
                moveOutput = f"{k.ljust(11)}{self} ⚜ {obj}"
                return moveOutput,transcript