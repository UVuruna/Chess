from chess import Chess

class Actions():
    
    def Move(self,newXY):
        tablePosition_OLD = Chess.NotationTableDict[self.getXY()] # ------------------------- Work - Setter -------------------------------
        tablePosition_NEW = Chess.NotationTableDict[newXY]
        self.setXY(newXY) 
        self.actionsCounter +=1 # ---------------------------------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------- Output - Print ------------------------------
        transcript = f"{str(self)[1:]} {tablePosition_OLD} move {tablePosition_NEW}\n" 
        moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(5)+'➔').ljust(8)}{tablePosition_NEW}" 
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
        moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(4)+'❌').ljust(7)}{tablePosition_NEW} {enemy}"
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
        moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(4)+'❌').ljust(7)}{tablePosition_NEW} {enemy} {tablePosition_ENEMY}"
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
        moveOutput = f"{posSide.ljust(11)}{self} ⚜ {rook}"
        return moveOutput,transcript # ----------------------------------------------------------------------------------------------------