from ImagesDecorators import Decorator,Import

class Chess():
#------------------------------------------------------------------------------------------------------------------------------------------  
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

#------------------------------------------------------------------------------------------------------------------------------------------ 
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

#------------------------------------------------------------------------------------------------------------------------------------------ 
# >>> Moves - Game Mechanic <<<
class Actions():
    direction = ['U','D','L','R','UL','UR','DL','DR']
    # Getter
    def getXY(self): 
        return self.x,self.y
    # Setter
    def setXY(self,xy):
        self.x,self.y = xy
 
    def incrementation(self,path):
        if path == Actions.direction[0]:
            self.x +=1
            return self.x,self.y
        elif path == Actions.direction[1]:
            self.x -=1
            return self.x,self.y
        elif path == Actions.direction[2]:
            self.y -=1
            return self.x,self.y
        elif path == Actions.direction[3]:
            self.y +=1
            return self.x,self.y
        elif path == Actions.direction[4]:
            self.x +=1 ; self.y -=1
            return self.x,self.y
        elif path == Actions.direction[5]:
            self.x +=1 ; self.y +=1
            return self.x,self.y
        elif path == Actions.direction[6]:
            self.x -=1 ; self.y -=1
            return self.x,self.y
        elif path == Actions.direction[7]:
            self.x -=1 ; self.y +=1
            return self.x,self.y
#------------------------------------------------------------------------------------------------------------------------------------------    
    def Move(self,newXY):
        tablePosition_OLD = Chess.NotationTableDict[self.getXY()] # ------------------------- Work - Setter -------------------------------
        tablePosition_NEW = Chess.NotationTableDict[newXY]
        self.setXY(newXY) 
        self.actionsCounter +=1 # ---------------------------------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------- Output - Print ------------------------------
        transcript = f"{str(self)[1:]} {tablePosition_OLD} move {tablePosition_NEW}\n" 
        moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(5)+Import.moveSign).ljust(8)}{tablePosition_NEW}" 
        return moveOutput,transcript #-----------------------------------------------------------------------------------------------------

    def Take(self,enemyXY,tableDict,moveCounter):
        enemy = tableDict[enemyXY] # ---------------------------------------------------- Work - Setter -----------------------------------
        tablePosition_OLD = Chess.NotationTableDict[self.getXY()] 
        tablePosition_NEW = Chess.NotationTableDict[enemyXY] 
        self.setXY(enemyXY)
        self.actionsCounter +=1
        Chess.pieces.remove(enemy) # ------------------------------------------------------------------------------------------------------

        if self not in Chess.TakenDict: # ------------------------------------------ Not Necessary ----------------------------------------
            Chess.TakenDict[self] = {}
        Chess.TakenDict[self][moveCounter+1] = enemy # ------------------------------------------------------------------------------------

        # ---------------------------------------------------------------- Output - Print -------------------------------------------------
        transcript = f"{str(self)[1:]} {tablePosition_OLD} took {tablePosition_NEW} {str(enemy)[1:]}\n" 
        moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(4)+Import.takeSign).ljust(7)}{tablePosition_NEW} {enemy}"
        return moveOutput,transcript #-----------------------------------------------------------------------------------------------------

    def enPassantTake(self,newXY,enemyXY,tableDict,moveCounter):
        enemy = tableDict[enemyXY] # ---------------------------------------------------- Work - Setter -----------------------------------
        tablePosition_OLD = Chess.NotationTableDict[self.getXY()] 
        tablePosition_ENEMY = Chess.NotationTableDict[enemyXY]
        self.setXY(newXY)
        self.actionsCounter +=1 
        Chess.pieces.remove(enemy) # ------------------------------------------------------------------------------------------------------

        if self not in Chess.TakenDict: # ------------------------------------------ Not Necessary ----------------------------------------
            Chess.TakenDict[self] = {}
        Chess.TakenDict[self][moveCounter+1]=enemy # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------- Output - Print ----------------------------------------
        tablePosition_NEW = Chess.NotationTableDict[newXY]
        transcript = f"{str(self)[1:]} {tablePosition_OLD} take {tablePosition_NEW} {str(enemy)[1:]} {tablePosition_ENEMY}\n"
        moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(4)+Import.takeSign).ljust(7)}{tablePosition_NEW} {enemy} {tablePosition_ENEMY}"
        return moveOutput,transcript #-----------------------------------------------------------------------------------------------------

    def Castling(self,rook):
        self.y -= 2 if rook.name=='L' else -2 # ---------------------------------------------------- Work - Setter ------------------------
        rook.y += 3 if rook.name=='L' else -2
        self.castling = False
        self.actionsCounter +=1
        rook.actionsCounter +=1 # ---------------------------------------------------------------------------------------------------------

        posSide = 'Queenside:' if rook.name=='L' else 'Kingside:' # ------------------------- Output - Print ------------------------------
        pieceSide = 'black\n' if self.side=='b' else 'white\n'
        transcript = f"{posSide} {pieceSide}" 
        moveOutput = f"{posSide.ljust(11)}{self} {Import.castlingSign} {rook}"
        return moveOutput,transcript # ----------------------------------------------------------------------------------------------------   