from ChessParent import Chess,Actions
from PiecesParent import *
from ImagesDecorators import Import
import copy

class King(Warrior):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<   
    def __init__(self,side) -> None:
        super().__init__(side)
        self.check = set()
        self.checkLine = set()
        self.castling = False
        self.x = (1 if self.side == 'w' else 8)
        self.y = 5
 
    def __str__(self) -> str:
        return f"{Import.whiteKing if self.side == 'w' else Import.blackKing}King"

class Queen(Archer):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side)
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = 4
        
    def __str__(self) -> str:
        return f"{Import.whiteQueen if self.side == 'w' else Import.blackQueen}Queen"

class Rook(Archer):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    def __init__(self,side,name=None) -> None:
        super().__init__(side)
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (1 if self.name == 'L' else 8)
        self.direction = Actions.direction[:4]

    def __str__(self) -> str:
        return f"{Import.whiteRook if self.side =='w' else Import.blackRook}Rook"        

class Bishop(Archer):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side)
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (3 if self.name == 'L' else 6)
        self.direction = Actions.direction[4:] 
        
    def __str__(self) -> str:
        return f"{Import.whiteBishop if self.side == 'w' else Import.blackBishop}Bishop"

class Knight(Warrior):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side)
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (2 if self.name == 'L' else 7)
        
    def __str__(self) -> str:
        return f"{Import.whiteKnight if self.side == 'w' else Import.blackKnight}Knight"

    direction = ['U+R','UR+','U+L','UL+','D+R','DR+','D+L','DL+']  
    def incrementation(self, path):
        if path == self.direction[0]:
            self.x +=2 ; self.y +=1
        elif path == self.direction[1]:
            self.x +=1 ; self.y +=2
        elif path == self.direction[2]:
            self.x +=2 ; self.y -=1
        elif path == self.direction[3]:
            self.x +=1 ; self.y -=2
        elif path == self.direction[4]:
            self.x -=2 ; self.y +=1
        elif path == self.direction[5]:
            self.x -=1 ; self.y +=2
        elif path == self.direction[6]:
            self.x -=2 ; self.y -=1
        elif path == self.direction[7]:
            self.x -=1 ; self.y -=2
        return self.x,self.y

class Pawn(Chess,Actions):   
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    Name = ['L1','L2','L3','CL','CR','R3','R2','R1']  
    def __init__(self,side,name=None) -> None:
        super().__init__(side)
        self.name = name
        self.passive_move = set()
        self.attack = set()
        self.enpassant = None
        self.x = (2 if self.side == 'w' else 7)
        self.y = Pawn.Name.index(self.name)+1
        if self.side == 'w':
            self.directionMove = Actions.direction[0]
            self.directionAttack = Actions.direction[4:6]
        else:
            self.directionMove = Actions.direction[1]
            self.directionAttack = Actions.direction[6:]

    def __str__(self) -> str:
        return f"{Import.whitePawn if self.side == 'w' else Import.blackPawn}Pawn"

    def AllActions(self,tableDict):
        selfCopy = copy.copy(self)
        tries = 2 if self.actionsCounter==0 else 1
        selfCopy.x,selfCopy.y = self.getXY()
        while selfCopy.XY_InsideBorder(): # Nema for jer Pion ima samo jedan pravac za pasivno kretanje
            selfCopy.incrementation(self.directionMove)
            if tries == 0: 
                break
            elif selfCopy.XY_InsideBorder() and selfCopy.XY_Content(tableDict) =='':
                self.passive_move.add(selfCopy.getXY())
                tries -= 1
            else: 
                break
        for dir in self.directionAttack:
            selfCopy.x,selfCopy.y = self.getXY()
            while selfCopy.XY_InsideBorder():
                selfCopy.incrementation(dir)
                if selfCopy.XY_InsideBorder():
                    if selfCopy.XY_Content(tableDict) !='':
                        if selfCopy.side !=selfCopy.XY_Content(tableDict).side:
                            self.take.add(selfCopy.getXY())
                            enemy = tableDict[selfCopy.getXY()]
                            if hasattr(enemy,'check'):
                                enemy.check.add(self.getXY())
                                Chess.Check=True
                            break
                        elif selfCopy.side ==selfCopy.XY_Content(tableDict).side:
                            self.defend.add(selfCopy.getXY())
                            break
                    else:
                        self.attack.add(selfCopy.getXY())
                        break
                else:
                    break
        del selfCopy