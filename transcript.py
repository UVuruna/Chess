from chess import Chess

class Rewind():
    PosInTransc = -1
    
    def EnPassant(TranscriptName): # zove je verifikacija # Pravi novi possible Take i novi Take move
        with open(f'{TranscriptName}.txt','r') as f:
            text = f.readlines()
        try:
            lastPlay = text[Rewind.PosInTransc].split()
            xS =int(lastPlay[2][1])
            xE =int(lastPlay[4][1])
            if lastPlay[3]=='move' and lastPlay[1]=='Pawn' and abs(xS-xE) ==2:
                Y =Rewind.letterToNum(lastPlay[2][0])
                return ((xS+xE)//2-1,Y),(xE-1,Y)
        except (IndexError,ValueError):
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
        elif (len(actions)+Rewind.PosInTransc) == -1:
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
                self = Table[endXY]
                self.actionsCounter -=1
                self.setXY(startXY)
            elif direction == 'n':
                self = Table[startXY]
                self.actionsCounter +=1
                self.setXY(endXY)
                if nextPlayCheck[1] == 'promote':
                    Rewind.PosInTransc += 1
                    Rewind.AnalyzeTranscript('n',moveCounter)
        elif len(lastPlay)==6: # Take
            startXY,endXY = Rewind.positionConverter(lastPlay,2)[:2]
            if direction == 'b':
                self = Table[endXY]
                self.actionsCounter -=1
                enemy = Chess.TakenDict[Table[endXY]][moveCounter]
                Chess.pieces.append(enemy)
                self.setXY(startXY)
                enemy.setXY(endXY)
            elif direction == 'n':
                Chess.pieces.remove(Table[endXY])
                self = Table[startXY]
                self.actionsCounter +=1
                self.setXY(endXY)
                if nextPlayCheck[1] == 'promote':
                    Rewind.PosInTransc += 1
                    Rewind.AnalyzeTranscript('n',moveCounter)
        elif len(lastPlay)==3: # Castling
            kS,kE,rS,rE = Rewind.castlingConverter(lastPlay)
            if direction == 'b':
                king = Table[kE] ; king.actionsCounter -=1 ; king.setXY(kS)
                rook = Table[rE] ; rook.actionsCounter -=1 ; rook.setXY(rS)
            elif direction == 'n':
                king = Table[kS] ; king.actionsCounter +=1 ; king.setXY(kE)
                rook = Table[rS] ; rook.actionsCounter +=1 ; rook.setXY(rE)
        elif len(lastPlay)==4: # Promote
            xy = Rewind.positionConverter(lastPlay,3)[0]
            if direction == 'b':
                promote = Table[xy]
                self = Chess.PromoteDict[promote]
                Chess.pieces.append(self)
                self.setXY(xy)
                Chess.pieces.remove(promote)
                Rewind.PosInTransc -= 1
                Rewind.AnalyzeTranscript('b',moveCounter)
            elif direction == 'n':
                self = Table[xy]
                promote = next((k for k,v in Chess.PromoteDict.items() if v==self),None)
                Chess.pieces.append(promote)
                promote.setXY(xy)
                Chess.pieces.remove(self)
        elif len(lastPlay)==7: # EnPassant
            startXY,endXY,objXY = Rewind.positionConverter(lastPlay,2)
            if direction == 'b':
                self = Table[endXY]
                self.actionsCounter -=1
                enemy = Chess.TakenDict[self][moveCounter]
                Chess.pieces.append(enemy)
                self.setXY(startXY)
                enemy.setXY(objXY) 
            elif direction == 'n':
                self = Table[startXY]
                Chess.pieces.remove(Table[objXY])
                self.actionsCounter +=1
                self.setXY(endXY)
        return Table
        
    def Previous(moveCounter):
        Table = Rewind.AnalyzeTranscript('b',moveCounter)
        Rewind.PosInTransc -= 1
        return Table

    def Next(moveCounter):
        Rewind.PosInTransc += 1
        Table = Rewind.AnalyzeTranscript('n',moveCounter)
        return Table