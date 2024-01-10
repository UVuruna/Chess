from tkinter import *
import copy
from chess import Chess
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from rook import Rook


class AI():

    def countExecutionMethod(method):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1
            print(f"{method}Ponavlja se {wrapper.counter}. put")
            return method(*args, **kwargs)
        wrapper.counter = 0
        return wrapper

    def insideBorder(Self):
        return (Self.x <= 7 and Self.x >= 0) and (Self.y <= 7 and Self.y >= 0)
    def square(Self,tableDict):
        return tableDict[Self.x,Self.y]

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
     
    def possibleMoves(Self,tableDict):
        Self_Copy = copy.deepcopy(Self)
        if Self.type == 'Archer':
            AI.possibleMovesArcher(Self,Self_Copy,tableDict)
        elif isinstance(Self,Pawn):
            AI.possibleMovesPawn(Self,Self_Copy,tableDict)
        else:
            AI.possibleMovesWarrior(Self,Self_Copy,tableDict)
    
    def possibleMovesArcher(Self,Self_Copy,tableDict):
        possibleMoves = set()
        possibleTakes = set()
        possibleDefends = set()
        Defenders = {}
        for dir in Self_Copy.direction:
            DefenderEnemy=None ; extLine = False ; possMove,extendedLine = set(),set()
            Self_Copy.x,Self_Copy.y = Self.getXY()
            while AI.insideBorder(Self_Copy): 
                Self_Copy.incrementation(dir)
                if AI.insideBorder(Self_Copy):
                    if AI.square(Self_Copy,tableDict) == '': # -------------------Prazno polje---------------------------------------------------------------
                        if not extLine:
                            possMove.add(Self_Copy.getXY())
                        else:
                            extendedLine.add(Self_Copy.getXY()) # ----------------------------------------------------------------------------------------
                    elif Self_Copy.side !=AI.square(Self_Copy,tableDict).side: # -------Protivnicka figura ---------------------------------------------------
                        if not extLine:
                            enemy = tableDict[Self_Copy.getXY()]
                            possibleTakes.add(Self_Copy.getXY())                               
                            if isinstance(enemy,King):
                                Chess.Check[Self.side,Self.getXY()]=possMove
                                possibleMoves.update(possMove)
                                break
                            else:
                                extLine=True
                                DefenderEnemy = enemy
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
                            possibleDefends.add(Self_Copy.getXY())
                            possibleMoves.update(possMove)
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

    def possibleMovesWarrior(Self,Self_Copy,tableDict):
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
                            Chess.Check[Self.side,Self.getXY()]=None
                        break # -----------------------------------------------------------------------------------------------------------------------------

                    elif Self_Copy.side ==AI.square(Self_Copy,tableDict).side: # ----------Nasa figura-------------------------------------------------------
                        possibleDefends.add(Self_Copy.getXY())
                        break # -----------------------------------------------------------------------------------------------------------------------------
                else:
                    break
        else:
            del Self_Copy
            AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends)

    def possibleMovesPawn(Self,Self_Copy,tableDict):
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
                                Chess.Check[Self.side,Self.getXY()]=None
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

    def possibleActions():
        W_King=None ; B_King=None
        WL_Rook=None ; WR_Rook=None
        BL_Rook=None ; BR_Rook=None

        if Chess.Check:
            numOfAttackers = len(Chess.Check)
            for k,v in Chess.Check.items():
                attackerSide = k[0]
                enemyAttacker = k[1]
                enemyLine = v
        else:
            numOfAttackers=0
        for p in Chess.pieces:
            if p.side=='w':
                Chess.AllActions_W['defend'].update(p.defend)
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
                        Chess.AllActions_W['move'].update(p.move)
                    else:
                        Chess.AllActions_W['passive_move'].update(p.passiv_move)
                        Chess.AllActions_W['attack'].update(p.attack)
                    Chess.AllActions_W['take'].update(p.take)
            else:
                Chess.AllActions_B['defend'].update(p.defend)
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
                        Chess.AllActions_B['move'].update(p.move)
                    else:
                        Chess.AllActions_B['passive_move'].update(p.passiv_move)
                        Chess.AllActions_B['attack'].update(p.attack)
                    Chess.AllActions_B['take'].update(p.take)       

        W_King.take -= (Chess.AllActions_B['defend'])
        B_King.take -= (Chess.AllActions_W['defend'])

        W = W_King.move.copy()
        B = B_King.move.copy()
        W_King.move -= (Chess.AllActions_B['move']|Chess.AllActions_B['attack']|B)
        B_King.move -= (Chess.AllActions_W['move']|Chess.AllActions_W['attack']|W)
        
        if numOfAttackers >1 and attackerSide=='b':
            Chess.AllActions_W['move'].clear()
            Chess.AllActions_W['take'].clear()
        elif numOfAttackers >1 and attackerSide=='w':
            Chess.AllActions_B['move'].clear()
            Chess.AllActions_B['take'].clear()

        Chess.AllActions_W['move'].update(W_King.move)
        Chess.AllActions_W['take'].update(W_King.take)
        Chess.AllActions_B['move'].update(B_King.move)
        Chess.AllActions_B['take'].update(B_King.take)

        if W_King.actionsCounter==0 and B_King.actionsCounter==0:
            return W_King,WL_Rook,WR_Rook,B_King,BL_Rook,BR_Rook
        elif W_King.actionsCounter==0:
            return W_King,WL_Rook,WR_Rook,None,None,None
        elif B_King.actionsCounter==0:
            return None,None,None,B_King,BL_Rook,BR_Rook
        else:
            return None,None,None,None,None,None

    def castlingCheck(W_King,WL_Rook,WR_Rook,B_King,BL_Rook,BR_Rook):
        W_King.castling=False ; B_King.castling=False
        if W_King:
            W=0; kingWPos=W_King.getXY()
            if WL_Rook:
                WL_Rook.castling=False
                if kingWPos in WL_Rook.defend and WL_Rook.actionsCounter==0:
                    W+=2
            if WR_Rook:
                WR_Rook.castling=False
                if kingWPos in WR_Rook.defend and WR_Rook.actionsCounter==0:
                    W+=1
        if B_King:
            B=0; kingBPos=B_King.getXY()
            if BL_Rook:
                BL_Rook.castling=False
                if kingBPos in BL_Rook.defend and BL_Rook.actionsCounter==0:
                    B+=2
            if BR_Rook:
                BR_Rook.castling=False
                if kingBPos in BR_Rook.defend and BR_Rook.actionsCounter==0:
                    B+=1
        if W or B:
            castlingSquare = [{(0,4),(0,5),(0,6),(0,7)},{(0,4),(0,3),(0,2),(0,1),(0,0)},
                                {(7,4),(7,5),(7,6),(7,7)},{(7,4),(7,3),(7,2),(7,1),(7,0)}]
            if W==1 or W==3:
                if not (castlingSquare[0] & (Chess.AllActions_B['move'] | Chess.AllActions_B['attack'] | Chess.AllActions_B['take'])):
                    W_King.castling=True ; WR_Rook.castling=True
            if W==2 or W==3:
                if not (castlingSquare[1] & (Chess.AllActions_B['move'] | Chess.AllActions_B['attack'] | Chess.AllActions_B['take'])):
                    W_King.castling=True ; WL_Rook.castling=True
            if B==1 or B==3:
                if not (castlingSquare[2] & (Chess.AllActions_W['move'] | Chess.AllActions_W['attack'] | Chess.AllActions_W['take'])):
                    B_King.castling=True ; BR_Rook.castling=True
            if B==2 or B==3:
                if not (castlingSquare[3] & (Chess.AllActions_W['move'] | Chess.AllActions_W['attack'] | Chess.AllActions_W['take'])):
                    B_King.castling=True ; BL_Rook.castling=True
                          
    def GameOverCheck(Turn):
        Solution: set =  (Chess.AllActions_W['move']|Chess.AllActions_W['take']|Chess.AllActions_W['passive_move']
                          if Turn==1 else
                          Chess.AllActions_B['move']|Chess.AllActions_B['take']|Chess.AllActions_B['passive_move'])
        
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
                elif piece.side =='':
                    if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                        blackTeam.clear()
                        break
                    blackTeam.append(piece)
            if 3>len(whiteTeam)>=1 and 3>len(blackTeam)>=1:
                return 'StaleMate'
        else:
            return None


    #@AI.countExecutionMethod
    def selfKingActionsCalc(Turn,CurrentTableDict):
        global realKing
        selfKingActions = []
        for piece in Chess.pieces:
            if (Turn == 1 and isinstance(piece,King) and piece.side == 'w') or \
                (Turn == -1 and isinstance(piece,King) and piece.side == 'b'):
                move,take = piece.possibleMoves(CurrentTableDict)[:2]
                selfKingActions += move
                selfKingActions += take
                selfKing = copy.deepcopy(piece)
                realKing = piece
        return selfKing, set(selfKingActions)

    #@AI.countExecutionMethod
    def enemyArcherDanger(CurrentTableDict,selfKing):
        Defenders = {}
        BlockableLine = []
        #@AI.countExecutionMethod
        def iteratingLine(possMove,direction):
            Line = []
            BlockableLine = []
            Defenders = {}
            defenderCount = 0
            while AI.insideBorder(possMove):
                possMove.incrementation(direction)
                if AI.insideBorder(possMove) and defenderCount <2:
                    Line.append(possMove.getXY())
                    if CurrentTableDict[possMove.getXY()] != '' and CurrentTableDict[possMove.getXY()].side != possMove.side:
                        if CurrentTableDict[possMove.getXY()].type =="Archer" and direction in CurrentTableDict[possMove.getXY()].direction:
                            if defenderCount ==0:
                                BlockableLine += Line
                            else:
                                Defenders[defender] = Line
                            return Defenders,BlockableLine
                        else:
                            return
                    elif CurrentTableDict[possMove.getXY()] !='' and CurrentTableDict[possMove.getXY()].side == possMove.side:
                        defenderCount +=1
                        defender = CurrentTableDict[possMove.getXY()]
                else:
                    return
        for dir in Chess.direction:
            possMove = copy.deepcopy(selfKing)
            try:
                d,bl = iteratingLine(possMove,dir)
                Defenders.update(d)
                BlockableLine.extend(bl)
            except TypeError: # za None situacije, koje su ceste.
                continue
        return dict(Defenders),set(BlockableLine)

    #@countExecutionMethod   
    def AnalyzingMovements(Turn,tableDict,ourTeam,king,defenders,ActDict):
        def team(Turn,ourTeam):
            if (ourTeam is False and Turn==1) or (ourTeam is True and Turn==-1):
                return piece.side == 'b'
            elif (ourTeam is True and Turn==1) or (ourTeam is False and Turn==-1):
                return piece.side == 'w'
        def noKing(king):
            if king is False:
                return not isinstance(piece,King)
            else:
                return True     
        def noDefender(defenders):
            if defenders:
                return piece not in list(defenders.keys())
            else:
                return True

        PossibleTakes = set()
        PossibleMoves = set()
        possibleActionsDefenders = set()
        possibleActionsDict = {}
        for piece in Chess.pieces:
            take = set() ; move = set()
            if team(Turn,ourTeam) and noKing(king):
                possMove,possTake = piece.possibleMoves(tableDict)[:2]
                if noDefender(defenders):  
                    PossibleMoves.update(possMove)
                    PossibleTakes.update(possTake)   
                    if ActDict:
                        possibleActionsDict[piece]=set(set(possTake)|set(possMove))
                else:
                    take.update(possTake)
                    move.update(possMove)
                    actionsAll = take|move
                    possibleActionsDefenders.update(actionsAll&set(defenders[piece]))
                    if ActDict:
                        possibleActionsDict[piece]=set(actionsAll&set(defenders[piece]))
        return PossibleTakes, PossibleMoves, possibleActionsDefenders, possibleActionsDict

    #@AI.countExecutionMethod
    def whoAttack_Position(Turn,CurrentTableDict,selfKing,position,noKing):
        king = copy.deepcopy(selfKing)
        TableDict = CurrentTableDict.copy()
        if noKing == True:
            TableDict[king.getXY()] = ''

        enemyAttack = []
        positionsAttacked = []
        for piece in Chess.pieces:
            T,D,A = piece.possibleMoves(TableDict)[1:]
            if Turn == 1 and  piece.side == 'b':
                if any(position in lists for lists in [T,D,A]):
                    enemyAttack.append(piece.getXY())
                    positionsAttacked.append(position)
            elif Turn == -1 and  piece.side == 'w':
                if any(position in lists for lists in [T,D,A]):
                    enemyAttack.append(piece.getXY())
                    positionsAttacked.append(position)
        return enemyAttack,positionsAttacked

    #@AI.countExecutionMethod
    def whoAttack_PositionsList(Turn,CurrentTableDict,selfKing,positionList,noKing):
        enemyAttack = []
        for pos in positionList:
            a = AI.whoAttack_Position(Turn,CurrentTableDict,selfKing,pos,noKing)[1]
            if a:
                enemyAttack +=a
        return set(enemyAttack)

    #@countExecutionMethod    
    def dangerZone(turn,tableDict,enPassant):
        selfKing,selfKingActions = AI.selfKingActionsCalc(turn,tableDict)
        Defenders,BlockableLine = AI.enemyArcherDanger(tableDict,selfKing)
        directAttackers: set = set(AI.whoAttack_Position(turn,tableDict,selfKing,selfKing.getXY(),noKing=False)[0]) 
        defendedEnemies: set = AI.whoAttack_PositionsList(turn,tableDict,selfKing,selfKingActions,noKing=True) 
        teamPossTake,teamPossMove,possibleActionsDefenders,possibleActionsDict  = AI.AnalyzingMovements(turn,tableDict,ourTeam=True,king=False,defenders=Defenders,ActDict=True) 
        directAttackerSolution = directAttackers&teamPossTake
        blockableLineSolution = BlockableLine&teamPossMove
        

        DangerKingSolve: set = selfKingActions - defendedEnemies
        DangerTeamSolve: set = directAttackerSolution|blockableLineSolution if len(directAttackers)==1 else set()
        TeamOptions: set = teamPossMove|teamPossTake|possibleActionsDefenders
        possibleActionsDict[realKing]=DangerKingSolve
        if enPassant:
            for pie in Chess.pieces:
                if isinstance(pie,Pawn) and pie.side==selfKing.side and enPassant in pie.possibleMoves(tableDict)[3]:
                    possibleActionsDict[pie].add(enPassant)


        return realKing,TeamOptions,DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,possibleActionsDict

    #@countExecutionMethod
    def GameOverCheck(selfKing,TeamOptions,directAttackers,DangerKingSolve,DangerTeamSolve):
        Solution: set =  DangerKingSolve|DangerTeamSolve
        StaleMate: set = Solution|directAttackers|TeamOptions

        GameOver = None
        selfTeam = []
        enemyTeam = []
        for piece in Chess.pieces:
            if piece.side == selfKing.side:
                if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                    selfTeam.clear()
                    break
                selfTeam.append(piece)
            else:
                if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                    enemyTeam.clear()
                    break
                enemyTeam.append(piece)

        if 3>len(selfTeam)>=1 and 3>len(enemyTeam)>=1:
            GameOver = 'StaleMate'
        if not StaleMate:
            GameOver = 'StaleMate'
        if directAttackers and not Solution:
            GameOver = 'CheckMate'

        return GameOver
    
    #@countExecutionMethod
    def CastlingCheck(turn,tableDict,king):
        castling = [{(0,4),(0,5),(0,6),(0,7)},{(0,4),(0,3),(0,2),(0,1),(0,0)},
                    {(7,4),(7,5),(7,6),(7,7)},{(7,4),(7,3),(7,2),(7,1),(7,0)}]
        CastlingList = [[(0,7),(0,4)],[(0,0),(0,4)],[(7,7),(7,4)],[(7,0),(7,4)]]
        attackPos,attackPie = AI.AnalyzingMovements(turn,tableDict,ourTeam=False,king=True,defenders=None,ActDict=False)[:2]
        attack = attackPos | attackPie
        kW,qW,kB,qB = 0,0,0,0 ; castlingOptions = [kW,qW,kB,qB]
        castlingOptions[0],castlingOptions[1],castlingOptions[2],castlingOptions[3] = king.castlingCheck(tableDict)

        if castling[0] & attack:
            castlingOptions[0] *=0
        if castling[1] & attack:
            castlingOptions[1] *=0
        if castling[2] & attack:
            castlingOptions[2] *=0
        if castling[3] & attack:
            castlingOptions[3] *=0

        squares = []
        for i in range(4):
            if castlingOptions[i] !=0:
                squares += CastlingList[i]

        return squares,castlingOptions[0],castlingOptions[1],castlingOptions[2],castlingOptions[3]