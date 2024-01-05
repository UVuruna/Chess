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

    def getTable():
        return Chess.currentTableDict()

    def StartingPosition():
            # Senatus
        king_W=King('w'); king_B=King('b') ; queen_W=Queen('w'); queen_B=Queen('b')
            # Hiereus
        bishop_wL=Bishop('w','L'); bishop_wR=Bishop('w','R'); bishop_bL=Bishop('b','L'); bishop_bR=Bishop('b','R')
            # Medjay
        knight_wL=Knight('w','L'); knight_wR=Knight('w','R'); knight_bL=Knight('b','L'); knight_bR=Knight('b','R')
            # Legiones
        rook_wL=Rook('w','L'); rook_wR=Rook('w','R'); rook_bL=Rook('b','L'); rook_bR=Rook('b','R')
            # Plebs
        pawn_bL1=Pawn('b', 'L1'); pawn_bL2=Pawn('b', 'L2'); pawn_bL3=Pawn('b', 'L3'); pawn_bCL=Pawn('b', 'CL')
        pawn_bCR=Pawn('b', 'CR'); pawn_bR3=Pawn('b', 'R3'); pawn_bR2=Pawn('b', 'R2'); pawn_bR1=Pawn('b', 'R1')
        pawn_wL1=Pawn('w', 'L1'); pawn_wL2=Pawn('w', 'L2'); pawn_wL3=Pawn('w', 'L3'); pawn_wCL=Pawn('w', 'CL')
        pawn_wCR=Pawn('w', 'CR'); pawn_wR3=Pawn('w', 'R3'); pawn_wR2=Pawn('w', 'R2'); pawn_wR1=Pawn('w', 'R1')

    def AllActions():
        pass


    def PositionAnalyze(Turn,tableDict,ourTeam):
        def team(Turn,ourTeam):
            if ourTeam is False:
                if Turn==1:
                    return piece.side == 'b'
                else:
                    return piece.side == 'w'
            else:
                if Turn==1:
                    return piece.side == 'w'
                else:
                    return piece.side == 'b'   

        ActionDict = {}
        for piece in Chess.pieces:
            if team(Turn,ourTeam):
                move,take,defend,attack = piece.possibleMoves(tableDict)
                piece_actions = { 'position': piece.position(),
                                  'move': move,
                                  'take': take,
                                  'defend': defend,
                                  'attack': attack if isinstance(piece,Pawn) else None}
                ActionDict[piece] = piece_actions
        if ourTeam==True:
            possibleActionsDict=AI.GameOverCheck(Turn)[-1]
        else:
            possibleActionsDict=AI.GameOverCheck(Turn*-1)[-1]    
        return ActionDict,possibleActionsDict


if __name__ == '__main__':
    ComputerAI.StartingPosition()

    start = time.time()
    for _ in range(1000):
        PossibleCheck,DangerKingSolve,directAttacker,DangerTeamSolve,Defenders,GameOver,CurrentTableDict,possibleActionsDict=AI.GameOverCheck(1)
        
        
    currentTable = ComputerAI.getTable()

    ActionDictOUR = ComputerAI.PositionAnalyze(1,currentTable,ourTeam=True)
    ActionDictENEMY = ComputerAI.PositionAnalyze(-1,currentTable,ourTeam=True)



    end = time.time()


    print(f'{(end-start)* 1000:,.2f} ms')

    print(Defenders)
    print(possibleActionsDict)

    print("OUR TEAM")
    for k,v in ActionDictOUR.items():
        print(str(type(k)).ljust(24),v)

    print("ENEMY TEAM")
    for k,v in ActionDictENEMY.items():
        print(str(type(k)).ljust(24),v)


    