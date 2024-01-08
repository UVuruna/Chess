from tkinter import *
import copy
from chess import Chess
from king import King
from queen import Queen
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

    def updatingAttributes(Self,m,t,d,De,extL,a=None):
        if Self.move is None:
            Self.move = m
        else:
            Self.move.update(m)

        if Self.take is None:
            Self.take = t
        else:
            Self.take.update(t)

        if Self.defend is None:
            Self.defend = d
        else:
            Self.defend.update(d)

        if a is not None:
            if Self.attack is None:
                Self.attack = a
            else:
                Self.attack.update(a)

        if De is not None:
            De.Defender = extL

    def possibleMoves(Self,tableDict):
        possibleMoves = set()
        possibleTakes = set()
        possibleDefends = set()
        if isinstance(Self,Pawn):
            AI.possibleMovesPawn(Self,tableDict,possibleMoves,possibleTakes,possibleDefends)
        else:
            for dir in Self.direction:
                extLine = False
                DefenderEnemy=None
                possibleMoves,possibleTakes,possibleDefends,extendedLine = set(),set(),set(),set()
                possMove = copy.deepcopy(Self)
                while AI.insideBorder(possMove): 
                    possMove.incrementation(dir)
                    if AI.insideBorder(possMove):
                        if AI.square(possMove,tableDict) == '': # -------------------Prazno polje------------------------------------
                            if not extLine:
                                possibleMoves.add(possMove.position())
                                if possMove.type == 'Archer':
                                    None
                                else:
                                    AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,DefenderEnemy,extendedLine)
                                    break
                            else:
                                extendedLine.add(possMove.position()) # -------------------------------------------------------------

                        elif possMove.side !=AI.square(possMove,tableDict).side: # -------Protivnicka figura ------------------------
                            if not extLine:
                                possibleTakes.add(tableDict[possMove.position()])
                                if possMove.type == 'Archer':
                                    extLine=True
                                    extendedLine.update(possibleMoves)
                                    extendedLine.add(possMove)
                                    DefenderEnemy = tableDict[possMove.position()]
                                else:
                                    AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,DefenderEnemy,extendedLine)
                                    break
                            else:
                                if isinstance(tableDict[possMove.position()],King):
                                    AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,DefenderEnemy,extendedLine)
                                else:
                                    DefenderEnemy=None
                                    AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,DefenderEnemy,extendedLine)
                                    break # ----------------------------------------------------------------------------------------

                        elif possMove.side ==AI.square(possMove,tableDict).side: # ----------Nasa figura----------------------------
                            if not extLine:
                                possibleDefends.add(tableDict[possMove.position()])
                                AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,DefenderEnemy,extendedLine)
                                break
                            else:
                                DefenderEnemy=None
                                AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,DefenderEnemy,extendedLine)
                                break # --------------------------------------------------------------------------------------------
                    else:
                        DefenderEnemy=None
                        AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,DefenderEnemy,extendedLine)
                        break
    
    def possibleMovesPawn(Self,tableDict,possibleMoves,possibleTakes,possibleDefends):
        possibleAttacks = set()

        if Self.side == 'w':
            Self.directionMove = Chess.direction[0]
            Self.directionAttack = Chess.direction[4:6]
        else:
            Self.directionMove = Chess.direction[1]
            Self.directionAttack = Chess.direction[6:]

        tries = 2 if (Self.side == 'w' and Self.x == 1) or (Self.side == 'b' and Self.x == 6) else 1

        for dir in Self.directionMove:
            possMove = copy.deepcopy(Self)
            while AI.insideBorder(possMove): 
                possMove.incrementation(dir)
                if tries == 0:
                    AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,None,None,possibleAttacks)
                    break
                elif AI.insideBorder(possMove) and AI.square(possMove,tableDict) =='':
                    possibleMoves.add(possMove.position())
                    tries -= 1
                else:
                    AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,None,None,possibleAttacks)
                    break 

        for dir in Self.directionAttack:
            possMove = copy.deepcopy(Self)
            while AI.insideBorder(possMove):
                possMove.incrementation(dir)
                if AI.insideBorder(possMove):
                    if AI.square(possMove,tableDict) !='':
                        if possMove.side !=AI.square(possMove,tableDict).side:
                            possibleTakes.add(tableDict[possMove.position()])
                            AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,None,None,possibleAttacks)
                            break
                        elif possMove.side ==AI.square(possMove,tableDict).side:
                            possibleDefends.add(possMove.position())
                            AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,None,None,possibleAttacks)
                            break
                    else:
                        possibleAttacks.add(possMove.position())
                        AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,None,None,possibleAttacks)
                        break
                else:
                    AI.updatingAttributes(Self,possibleMoves,possibleTakes,possibleDefends,None,None,possibleAttacks)
                    break                    




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
                    Line.append(possMove.position())
                    if CurrentTableDict[possMove.position()] != '' and CurrentTableDict[possMove.position()].side != possMove.side:
                        if CurrentTableDict[possMove.position()].type =="Archer" and direction in CurrentTableDict[possMove.position()].direction:
                            if defenderCount ==0:
                                BlockableLine += Line
                            else:
                                Defenders[defender] = Line
                            return Defenders,BlockableLine
                        else:
                            return
                    elif CurrentTableDict[possMove.position()] !='' and CurrentTableDict[possMove.position()].side == possMove.side:
                        defenderCount +=1
                        defender = CurrentTableDict[possMove.position()]
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
            TableDict[king.position()] = ''

        enemyAttack = []
        positionsAttacked = []
        for piece in Chess.pieces:
            T,D,A = piece.possibleMoves(TableDict)[1:]
            if Turn == 1 and  piece.side == 'b':
                if any(position in lists for lists in [T,D,A]):
                    enemyAttack.append(piece.position())
                    positionsAttacked.append(position)
            elif Turn == -1 and  piece.side == 'w':
                if any(position in lists for lists in [T,D,A]):
                    enemyAttack.append(piece.position())
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
        directAttackers: set = set(AI.whoAttack_Position(turn,tableDict,selfKing,selfKing.position(),noKing=False)[0]) 
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