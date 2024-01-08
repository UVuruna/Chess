from chess import Chess

class Knight(Chess):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Creating Object <<<
    def __init__(self,side,name=None) -> None:
        super().__init__(side,move=None,take=None,defend=None,Defender=None)
        self.type = 'Warrior'
        self.name = name
        self.x = (0 if self.side == 'w' else 7)
        self.y = (1 if self.name == 'L' else 6)  if name else 0
    def __str__(self) -> str:
        white_knight = '♘'
        black_knight = '♞'
        return f"{white_knight if self.side == 'w' else black_knight}Knight"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
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