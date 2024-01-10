from chess import Chess

class Actions(Chess):
    
    def Move(self,square):
        if square in self.move: # ---------------------------------------------------- Work - Setter ------------------------------------------
            tablePosition_OLD = Chess.NotationTableDict[self.getXY()]
            tablePosition_NEW = Chess.NotationTableDict[square]
            self.setXY(square)
            self.actionsCounter +=1 # ---------------------------------------------------------------------------------------------------------

            transcript = f"{str(self)[1:]} {tablePosition_OLD} move {tablePosition_NEW}\n" # -------- Output - Print --------------------------
            moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(5)+'➔').ljust(8)}{tablePosition_NEW}" 
            return moveOutput,transcript #-----------------------------------------------------------------------------------------------------

    def Take(self,enemyXY,tableDict,moveCounter):
        if enemyXY in self.take: # ---------------------------------------------------- Work - Setter -----------------------------------------
            enemy = tableDict[enemyXY]
            tablePosition_OLD = Chess.NotationTableDict[self.getXY()]
            tablePosition_NEW = Chess.NotationTableDict[enemyXY]
            self.setXY(enemyXY)
            self.actionsCounter +=1
            Chess.pieces.remove(enemy) # ------------------------------------------------------------------------------------------------------

            if self not in Chess.TakenDict: # ------------------------------------------ Not Necessary ----------------------------------------
                Chess.TakenDict[self] = {}
            Chess.TakenDict[self][moveCounter+1] = enemy # ------------------------------------------------------------------------------------
             
            transcript = f"{str(self)[1:]} {tablePosition_OLD} took {tablePosition_NEW} {str(enemy)[1:]}\n" # --------- Output - Print --------
            moveOutput = f"{str(self).ljust(8)}{(tablePosition_OLD.ljust(4)+'❌').ljust(7)}{tablePosition_NEW} {enemy}"
            return moveOutput,transcript #-----------------------------------------------------------------------------------------------------

    def Castling(self,rook):
        if self.castling and rook.castling: # ---------------------------------------------------- Work - Setter ------------------------------
            self.y -= 2 if rook.name=='L' else -2
            rook.y += 3 if rook.name=='L' else -2
            self.actionsCounter +=1
            rook.actionsCounter +=1 # ---------------------------------------------------------------------------------------------------------

            posSide = 'Queenside:' if rook.name=='L' else 'Kingside:' # ------------------------- Output - Print ------------------------------
            pieceSide = 'black\n' if self.side=='b' else 'white\n'
            transcript = f"{posSide} {pieceSide}" 
            moveOutput = f"{posSide.ljust(11)}{self} ⚜ {rook}"
            return moveOutput,transcript # ----------------------------------------------------------------------------------------------------
    
    
