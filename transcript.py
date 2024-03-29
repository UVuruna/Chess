from chess import Chess

class Rewind():
    PosInTransc = -1
    
    def EnPassant(TranscriptName): # zove je verifikacija # Pravi novi possible Take i novi Take move
        with open(f'{TranscriptName}.txt','r') as f:
            text = f.readlines()
        try:
            lastPlay = text[Rewind.PosInTransc].split()
            if lastPlay[3]=='move' and lastPlay[1]=='Pawn' and abs(int(lastPlay[2][1])-int(lastPlay[4][1])) == 2:
                xy: tuple = ((int(lastPlay[2][1])+int(lastPlay[4][1]))//2-1),(Rewind.letterToNum(lastPlay[2][0]))
                enemyXY: tuple = ((int(lastPlay[4][1])-1),(Rewind.letterToNum(lastPlay[2][0])))
                return xy,enemyXY
        except IndexError:
            return

    def ResetPosition():
        Rewind.PosInTransc = -1
        return Rewind.PosInTransc

    def Get_Transcript_and_Position(TranscriptName=None):
        global actions
        if TranscriptName:
            with open(f'{TranscriptName}.txt','r') as f:
                actions = f.readlines()
        if Rewind.PosInTransc == -1:
            return 'noNext',Rewind.PosInTransc
        elif (len(actions)+Rewind.PosInTransc) < 0:
            return 'noBack',Rewind.PosInTransc
        else:
            return None,Rewind.PosInTransc

    def letterToNum(sign):
        return ord(sign) - ord('A')

    def castlingConverter(play):
        if play[1][0] == 'K' and play[2][0] == 'b':
            kingStartPos: tuple = (7,4)
            rookStartPos: tuple = (7,7)
            kingEndPos: tuple = (7,6)
            rookEndPos: tuple = (7,5)
        elif play[1][0] == 'K' and play[2][0] == 'w':
            kingStartPos: tuple = (0,4)
            rookStartPos: tuple = (0,7)
            kingEndPos: tuple = (0,6)
            rookEndPos: tuple = (0,5)
        elif play[1][0] == 'Q' and play[2][0] == 'b':
            kingStartPos: tuple = (7,4)
            rookStartPos: tuple = (7,0)
            kingEndPos: tuple = (7,2)
            rookEndPos: tuple = (7,3)
        else:
            kingStartPos: tuple = (0,4)
            rookStartPos: tuple = (0,0)
            kingEndPos: tuple = (0,2)
            rookEndPos: tuple = (0,3)
        return kingStartPos,kingEndPos,rookStartPos,rookEndPos

    def positionConverter(play,num):
        EndingPos = None
        objPos = None
        xS: int = int(play[num][1])-1
        yS: int = Rewind.letterToNum(play[num][0])
        StartingPos: tuple = (xS,yS)
        try:
            xE: int = int(play[num+2][1])-1
            yE: int = Rewind.letterToNum(play[num+2][0])
            EndingPos: tuple = (xE,yE)

            xO: int = int(play[num+4][1])-1
            yO: int = Rewind.letterToNum(play[num+4][0])
            objPos: tuple = (xO,yO)
        except IndexError:
            None
        return StartingPos,EndingPos,objPos

    def AnalyzeTranscript(direction,moveCounter):
        Table = Chess.currentTableDict()
        try:
            lastPlay = actions[Rewind.PosInTransc].split()
            nextPlayCheck = actions[Rewind.PosInTransc+1].split()
        except IndexError:
            return
        if len(lastPlay)==5: # Move
            startXY,endXY = Rewind.positionConverter(lastPlay,2)[:2]
            if direction == 'b':
                Chess.MovesDict[Table[endXY]]-=1
                Table[endXY].x,Table[endXY].y = startXY
            elif direction == 'n':
                Chess.MovesDict[Table[startXY]]+=1
                Table[startXY].x,Table[startXY].y = endXY
                if nextPlayCheck[1] == 'promote':
                    Rewind.PosInTransc += 1
                    Rewind.AnalyzeTranscript('n',moveCounter)
        elif len(lastPlay)==6: # Take
            startXY,endXY = Rewind.positionConverter(lastPlay,2)[:2]
            if direction == 'b':
                Chess.MovesDict[Table[endXY]]-=1
                a = Chess.TakenDict[Table[endXY]][moveCounter]
                Chess.pieces.append(a)
                Table[endXY].x,Table[endXY].y = startXY
                a.x,a.y = endXY 
            elif direction == 'n':
                Chess.pieces.remove(Table[endXY])
                Chess.MovesDict[Table[startXY]]+=1
                Table[startXY].x,Table[startXY].y = endXY
                if nextPlayCheck[1] == 'promote':
                    Rewind.PosInTransc += 1
                    Rewind.AnalyzeTranscript('n',moveCounter)
        elif len(lastPlay)==3: # Castling
            kS,kE,rS,rE = Rewind.castlingConverter(lastPlay)
            if direction == 'b':
                king = Table[kE] ; Chess.MovesDict[king]-=1 ; king.x,king.y = kS
                rook = Table[rE] ; Chess.MovesDict[rook]-=1 ; rook.x,rook.y = rS
            elif direction == 'n':
                king = Table[kS] ; Chess.MovesDict[king]+=1 ; king.x,king.y = kE
                rook = Table[rS] ; Chess.MovesDict[rook]+=1 ; rook.x,rook.y = rE
        elif len(lastPlay)==4: # Promote
            xy = Rewind.positionConverter(lastPlay,3)[0]
            if direction == 'b':
                a = Chess.PromoteDict[Table[xy]]
                Chess.pieces.append(a)
                a.x,a.y = xy
                Chess.pieces.remove(Table[xy])
                Rewind.PosInTransc -= 1
                Rewind.AnalyzeTranscript('b',moveCounter)
            elif direction == 'n':
                a = next((k for k,v in Chess.PromoteDict.items() if v==Table[xy]),None)
                Chess.pieces.append(a)
                a.x,a.y = xy
                Chess.pieces.remove(Table[xy])
        elif len(lastPlay)==7: # EnPassant
            startXY,endXY,objXY = Rewind.positionConverter(lastPlay,2)
            if direction == 'b':
                Chess.MovesDict[Table[endXY]]-=1
                a = Chess.TakenDict[Table[endXY]][moveCounter]
                Chess.pieces.append(a)
                Table[endXY].x,Table[endXY].y = startXY
                a.x,a.y = objXY 
            elif direction == 'n':
                Chess.pieces.remove(Table[objXY])
                Chess.MovesDict[Table[startXY]]+=1
                Table[startXY].x,Table[startXY].y = endXY
        return Table
        
            

    def Previous(moveCounter):
        Table = Rewind.AnalyzeTranscript('b',moveCounter)
        Rewind.PosInTransc -= 1
        return Table

    def Next(moveCounter):
        Rewind.PosInTransc += 1
        Table = Rewind.AnalyzeTranscript('n',moveCounter)
        return Table