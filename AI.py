from tkinter import *
from ChessParent import Chess
from Pieces import *
from ImagesDecorators import Decorator


class AI:

    def ClearPossibleActions():
        for k in Chess.AllActions_W.keys():
            Chess.AllActions_W[k].clear()
        for k in Chess.AllActions_B.keys():
            Chess.AllActions_B[k].clear()
        Chess.Check=False

        pieces = Chess.piecesB+Chess.piecesW
        for p in pieces:
            if isinstance(p,King):
                p.check.clear() ; p.checkLine.clear()
            if not isinstance(p,Pawn):
                p.move.clear()
                if isinstance(p,Archer):
                    p.attack.clear()
            else:
                p.attack.clear() ; p.passive_move.clear() ; p.enpassant = None
            p.take.clear() ; p.defend.clear() ; p.pinned.clear()

    #@Decorator.countExecutionMethod
    def PossibleActions():
        W_King=None ; B_King=None
        WL_Rook=None ; WR_Rook=None
        BL_Rook=None ; BR_Rook=None

        def updateActionsDict(p,ActionsDict):
            ActionsDict['defend'].extend(p.defend)
            if p.pinned:
                pin = p.pinned
                p.move &= pin[0]
                p.take &= pin[1]
            if Chess.enPassant and isinstance(p,Pawn) and Chess.enPassant[2]!=p.side and Chess.enPassant[0] in p.attack:
                    p.take.add(Chess.enPassant[0])
                    p.enpassant = Chess.enPassant[1]

            if len(check)==1:
                try:
                    p.move &= checkLine
                except AttributeError:
                    p.passive_move &= checkLine
                    p.attack &= checkLine
                p.take &= check
            elif len(check)>1:
                try:
                    p.move.clear()
                except AttributeError:
                    p.passive_move.clear()
                    p.attack.clear()
                p.take.clear()
                return
            
            try:
                ActionsDict['move'].extend(p.move)
                if isinstance(p,Archer):
                    ActionsDict['attack'].extend(p.attack)
            except AttributeError:
                ActionsDict['passive_move'].extend(p.passive_move)
                ActionsDict['attack'].extend(p.attack)
            ActionsDict['take'].extend(p.take)

        for p in Chess.piecesW:
            if isinstance(p,King):
                check = set()
                checkLine = set()
                W_King=p
                check.update(p.check)
                checkLine.update(p.checkLine)
            elif isinstance(p,Rook) and p.actionsCounter==0:
                if p.name=='L':
                    WL_Rook=p
                else:
                    WR_Rook=p
                updateActionsDict(p,Chess.AllActions_W)
            else:
                updateActionsDict(p,Chess.AllActions_W)

        for p in Chess.piecesB:
            if isinstance(p,King):
                check = set()
                checkLine = set()
                B_King=p
                check.update(p.check)
                checkLine.update(p.checkLine)
            elif isinstance(p,Rook) and p.actionsCounter==0:
                if p.name=='L':
                    BL_Rook=p
                else:
                    BR_Rook=p
                updateActionsDict(p,Chess.AllActions_B)
            else:
                updateActionsDict(p,Chess.AllActions_B)

        W_King.take -= set(Chess.AllActions_B['defend'])
        B_King.take -= set(Chess.AllActions_W['defend'])

        W = W_King.move.copy()
        B = B_King.move.copy()

        W_King.move -= (set(Chess.AllActions_B['attack']) | set(Chess.AllActions_B['move']) | B )
        B_King.move -= (set(Chess.AllActions_W['attack']) | set(Chess.AllActions_W['move']) | W )
        

        Chess.AllActions_W['move'].extend(W_King.move)
        Chess.AllActions_W['take'].extend(W_King.take)
        Chess.AllActions_B['move'].extend(B_King.move)
        Chess.AllActions_B['take'].extend(B_King.take)
        Chess.enPassant.clear()

        return W_King,WL_Rook,WR_Rook,B_King,BL_Rook,BR_Rook


    #@Decorator.countExecutionMethod
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
            castlingSquare = [{(1,5),(1,6),(1,7)},{(1,5),(1,4),(1,3)},
                                {(8,5),(8,6),(8,7)},{(8,5),(8,4),(8,3)}]
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

    #@Decorator.countExecutionMethod                      
    def GameOverCheck(Turn):
        Solution: set =  (  set(Chess.AllActions_W['move']) | set(Chess.AllActions_W['take']) | set(Chess.AllActions_W['passive_move'])
                          if Turn==1 else
                            set(Chess.AllActions_B['move']) | set(Chess.AllActions_B['take']) | set(Chess.AllActions_B['passive_move'])  )
        if not Solution:
            if Chess.Check is False:
                return 'StaleMate'
            else:
                return 'CheckMate'
        elif len(Chess.piecesW)<3 and len(Chess.piecesB)<3:
            whiteTeam = []
            blackTeam = []
            for piece in Chess.piecesW:
                    if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                        whiteTeam.clear()
                        break
                    whiteTeam.append(piece)

            for piece in Chess.piecesB:
                    if isinstance(piece,Queen) or isinstance(piece,Rook) or isinstance(piece,Pawn):
                        blackTeam.clear()
                        break
                    blackTeam.append(piece)
            if 3>len(whiteTeam)>=1 and 3>len(blackTeam)>=1:
                return 'StaleMate'
        else:
            return None