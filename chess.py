from abc import ABC
import copy


class Chess(ABC):
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Shared Initialization <<<
    pieces = [] 
    def __init__(self,side,move=set(),take=set(),defend=set(),Defender=False) -> None:
        super().__init__()
        self.side = side
        self.move=move
        self.take=take
        self.defend=defend
        self.Defender=Defender
        self.actionsCounter =0
        Chess.pieces.append(self)
        Chess.MovesDict[self] = 0

        


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Hash TABLES  --  CORE MECHANIC <<<
    MovesDict = {}
    TakenDict = {}
    PromoteDict = {}
    Check = {}
    AllActions_W = {'move':set(),'take':set(),'defend':set(),'attack':set(),'passive_move':set()}
    AllActions_B = {'move':set(),'take':set(),'defend':set(),'attack':set(),'passive_move':set()}

    def countExecutionMethod(method):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1
            print(f"{method}Ponavlja se {wrapper.counter}. put")
            return method(*args, **kwargs)
        wrapper.counter = 0
        return wrapper

    # >>> STATIC Dictionaries <<<
    def emptyTableDict():  
        emptyTableDict = {}
        for x in range(8):
            for y in range(8):
                emptyTableDict[x,y] = ''
        return emptyTableDict
    EmptyTableDict = emptyTableDict()
       
    def notationTableDict():
        def notationTable():
            rowX = [chr(i) for i in range(ord('A'),ord('I'))]
            colY = [str(i) for i in range(1,9)]
            return [[(rowX[y]+colY[x]) for y in range(8)] for x in range(8)]
        
        NotationTable = notationTable()
        notationTableDict = {}
        for x in range(8):
            for y in range(8):
                notationTableDict[x,y] = NotationTable[x][y]
        return notationTableDict
    NotationTableDict = notationTableDict()
    
    # >>> DYNAMIC Dictionaries <<<

    #@countExecutionMethod
    def piecesDict():
        piecesDict = {}
        for i in Chess.pieces:
            piecesDict[i.getXY()] = i
        return piecesDict
    
    @countExecutionMethod
    def currentTableDict():
        currentTableDict = Chess.EmptyTableDict.copy()
        piecesDict = Chess.piecesDict()

        for k in piecesDict.keys():
            currentTableDict[k] = piecesDict[k]
        return currentTableDict

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Moves - Game Mechanic <<<
    direction = ['U','D','L','R','UL','UR','DL','DR']  
    def incrementation(self,path):
        if path == Chess.direction[0]:
            self.x +=1
            return self.x,self.y
        elif path == Chess.direction[1]:
            self.x -=1
            return self.x,self.y
        elif path == Chess.direction[2]:
            self.y -=1
            return self.x,self.y
        elif path == Chess.direction[3]:
            self.y +=1
            return self.x,self.y
        elif path == Chess.direction[4]:
            self.x +=1 ; self.y -=1
            return self.x,self.y
        elif path == Chess.direction[5]:
            self.x +=1 ; self.y +=1
            return self.x,self.y
        elif path == Chess.direction[6]:
            self.x -=1 ; self.y -=1
            return self.x,self.y
        elif path == Chess.direction[7]:
            self.x -=1 ; self.y +=1
            return self.x,self.y
    
    # Getter
    def getXY(self): 
        return self.x,self.y
    # Setter
    def setXY(self,xy):
        self.x,self.y = xy
    
    #symbols = '☀☘☛☥☦☯♋♻♺⚔🗡️🠊🢂⚜⛌🢣⚔⛦⛥⛤⛧⛨✚✟✡✰❌❎❭❯❱➔➩➵➸➼⭕⭐🕊🗙'
    #arrow = '➔'
    #sword = '🗙'
    # Setter #1
    def Move(self,tableDict,square):
        PossibleLines = self.possibleMoves(tableDict)[0]
        if square in PossibleLines:
            position = Chess.NotationTableDict[self.getXY()]
            self.x,self.y = square
            Chess.MovesDict[self] +=1
            transcript = f"{str(self)[1:]} {position} move {Chess.NotationTableDict[square]}\n"   
            moveOutput = f"{str(self).ljust(8)}{(position.ljust(5)+'➔').ljust(8)}{Chess.NotationTableDict[square]}"
            return moveOutput,transcript
    # Setter #2 
    def Take(self,tableDict,obj,moveCounter):
        PossibleTake = self.possibleMoves(tableDict)[1]
        if obj.getXY() in PossibleTake:
            position = Chess.NotationTableDict[self.getXY()]
            self.x,self.y = obj.getXY()
            if self not in Chess.TakenDict:
                Chess.TakenDict[self] = {}
            Chess.TakenDict[self][moveCounter+1] = obj
            Chess.MovesDict[self] +=1
            transcript = f"{str(self)[1:]} {position} took {Chess.NotationTableDict[obj.getXY()]} {str(obj)[1:]}\n"  
            moveOutput = f"{str(self).ljust(8)}{(position.ljust(4)+'❌').ljust(7)}{Chess.NotationTableDict[obj.getXY()]} {obj}"
            Chess.pieces.remove(obj)
            return moveOutput,transcript 
    
    #@countExecutionMethod
    def possibleMoves(self,tableDict):
        def square(Self):
            return tableDict[Self.x,Self.y]
        
        possibleMoveAttack_List = []
        possibleTake_List = []
        possibleDefend_List = []
        
        for dir in self.direction:
            possMove = copy.deepcopy(self)
            while possMove.insideBorder(): 
                possMove.incrementation(dir)
                if possMove.insideBorder() and square(possMove) == '':
                    possibleMoveAttack_List.append(possMove.getXY())
                    if possMove.type == 'Archer':
                        None
                    else:
                        break
                elif possMove.insideBorder() and possMove.side !=square(possMove).side:
                    possibleTake_List.append(possMove.getXY())
                    break
                elif possMove.insideBorder() and possMove.side ==square(possMove).side:
                    possibleDefend_List.append(possMove.getXY())
                    break
                else:
                    break
                         
        return possibleMoveAttack_List, possibleTake_List, possibleDefend_List, possibleMoveAttack_List
    
    def insideBorder(self):
        return (self.x <= 7 and self.x >= 0) and (self.y <= 7 and self.y >= 0)