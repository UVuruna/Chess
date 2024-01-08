from chess import Chess
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from rook import Rook
from AI import AI
import time

class ComputerAI():

    def PositionAnalyze(Turn,tableDict,enPassant,ourTeam):
        def turnSwap(Turn):
            return Turn if ourTeam is True else Turn*-1

        def team(Turn,ourTeam):
            if (ourTeam is False and Turn==1) or (ourTeam is True and Turn==-1):
                return piece.side == 'b'
            else:
                return piece.side == 'w'
               
        def position_toObject(possActions,tableDict,noKing):
            
            def withoutKing(piece):
                if noKing is True:
                    return not isinstance(piece,King)
                else:
                    return True
            piecesSet = set()
            points=0
            for i in possActions:
                obj = tableDict[i]
                if withoutKing(obj):
                    points +=(ComputerAI.PointsCoefficient(obj,action=False))
                    piecesSet.add(obj)
            return piecesSet,points

        directAttackers,DangerTeamSolve,Defenders,possibleActionsDict=AI.dangerZone(turnSwap(Turn),tableDict,enPassant)[-4:]
        if directAttackers:
            for k,v in possibleActionsDict.items():
                if not isinstance(k,King):
                    possibleActionsDict[k]=set(v)&DangerTeamSolve
  
        ActionDict = {}
        ActionNumDict = {}
        for piece in Chess.pieces:
            if team(Turn,ourTeam):
                move,take,defend,attack = piece.possibleMoves(tableDict)
                allowedActions = set(possibleActionsDict[piece])
                possMove:set = set(move)&allowedActions
                numPossMove = len(possMove)

                possTake:set = set(take)&allowedActions
                possTakeObj,possTakeObjPoints = position_toObject(possTake,tableDict,False)
                numPossTake = len(possTakeObj)*possTakeObjPoints/4

                possDefendObj,possDefendObjPoints = position_toObject(defend,tableDict,True)
                numPossDefend = len(possDefendObj)*possDefendObjPoints/4

                if isinstance(piece,Pawn):
                    try:
                        possAttack:set = set(attack)&set(Defenders[piece])
                    except KeyError:
                        possAttack=set(attack)
                    numPossOther = len(possAttack)
                    piece_actions = { 'move': possMove,
                                    'take': possTakeObj,
                                    'defend': possDefendObj,
                                    'attack': possAttack}
                elif isinstance(piece,King):
                    possCastlingObj=set()
                    numPossOther =0
                    kW,qW,kB,qB = AI.CastlingCheck(turnSwap(Turn),tableDict,piece)[1:]
                    if (kW or kB)!=0:
                        for rook in Chess.pieces:
                            if isinstance(rook,Rook) and rook.side==piece.side and rook.name=='R':
                                possCastlingObj.add(rook)
                                numPossOther +=1
                    if (qW or qB)!=0:
                        for rook in Chess.pieces:
                            if isinstance(rook,Rook) and rook.side==piece.side and rook.name=='L':
                                possCastlingObj.add(rook)
                                numPossOther +=1
                    piece_actions = { 'move': possMove,
                                    'take': possTakeObj,
                                    'defend': possDefendObj,
                                    'castling': possCastlingObj}
                else:
                    piece_actions = { 'move': possMove,
                                    'take': possTakeObj,
                                    'defend': possDefendObj}
                    numPossOther=0
                ActionDict[piece] = piece_actions
                ActionNumDict[piece] = [numPossMove,numPossTake,numPossDefend,numPossOther]
          
        return ActionDict,ActionNumDict
    

    def PointsCoefficient(Piece,action):
        if isinstance(Piece,Pawn):
            coef = 2
        elif isinstance(Piece,Knight):
            coef = 4
        elif isinstance(Piece,Bishop):
            coef = 4
        elif isinstance(Piece,Rook):
            coef = 5
        elif isinstance(Piece,Queen):
            coef = 7
        elif isinstance(Piece,King):
            coef = 1

        if action is True:
            move=1 if not isinstance(Piece,Pawn) else 0.5
            take=2.5
            defend=1.5
            other=1 if isinstance(Piece,Pawn) else 1.5
            return coef,[move,take,defend,other]
        else:
            return coef
    
    def PointCalulator(actionDictionary):
        points=0
        for k,v in actionDictionary.items():
            lifeCoeff,actionCoeff = ComputerAI.PointsCoefficient(k,action=True)
            points+=2*lifeCoeff
            for i in range(4):
                points+=(v[i]*actionCoeff[i]) if not isinstance(k,King) else (v[i]*actionCoeff[i])/3
        return points





