from ChessParent import Chess,Actions
from ImagesDecorators import Import

class King(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<   
    def __init__(self,side,castling=False) -> None:
        super().__init__(side,move=set(),take=set(),defend=set())
        self.type = 'Warrior'
        self.castling = castling
        self.x = (1 if self.side == 'w' else 8)
        self.y = 5
 
    def __str__(self) -> str:
        return f"{Import.whiteKing if self.side == 'w' else Import.blackKing}King"

class Queen(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side,move=set(),take=set(),defend=set(),Defender=False)
        self.type = 'Archer'
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = 4
        
    def __str__(self) -> str:
        return f"{Import.whiteQueen if self.side == 'w' else Import.blackQueen}Queen"

class Rook(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    def __init__(self,side,name=None) -> None:
        super().__init__(side,move=set(),take=set(),defend=set(),Defender=False)
        self.type = 'Archer'
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (1 if self.name == 'L' else 8)
        self.direction = Actions.direction[:4]

    def __str__(self) -> str:
        return f"{Import.whiteRook if self.side =='w' else Import.blackRook}Rook"        

class Bishop(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side,move=set(),take=set(),defend=set(),Defender=False)
        self.type = 'Archer'
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (3 if self.name == 'L' else 6)
        self.direction = Actions.direction[4:] 
        
    def __str__(self) -> str:
        return f"{Import.whiteBishop if self.side == 'w' else Import.blackBishop}Bishop"

class Knight(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side,move=set(),take=set(),defend=set(),Defender=False)
        self.type = 'Warrior'
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (2 if self.name == 'L' else 7)
        
    def __str__(self) -> str:
        return f"{Import.whiteKnight if self.side == 'w' else Import.blackKnight}Knight"

    direction = ['U+R','UR+','U+L','UL+','D+R','DR+','D+L','DL+']  
    def incrementation(self, path):
        if path == self.direction[0]:
            self.x +=2 ; self.y +=1
            return self.x,self.y
        elif path == self.direction[1]:
            self.x +=1 ; self.y +=2
            return self.x,self.y
        elif path == self.direction[2]:
            self.x +=2 ; self.y -=1
            return self.x,self.y
        elif path == self.direction[3]:
            self.x +=1 ; self.y -=2
            return self.x,self.y
        elif path == self.direction[4]:
            self.x -=2 ; self.y +=1
            return self.x,self.y
        elif path == self.direction[5]:
            self.x -=1 ; self.y +=2
            return self.x,self.y
        elif path == self.direction[6]:
            self.x -=2 ; self.y -=1
            return self.x,self.y
        elif path == self.direction[7]:
            self.x -=1 ; self.y -=2
            return self.x,self.y

class Pawn(Chess,Actions):   
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    Name = ['L1','L2','L3','CL','CR','R3','R2','R1']  
    def __init__(self,side,name=None,passiv_move=None,attack=None) -> None:
        super().__init__(side,move=set(),take=set(),defend=set(),Defender=False)
        self.type = 'Warrior'
        self.name = name
        self.passiv_move = passiv_move if passiv_move is not None else set()
        self.attack = attack if attack is not None else set()
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