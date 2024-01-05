from chess import Chess
from queen import Queen
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from rook import Rook

class Rewind():
    PosInTransc = -1
    
    def EnPassant(TranscriptName): # zove je verifikacija # Pravi novi possible Take i novi Take move
        with open(f'{TranscriptName}.txt','r') as f:
            text = f.readlines()
        try:
            lastPlay = text[-1].split()
            if lastPlay [3]=='move' and lastPlay[1]=='Pawn' and abs(int(lastPlay[2][1])-int(lastPlay[4][1])) == 2:
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

    def PiecesList(piece,side):
        if piece == 'Pawn':
            return Pawn(side)
        elif piece == 'Knight':
            return Knight(side)
        elif piece == 'Bishop':
            return Bishop(side)
        elif piece == 'Rook':
            return Rook(side)
        elif piece == 'Queen':
            return Queen(side)


    def AnalyzeTranscript(direction):
            Table = Chess.currentTableDict()
            try:
                lastPlay = actions[Rewind.PosInTransc].split()
                nextPlayCheck = actions[Rewind.PosInTransc+1].split()
            except IndexError:
                return
            if len(lastPlay)==5: # Move
                startXY,endXY = Rewind.positionConverter(lastPlay,2)[:2]
                if direction == 'b':
                    Table[endXY].x,Table[endXY].y = startXY
                elif direction == 'n':
                    Table[startXY].x,Table[startXY].y = endXY
                    if nextPlayCheck[1] == 'promote':
                        Rewind.PosInTransc += 1
                        Rewind.AnalyzeTranscript('n')
            elif len(lastPlay)==6: # Take
                startXY,endXY = Rewind.positionConverter(lastPlay,2)[:2]
                enemy = lastPlay[5]
                if direction == 'b':
                    side = 'b' if Table[endXY].side == 'w' else 'w'
                    Table[endXY].x,Table[endXY].y = startXY
                    a = Rewind.PiecesList(enemy,side)
                    a.x,a.y = endXY 
                elif direction == 'n':
                    Chess.pieces.remove(Table[endXY])
                    Table[startXY].x,Table[startXY].y = endXY
                    if nextPlayCheck[1] == 'promote':
                        Rewind.PosInTransc += 1
                        Rewind.AnalyzeTranscript('n')
            elif len(lastPlay)==3: # Castling
                kS,kE,rS,rE = Rewind.castlingConverter(lastPlay)
                if direction == 'b':
                    king = Table[kE] ; king.x,king.y = kS
                    rook = Table[rE] ; rook.x,rook.y = rS
                elif direction == 'n':
                    king = Table[kS] ; king.x,king.y = kE
                    rook = Table[rS] ; rook.x,rook.y = rE
            elif len(lastPlay)==4: # Promote
                xy = Rewind.positionConverter(lastPlay,3)[0]
                promote = lastPlay[2]
                if direction == 'b':
                    side = Table[xy].side
                    a = Pawn(side)
                    a.x,a.y = xy
                    Chess.pieces.remove(Table[xy])
                    Rewind.PosInTransc -= 1
                    Rewind.AnalyzeTranscript('b')
                elif direction == 'n':
                    side = Table[xy].side
                    a = Rewind.PiecesList(promote,side)
                    a.x,a.y = xy
                    Chess.pieces.remove(Table[xy])
            elif len(lastPlay)==7: # EnPassant
                startXY,endXY,objXY = Rewind.positionConverter(lastPlay,2)
                enemy = lastPlay[5]
                if direction == 'b':
                    side = 'b' if Table[endXY].side == 'w' else 'w'
                    Table[endXY].x,Table[endXY].y = startXY
                    a = Pawn(side)
                    a.x,a.y = objXY 
                elif direction == 'n':
                    Chess.pieces.remove(Table[objXY])
                    Table[startXY].x,Table[startXY].y = endXY
            return Table
            
            

    def Previous():
        Table = Rewind.AnalyzeTranscript('b')
        Rewind.PosInTransc -= 1
        return Table

    def Next():
        Rewind.PosInTransc += 1
        Table = Rewind.AnalyzeTranscript('n')
        return Table