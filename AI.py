from tkinter import *
import copy
from chess import Chess
from Pieces import *
import time


class AI():

    def countExecutionMethod(method):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1
            print(f"{method}Ponavlja se {wrapper.counter}. put")
            return method(*args, **kwargs)
        wrapper.counter = 0
        return wrapper

    def ClearPossibleActions(everything=True,check=True,TwoCheck=False):
        def side(piece,TwoCheck):
            if not TwoCheck:
                return True
            else:
                return piece.side!=TwoCheck and not isinstance(piece,King)

        if TwoCheck!='w': 
            for k in Chess.AllActions_W.keys():
                Chess.AllActions_W[k].clear()
        if TwoCheck!='b':
            for k in Chess.AllActions_B.keys():
                Chess.AllActions_B[k].clear()
        if check:
            Chess.Check.clear()
        if everything:
            for p in Chess.pieces:
                if side(p,TwoCheck):
                    if not isinstance(p,Pawn):
                        p.move.clear()
                    else:
                        p.attack.clear() ; p.passiv_move.clear()
                    p.take.clear() ; p.defend.clear() ; p.Defender=False

    def insideBorder(Self):
        return (Self.x <= 7 and Self.x >= 0) and (Self.y <= 7 and Self.y >= 0)
    def square(Self,tableDict):
        return tableDict[Self.x,Self.y]

    #@countExecutionMethod
    def updatingAttributes(Self,m,t,d,De=None,a=None):
        if De:
            defender = De[0]
            defender.Defender = True
            if not defender.move:
                if not isinstance(defender,Pawn):
                    defender.move.update(De[1])
                else:
                    defender.passiv_move.update(De[1])
                    defender.attack.update(De[1])
                defender.take.update([Self.getXY()])
            else: 
                if not isinstance(defender,Pawn):
                     defender.move &= De[1]
                else: # ovo ne moze da se desi sa Pawn jer se ubaciju posle Archera u START GAME (ali neka ostane)
                    defender.passiv_move &= De[1]
                    defender.attack &= De[1]
                defender.take &= set([Self.getXY()])

        if Self.Defender is False:
            Self.take.update(t)
            Self.defend.update(d)
            if not isinstance(Self,Pawn):
                Self.move.update(m)
            else:
                Self.passiv_move.update(m)
                Self.attack.update(a)
        else:
            Self.take &= t
            Self.defend.clear()
            if not isinstance(Self,Pawn):
                Self.move &= m
            else:
                Self.passiv_move &= m
                Self.attack &= a

    #@countExecutionMethod 
    def AllActions(Self,tableDict):
        Self_Copy = copy.deepcopy(Self)
        if Self.type == 'Archer':
            AI.AllActionsArcher(Self,Self_Copy,tableDict)
        elif isinstance(Self,Pawn):
            AI.AllActionsPawn(Self,Self_Copy,tableDict)
        else:
            AI.AllActionsWarrior(Self,Self_Copy,tableDict)
    
    #@countExecutionMethod
    def AllActionsArcher(Self,Self_Copy,tableDict):
        possibleMoves = set()
        possibleTakes = set()
        possibleDefends = set()
        Defenders = {}
        for dir in Self_Copy.direction:
            DefenderEnemy=None ; extLine=False ; check=False
            possMove,extendedLine = set(),set()
            Self_Copy.x,Self_Copy.y = Self.getXY()
            while AI.insideBorder(Self_Copy): 
                Self_Copy.incrementation(dir)
                if AI.insideBorder(Self_Copy):
                    if AI.square(Self_Copy,tableDict) == '': # -------------------Prazno polje---------------------------------------------------------------
                        if not extLine:
                            if not check:
                                possMove.add(Self_Copy.getXY()) 
                            else:
                                Self.move.add(Self_Copy.getXY())
                                break    
                        else:
                            extendedLine.add(Self_Copy.getXY()) # ----------------------------------------------------------------------------------------
                    elif Self_Copy.side !=AI.square(Self_Copy,tableDict).side: # -------Protivnicka figura ---------------------------------------------------
                        if not extLine:
                            enemy = tableDict[Self_Copy.getXY()]
                            possibleTakes.add(Self_Copy.getXY())                               
                            if isinstance(enemy,King):
                                check=True
                                Chess.Check[Self.side,Self.getXY(),Self_Copy.getXY()]=possMove
                                possibleMoves.update(possMove)
                            else:
                                if not check:
                                    extLine=True
                                    DefenderEnemy = enemy
                                else:
                                    break
                        else:
                            if isinstance(tableDict[Self_Copy.getXY()],King):
                                Defenders=[DefenderEnemy,(extendedLine|possMove)]
                                possibleMoves.update(possMove) 
                                break
                            else:
                                DefenderEnemy=None
                                possibleMoves.update(possMove)
                                break # -------------------------------------------------------------------------------------------------------------------

                    elif Self_Copy.side ==AI.square(Self_Copy,tableDict).side: # ----------Nasa figura-------------------------------------------------------
                        if not extLine:
                            if not check:
                                possibleDefends.add(Self_Copy.getXY())
                                possibleMoves.update(possMove)
                                break
                            else:
                                Self.defend.add(Self_Copy.getXY())
                                break
                        else:
                            DefenderEnemy=None
                            possibleMoves.update(possMove) 
                            break # -----------------------------------------------------------------------------------------------------------------------
                else:
                    DefenderEnemy=None
                    possibleMoves.update(possMove)
                    break
        else:
            del Self_Copy
            AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,Defenders)

    #@countExecutionMethod
    def AllActionsWarrior(Self,Self_Copy,tableDict):
        possibleMoves = set()
        possibleTakes = set()
        possibleDefends = set()
        for dir in Self_Copy.direction:
            Self_Copy.x,Self_Copy.y = Self.getXY()
            while AI.insideBorder(Self_Copy): 
                Self_Copy.incrementation(dir)
                if AI.insideBorder(Self_Copy):
                    if AI.square(Self_Copy,tableDict) == '': # -------------------Prazno polje---------------------------------------------------------------
                        possibleMoves.add(Self_Copy.getXY())
                        break  # ----------------------------------------------------------------------------------------------------------------------------

                    elif Self_Copy.side !=AI.square(Self_Copy,tableDict).side: # -------Protivnicka figura --------------------------------------------------
                        possibleTakes.add(Self_Copy.getXY())                               
                        if isinstance(tableDict[Self_Copy.getXY()],King):
                            Chess.Check[Self.side,Self.getXY(),Self_Copy.getXY()]=set()
                        break # -----------------------------------------------------------------------------------------------------------------------------

                    elif Self_Copy.side ==AI.square(Self_Copy,tableDict).side: # ----------Nasa figura-------------------------------------------------------
                        possibleDefends.add(Self_Copy.getXY())
                        break # -----------------------------------------------------------------------------------------------------------------------------
                else:
                    break
        else:
            del Self_Copy
            AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends)

    #@countExecutionMethod
    def AllActionsPawn(Self,Self_Copy,tableDict):
        possibleMoves = set()
        possibleTakes = set()
        possibleDefends = set()
        possibleAttacks = set()
        tries = 2 if (Self.side == 'w' and Self.x == 1) or (Self.side == 'b' and Self.x == 6) else 1
        for dir in Self.directionMove:
            Self_Copy.x,Self_Copy.y = Self.getXY()
            while AI.insideBorder(Self_Copy): 
                Self_Copy.incrementation(dir)
                if tries == 0: 
                    break
                elif AI.insideBorder(Self_Copy) and AI.square(Self_Copy,tableDict) =='':
                    possibleMoves.add(Self_Copy.getXY())
                    tries -= 1
                else: 
                    break
        for dir in Self.directionAttack:
            Self_Copy.x,Self_Copy.y = Self.getXY()
            while AI.insideBorder(Self_Copy):
                Self_Copy.incrementation(dir)
                if AI.insideBorder(Self_Copy):
                    if AI.square(Self_Copy,tableDict) !='':
                        if Self_Copy.side !=AI.square(Self_Copy,tableDict).side:
                            possibleTakes.add(Self_Copy.getXY())
                            if isinstance(tableDict[Self_Copy.getXY()],King):
                                Chess.Check[Self.side,Self.getXY(),Self_Copy.getXY()]=set()
                            break
                        elif Self_Copy.side ==AI.square(Self_Copy,tableDict).side:
                            possibleDefends.add(Self_Copy.getXY())
                            break
                    else:
                        possibleAttacks.add(Self_Copy.getXY())
                        break
                else:
                    break
        del Self_Copy            
        AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,None,possibleAttacks)                   

    #@countExecutionMethod
    def PossibleActions(enPassantSquare=None,side=None):
        W_King=None ; B_King=None
        WL_Rook=None ; WR_Rook=None
        BL_Rook=None ; BR_Rook=None
        if Chess.Check:
            numOfAttackers = len(Chess.Check)
            for k,v in Chess.Check.items():
                attackerSide = k[0]
                enemyAttacker = k[1]
                enemyLine = v
                break
           
        else:
            numOfAttackers=0
        for p in Chess.pieces:
            if p.side=='w':
                Chess.AllActions_W['defend'].extend(p.defend)
                if isinstance(p,King):
                    W_King=p    
                else:
                    if isinstance(p,Rook) and p.actionsCounter==0:
                        if p.name=='L':
                            WL_Rook=p
                        else:
                            WR_Rook=p
                    if numOfAttackers ==1 and attackerSide=='b':
                        if not isinstance(p,Pawn):
                            p.move &= enemyLine
                        else:
                            p.passiv_move &= enemyLine
                            p.attack &= enemyLine
                        p.take &= set([enemyAttacker])
                    if not isinstance(p,Pawn):
                        Chess.AllActions_W['move'].extend(p.move)
                    else:
                        if enPassantSquare in p.attack and side!='w':
                            p.take.add(enPassantSquare)
                        Chess.AllActions_W['passive_move'].extend(p.passiv_move)
                        Chess.AllActions_W['attack'].extend(p.attack)
                    Chess.AllActions_W['take'].extend(p.take)
            else:
                Chess.AllActions_B['defend'].extend(p.defend)
                if isinstance(p,King):
                    B_King=p
                else:
                    if isinstance(p,Rook) and p.actionsCounter==0:
                        if p.name=='L':
                            BL_Rook=p
                        else:
                            BR_Rook=p
                    if numOfAttackers ==1 and attackerSide=='w':
                        if not isinstance(p,Pawn):
                            p.move &= enemyLine
                        else:
                            p.passiv_move &= enemyLine
                            p.attack &= enemyLine
                        p.take &= set([enemyAttacker])
                    if not isinstance(p,Pawn):
                        Chess.AllActions_B['move'].extend(p.move)
                    else:
                        if enPassantSquare in p.attack and side!='b':
                            p.take.add(enPassantSquare)
                        Chess.AllActions_B['passive_move'].extend(p.passiv_move)
                        Chess.AllActions_B['attack'].extend(p.attack)
                    Chess.AllActions_B['take'].extend(p.take)       

        W_King.take -= set(Chess.AllActions_B['defend'])
        B_King.take -= set(Chess.AllActions_W['defend'])

        W = W_King.move.copy()
        B = B_King.move.copy()

        W_King.move -= (set(Chess.AllActions_B['move']) | set(Chess.AllActions_B['attack']) | B )
        B_King.move -= (set(Chess.AllActions_W['move']) | set(Chess.AllActions_W['attack']) | W )
        
        if numOfAttackers >1:
            AI.ClearPossibleActions(True,False,attackerSide)

        Chess.AllActions_W['move'].extend(W_King.move)
        Chess.AllActions_W['take'].extend(W_King.take)
        Chess.AllActions_B['move'].extend(B_King.move)
        Chess.AllActions_B['take'].extend(B_King.take)

        return W_King,WL_Rook,WR_Rook,B_King,BL_Rook,BR_Rook

    #@countExecutionMethod
    def castlingCheck(W_King,WL_Rook,WR_Rook,B_King,BL_Rook,BR_Rook):
        W=0 ; B=0
        if W_King.actionsCounter==0:
            W_King.castling=False
            W=0; kingWPos=W_King.getXY()
            if WL_Rook:
                if kingWPos in WL_Rook.defend and WL_Rook.actionsCounter==0:
                    W+=2
            if WR_Rook:
                if kingWPos in WR_Rook.defend and WR_Rook.actionsCounter==0:
                    W+=1
        if B_King.actionsCounter==0:
            B_King.castling=False
            B=0; kingBPos=B_King.getXY()
            if BL_Rook:
                if kingBPos in BL_Rook.defend and BL_Rook.actionsCounter==0:
                    B+=2
            if BR_Rook:
                if kingBPos in BR_Rook.defend and BR_Rook.actionsCounter==0:
                    B+=1
        if W or B:
            castlingSquare = [{(0,4),(0,5),(0,6),(0,7)},{(0,4),(0,3),(0,2),(0,1),(0,0)},
                                {(7,4),(7,5),(7,6),(7,7)},{(7,4),(7,3),(7,2),(7,1),(7,0)}]
            if W==1 or W==3:
                if not (castlingSquare[0] & (set(Chess.AllActions_B['move']) | set(Chess.AllActions_B['attack']) | set(Chess.AllActions_B['take']))):
                    W_King.castling = {W_King.getXY()} if not W_King.castling else W_King.castling
                    W_King.castling.add(WR_Rook.getXY())
            if W==2 or W==3:
                if not (castlingSquare[1] & (set(Chess.AllActions_B['move']) | set(Chess.AllActions_B['attack']) | set(Chess.AllActions_B['take']))):
                    W_King.castling = {W_King.getXY()} if not W_King.castling else W_King.castling
                    W_King.castling.add(WL_Rook.getXY())
            if B==1 or B==3:
                if not (castlingSquare[2] & (set(Chess.AllActions_W['move']) | set(Chess.AllActions_W['attack']) | set(Chess.AllActions_W['take']))):
                    B_King.castling = {B_King.getXY()} if not B_King.castling else B_King.castling
                    B_King.castling.add(BR_Rook.getXY())
            if B==2 or B==3:
                if not (castlingSquare[3] & (set(Chess.AllActions_W['move']) | set(Chess.AllActions_W['attack']) | set(Chess.AllActions_W['take']))):
                    B_King.castling = {B_King.getXY()} if not B_King.castling else B_King.castling
                    B_King.castling.add(BL_Rook.getXY())

    #@countExecutionMethod                      
    def GameOverCheck(Turn):
        Solution: set =  (  set(Chess.AllActions_W['move']) | set(Chess.AllActions_W['take']) | set(Chess.AllActions_W['passive_move'])
                          if Turn==1 else
                            set(Chess.AllActions_B['move']) | set(Chess.AllActions_B['take']) | set(Chess.AllActions_B['passive_move'])  )
        if not Solution:
            if not Chess.Check:
                return 'StaleMate'
            else:
                return 'CheckMate'
        elif len(Chess.pieces)<5:
            whiteTeam = []
            blackTeam = []
            for piece in Chess.pieces:
                if piece.side =='w':
                    if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                        whiteTeam.clear()
                        break
                    whiteTeam.append(piece)
                else:
                    if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                        blackTeam.clear()
                        break
                    blackTeam.append(piece)
            if 3>len(whiteTeam)>=1 and 3>len(blackTeam)>=1:
                return 'StaleMate'
        else:
            return None