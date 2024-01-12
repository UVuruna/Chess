from chess import Chess
from actions import Actions

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
        self.x = (1 if self.side == 'w' else 6)
        self.y = Pawn.Name.index(self.name)  if name else 0
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