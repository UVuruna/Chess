from ImagesDecorators import Decorator

class Chess():
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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# >>> Hash TABLES  --  CORE MECHANIC <<<
    TakenDict = {}
    PromoteDict = {}
    Check = {}
    AllActions_W = {'move':[],'take':[],'defend':[],'attack':[],'passive_move':[]}
    AllActions_B = {'move':[],'take':[],'defend':[],'attack':[],'passive_move':[]}

    # >>> STATIC Dictionaries <<<
    def emptyTableDict():  
        emptyTableDict = {}
        for x in range(1,9):
            for y in range(1,9):
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
                notationTableDict[x+1,y+1] = NotationTable[x][y]
        return notationTableDict
    NotationTableDict = notationTableDict()
    
    # >>> DYNAMIC Dictionaries <<<
    #@Decorator.countExecutionMethod
    def piecesDict():
        piecesDict = {}
        for i in Chess.pieces:
            piecesDict[i.getXY()] = i
        return piecesDict
    
    #@Decorator.countExecutionMethod
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

    