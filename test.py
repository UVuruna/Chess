def possibleMovesWarrior(Self,tableDict,possibleMoves,possibleTakes,possibleDefends):
    Self_Copy = copy.deepcopy(Self)
    for dir in Self_Copy.direction:
        Self_Copy.x,Self_Copy.y = Self.position()
        while AI.insideBorder(Self_Copy): 
            Self_Copy.incrementation(dir)
            if AI.insideBorder(Self_Copy):
                if AI.square(Self_Copy,tableDict) == '': # -------------------Prazno polje---------------------------------------------------------------
                    possibleMoves.update(Self_Copy.position())
                    break  # ----------------------------------------------------------------------------------------------------------------------------

                elif Self_Copy.side !=AI.square(Self_Copy,tableDict).side: # -------Protivnicka figura --------------------------------------------------
                    possibleTakes.add(Self_Copy.position())                               
                    if isinstance(tableDict[Self_Copy.position()],King):
                        Chess.Check[Self.position()]=None
                    break # -----------------------------------------------------------------------------------------------------------------------------

                elif Self_Copy.side ==AI.square(Self_Copy,tableDict).side: # ----------Nasa figura-------------------------------------------------------
                    possibleDefends.add(Self_Copy.position())
                    break # -----------------------------------------------------------------------------------------------------------------------------
            else:
                break
    else:
        del Self_Copy
        AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,Defenders)