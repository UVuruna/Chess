from chess import Chess
import copy

class Pawn(Chess):   
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<< 
    Name = ['L1','L2','L3','CL','CR','R3','R2','R1']  
    def __init__(self,side,name=None,attack=None) -> None:
        super().__init__(side,move=None,take=None,defend=None,Defender=None)
        self.type = 'Warrior'
        self.name = name
        self.attack = attack
        self.x = (1 if self.side == 'w' else 6)
        self.y = Pawn.Name.index(self.name)  if name else 0

    def __str__(self) -> str:
        white_pawn = '♙'
        black_pawn = '♟'
        return f"{white_pawn if self.side == 'w' else black_pawn}Pawn" 


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<   
    def possibleMoves(self,TableDict):
        
        def polje(content):
            return TableDict[content.x,content.y]
        
        # Za razliku od ostalih PION ima razlicite PETLJE za JEDENJE i KRETANJE, jer to radi u razlicitim smerovima
        # Takodje kretanje zavisi od strane na kojoj se nalazi za razliku od ostalih FIGURA, zato postoji ovaj IF-ELSE
        if self.side == 'w':
            self.directionMove = Chess.direction[0]
            self.directionAttack = Chess.direction[4:6]
        elif self.side == 'b':
            self.directionMove = Chess.direction[1]
            self.directionAttack = Chess.direction[6:]
        # Varijabla TRIES sluzi jer PION u odredjenim slucajevima moze da skoci 2 polja, dok u vecini moze samo 1 polje kao 1 korak
        if (self.side == 'w' and self.x == 1) or (self.side == 'b' and self.x == 6):
            tries = 2
        else:
            tries = 1

        possibleMove_List = []
        possibleTake_List = []
        possibleDefend_List = []
        possibleAttack_List = []

        for dir in self.directionMove:
            possMove = copy.deepcopy(self)
            while possMove.insideBorder(): 
                possMove.incrementation(dir)
                if tries == 0:
                    break
                elif possMove.insideBorder() and polje(possMove) =='':
                    possibleMove_List.append(possMove.position())
                    tries -= 1
                else:
                    break 

        for dir in self.directionAttack:
            possMove = copy.deepcopy(self)
            while possMove.insideBorder():
                possMove.incrementation(dir)
                if possMove.insideBorder():
                    if polje(possMove) !='' and possMove.side !=polje(possMove).side:
                        possibleTake_List.append(possMove.position())
                        break
                    elif polje(possMove) !='' and possMove.side ==polje(possMove).side:
                        possibleDefend_List.append(possMove.position())
                        break
                    elif polje(possMove) =='':
                        possibleAttack_List.append(possMove.position())
                        break
                
                else:
                    break 
        return possibleMove_List, possibleTake_List, possibleDefend_List, possibleAttack_List