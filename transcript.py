from ChessParent import Chess

class Rewind:
    FullTranscript  = None
    PosInTransc     = -1
    
    def EnPassant(TranscriptName): # zove je verifikacija # Pravi novi possible Take i novi Take move
        with open(f'{TranscriptName}.txt','r') as f:
            text = f.readlines()
        try:
            lastPlay = text[Rewind.PosInTransc].split()
            XS =int(lastPlay[2][1])
            XE =int(lastPlay[4][1])
            if lastPlay[3]=='move' and lastPlay[1]=='Pawn' and abs(XS-XE) ==2:
                Y =Rewind.letterToNum(lastPlay[2][0])
                return ((XS+XE)//2,Y),(XE,Y)
        except (IndexError,ValueError):
            return

    def ResetPosition():
        Rewind.PosInTransc = -1
        return Rewind.PosInTransc

    def UpdateTranscript(TranscriptName=None):
        if TranscriptName:
            with open(f'{TranscriptName}.txt','r') as f:
                Rewind.FullTranscript = f.readlines()
        
    def letterToNum(sign):
        return ord(sign)+1 - ord('A')

    def castlingConverter(play):
        if play[1][0] == 'K' and play[2][0] == 'b':
            kingStartPos: tuple = (8,5)
            rookStartPos: tuple = (8,8)
            kingEndPos: tuple = (8,7)
            rookEndPos: tuple = (8,6)
        elif play[1][0] == 'K' and play[2][0] == 'w':
            kingStartPos: tuple = (1,5)
            rookStartPos: tuple = (1,8)
            kingEndPos: tuple = (1,7)
            rookEndPos: tuple = (1,6)
        elif play[1][0] == 'Q' and play[2][0] == 'b':
            kingStartPos: tuple = (8,5)
            rookStartPos: tuple = (8,1)
            kingEndPos: tuple = (8,3)
            rookEndPos: tuple = (8,4)
        else:
            kingStartPos: tuple = (1,5)
            rookStartPos: tuple = (1,1)
            kingEndPos: tuple = (1,3)
            rookEndPos: tuple = (1,4)
        return kingStartPos,kingEndPos,rookStartPos,rookEndPos

    def positionConverter(play,num):
        EndingPos = None
        objPos = None
        xS: int = int(play[num][1])
        yS: int = Rewind.letterToNum(play[num][0])
        StartingPos: tuple = (xS,yS)
        try:
            xE: int = int(play[num+2][1])
            yE: int = Rewind.letterToNum(play[num+2][0])
            EndingPos: tuple = (xE,yE)

            xO: int = int(play[num+4][1])
            yO: int = Rewind.letterToNum(play[num+4][0])
            objPos: tuple = (xO,yO)
        except IndexError:
            None
        return StartingPos,EndingPos,objPos

    def AnalyzeTranscript(direction,moveCounter):
        Table = Chess.currentTableDict()
        lastPlay = Rewind.FullTranscript[Rewind.PosInTransc].split()
        nextPlayCheck = Rewind.FullTranscript[Rewind.PosInTransc+1].split()
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
                Rewind.PosInTransc -=1
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