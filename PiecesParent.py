from ChessParent import *
import copy

class Archer(Chess,Actions):
    def __init__(self, side) -> None:
        super().__init__(side)
        self.move = set()
        self.attack = set()

    def AllActions(self,tableDict):
        selfCopy = copy.copy(self)
        pin=None
        check=None
        for dir in selfCopy.direction:
            possMove,extendedLine = set(),set()
            selfCopy.x,selfCopy.y = self.getXY()
            while selfCopy.XY_InsideBorder(): 
                selfCopy.incrementation(dir)
                if selfCopy.XY_InsideBorder():
                    if selfCopy.XY_Content(tableDict) == '': # -------------------Prazno polje---------------------------------------------------------------
                        if not pin: # ili None ili False
                            if not check: # ili None ili False
                                possMove.add(selfCopy.getXY()) 
                            else:
                                check = False
                                self.attack.add(selfCopy.getXY()) # Ovo se dodaje kada je sah kao da moze tu da se stane zato sto je suprotna ekipa na potezu 
                                break    
                        else:
                            extendedLine.add(selfCopy.getXY()) # ----------------------------------------------------------------------------------------
                    elif selfCopy.side !=selfCopy.XY_Content(tableDict).side: # -------Protivnicka figura ---------------------------------------------------
                        if not pin: # ili None ili False
                            enemy = tableDict[selfCopy.getXY()]
                            self.take.add(selfCopy.getXY())                               
                            try:                                  # Ovo ako jeste kralj opet se nema BREAK jer mora da spreci kralja da stane na pozicije iza
                                enemy.check.add(self.getXY())
                                enemy.checkLine.update(possMove)
                                Chess.Check=True
                                self.move.update(possMove)
                                check=True
                            except AttributeError:
                                if check is None and pin is None: # Ovo je ako je protivnik, a nije kralj onda krece Extended Line da se proveri da li je iza njega Kralj
                                    pin = enemy
                                else:
                                    break 
                        else:
                            if hasattr(tableDict[selfCopy.getXY()],'check'):
                                pin.pinned.extend([(extendedLine | possMove) , {self.getXY(),}])
                                pin = False
                                self.move.update(possMove) 
                                break
                            else:
                                pin=None
                                self.move.update(possMove)
                                break # -------------------------------------------------------------------------------------------------------------------

                    elif selfCopy.side ==selfCopy.XY_Content(tableDict).side: # ----------Nasa figura-------------------------------------------------------
                        if not pin:
                            if not check:
                                self.defend.add(selfCopy.getXY())
                                self.move.update(possMove)
                                break
                            else:
                                check = False
                                self.defend.add(selfCopy.getXY())
                                break
                        else:
                            pin=None
                            self.move.update(possMove) 
                            break # -----------------------------------------------------------------------------------------------------------------------
                else:
                    pin=None
                    self.move.update(possMove)
                    break
        else:
            del selfCopy

class Warrior(Chess,Actions):
    def __init__(self, side) -> None:
        super().__init__(side)
        self.move = set()

    def AllActions(self,tableDict):
        selfCopy = copy.copy(self)
        for dir in selfCopy.direction:
            selfCopy.x,selfCopy.y = self.getXY()
            while selfCopy.XY_InsideBorder(): 
                selfCopy.incrementation(dir)
                if selfCopy.XY_InsideBorder():
                    if selfCopy.XY_Content(tableDict) == '': # -------------------Prazno polje---------------------------------------------------------------
                        self.move.add(selfCopy.getXY())
                        break  # ----------------------------------------------------------------------------------------------------------------------------
                    elif selfCopy.side !=selfCopy.XY_Content(tableDict).side: # -------Protivnicka figura --------------------------------------------------
                        self.take.add(selfCopy.getXY())
                        enemy = tableDict[selfCopy.getXY()]                             
                        if hasattr(enemy,'check'):
                            enemy.check.add(self.getXY())
                            Chess.Check=True
                        break # -----------------------------------------------------------------------------------------------------------------------------
                    elif selfCopy.side ==selfCopy.XY_Content(tableDict).side: # ----------Nasa figura-------------------------------------------------------
                        self.defend.add(selfCopy.getXY())
                        break # -----------------------------------------------------------------------------------------------------------------------------
                else:
                    break
        else:
            del selfCopy