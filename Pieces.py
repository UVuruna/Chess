from ChessParent import Chess
from Actions import Actions

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
        white_king = '♔'
        black_king = '♚'
        return f"{white_king if self.side == 'w' else black_king}King"

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
            black_queen = '♛'
            white_queen = '♕'
            return f"{white_queen if self.side == 'w' else black_queen}Queen"

class Rook(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    def __init__(self,side,name=None) -> None:
        super().__init__(side,move=set(),take=set(),defend=set(),Defender=False)
        self.type = 'Archer'
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (1 if self.name == 'L' else 8)
        self.direction = Chess.direction[:4]

    def __str__(self) -> str:
        white_rook = '♖'
        black_rook = '♜'
        return f"{white_rook if self.side =='w' else black_rook}Rook"        

class Bishop(Chess,Actions):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side,move=set(),take=set(),defend=set(),Defender=False)
        self.type = 'Archer'
        self.name = name
        self.x = (1 if self.side == 'w' else 8)
        self.y = (3 if self.name == 'L' else 6)
        self.direction = Chess.direction[4:] 
        
    def __str__(self) -> str:
        black_bishop = '♝'
        white_bishop = '♗'
        return f"{white_bishop if self.side == 'w' else black_bishop}Bishop"

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
        white_knight = '♘'
        black_knight = '♞'
        return f"{white_knight if self.side == 'w' else black_knight}Knight"

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
            self.directionMove = Chess.direction[0]
            self.directionAttack = Chess.direction[4:6]
        else:
            self.directionMove = Chess.direction[1]
            self.directionAttack = Chess.direction[6:]

    def __str__(self) -> str:
        white_pawn = '♙'
        black_pawn = '♟'
        return f"{white_pawn if self.side == 'w' else black_pawn}Pawn"      