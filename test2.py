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
                if not isinstance(p,Rook) and not isinstance(p,King):
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
                elif isinstance(p,Rook) and p.actionsCounter==0:
                    if p.name=='L':
                        WL_Rook=p
                    else:
                        WR_Rook=p
                elif isinstance(p,King):
                    W_King=p
            else:
                Chess.AllActions_B['defend'].update(p.defend)
                if not isinstance(p,Rook) and not isinstance(p,King):
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
                elif isinstance(p,Rook) and p.actionsCounter==0:
                    if p.name=='L':
                        BL_Rook=p
                    else:
                        BR_Rook=p
                elif isinstance(p,King):
                    B_King=p      

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