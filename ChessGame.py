from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
import time
from chess import Chess
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from rook import Rook
from AI import AI
from transcript import Rewind
from rendering import Rendering
from computerAI import ComputerAI
import os

ImagesLocation = os.path.join(os.path.dirname(__file__),'Slike')

window = Tk()
window.title("Chess")
window.resizable(False,False)
X=1550 ; Y=1000
window.geometry(f"{X}x{Y}")



# >>> IMPORT <<<
class Import():
    
    def ImageImport():
        imageCount = 31
        ImageList = [] ; Img_wPwS = [] ; Img_wPbS = [] ; Img_bPwS = [] ; Img_bPbS = []
        for i in range(imageCount): # Image upload
            image = ImageTk.PhotoImage(Image.open(os.path.join(ImagesLocation,f"{i}.png")))
            ImageList.append(image) if i<3 else \
                (Img_wPwS.append(image) if i <10 else \
                (Img_wPbS.append(image) if i < 17 else \
                (Img_bPwS.append(image) if i < 24 else \
                (Img_bPbS.append(image)))))
        return  ImageList,Img_wPwS,Img_wPbS,Img_bPwS,Img_bPbS
    Images,Img_wPwS,Img_wPbS,Img_bPwS,Img_bPbS = ImageImport()

    def Hover(event,button):    # Green                          # Red                             # Light Blue                      # Yellow  
        global hover
        hover = event.widget
        if button.cget('bg') !='#00BB00' and button.cget('bg') !='#FF0000' and button.cget('bg') !='#00AACC' and button.cget('bg') !='#FFFF00':
            button.config(background='silver')
        elif button.cget('bg') =='#00BB00':
            button.config(background='#008800')
        elif button.cget('bg') =='#FF0000':
            button.config(background='#AD0000')
        elif button.cget('bg') =='#00AACC':
            button.config(background='#0066AD')
        elif button.cget('bg') =='#FFFF00':
            button.config(background='#ADAD00')

    def ClearHover(event,button):
        if button.cget('bg') == 'silver':
            button.config(background='SystemButtonFace')
        elif button.cget('bg') =='#008800':
            button.config(background='#00BB00')
        elif button.cget('bg') =='#AD0000':
            button.config(background='#FF0000')
        elif button.cget('bg') =='#0066AD':
            button.config(background='#00AACC')
        elif button.cget('bg') =='#ADAD00':
            button.config(background='#FFFF00')
    
    # Icon   
    window.iconbitmap(os.path.join(ImagesLocation,"ico.ico"))   

    def ButtonsCreating(images):
        global canvas
        # Canvas
        canvas = Canvas(window, width=images[0].width()+550, height=images[0].height())
        canvas.place(anchor=NW,x=0,y=0)
        canvas.create_image(0,0, anchor=NW, image=images[0])
            # Square buttons
        BorderDistance = 97 ; ButtonDimension = 101.7
        ButtonReferences = list(Chess.emptyTableDict().keys())
        ButtonDict = {}
        for i in range(64): 
            n=8                 # Ovaj deo je da se napravi matrica (8*8) od liste 
            x = i//n            # zbog postavke BUTTONA na CANVAS (pozicije XY)
            y = i-x*n           # Radi izracunavanja koordinata preko FORMULE
                                        
            button = Button(window)                                                           # kreiranje Buttona
            button.text = ButtonReferences[i]                                                 # ubacivanje Atributa koji opisuje poziciju. Improvizovana ButtonID
            button.config(border=2,command=lambda text = button.text: (GameFlow.GameMechanic(text)))     # FUNKCIJA Buttona
            button.bind("<Enter>",lambda event, text = button: Import.Hover(event,text))                # Hover
            button.bind("<Leave>",lambda event, text = button: Import.ClearHover(event,text))         # Clear Hover
            button_window = canvas.create_window(1,1, anchor=NW, window=button)               # kreiranje prozora buttona
            canvas.coords(button_window,(BorderDistance+y*ButtonDimension),(BorderDistance+(7-x)*ButtonDimension))                                # postavljanje buttona na EKRAN
            ButtonDict[button.text] = button                                                  # Ubacivanje Buttona u RECNIK                            

            if x%2==0: # Default Square Color
                if y%2==1:
                    button.config(image=images[1]) ; button.color = 'w' 
                else:
                    button.config(image=images[2]) ; button.color = 'b'
            else:
                if y%2==1:
                    button.config(image=images[2]) ; button.color = 'b'
                else:
                    button.config(image=images[1]) ; button.color = 'w'
        return ButtonDict
    ButtonDict: dict = None

    def RightPanel_FirstScreen():
        global MoveOutput,ExecutionTime,ExecutionTime_window,buttonSG_window,buttonGM_window
        # Text
        MoveOutput = Text(window, width= 550, height=22, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        MoveOutput.place(anchor=NW,x=1000,y=2)

        exTiText = 'Standard Game:\nNormal Chess game\nwith all rules applied\n\nGod Mode:\nDelete: Remove Piece\nInsert: Freely move Piece\nRightClick: Change Turn '
        ExecutionTime = Label(window, font=('Eras Demi ITC', 16), width=24, height=8, bd=2, relief='groove', text=exTiText)
        ExecutionTime_window = canvas.create_window(1220, 787, anchor=NW, window=ExecutionTime)

        buttonSG = Button(window, border=3, font=('Eras Demi ITC', 24), width=9, height=2, text='Standard\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvas.create_window(1010,780, anchor=NW, window=buttonSG)
        buttonGM = Button(window, border=3, font=('Eras Demi ITC', 24), width=9, height=2, text='God Mode', command=lambda: GameFlow.GodMode())
        buttonGM_window = canvas.create_window(1010,890, anchor=NW, window=buttonGM)
    
    def RightPanel_SecondScreen():
        global buttonNG_window,buttonBack_window,buttonNext_window

        buttonNG = Button(window, border=3, font=('Eras Demi ITC', 24), width=9, height=2, text='New Game', command=lambda: GameFlow.NewGame())
        buttonNG_window = canvas.create_window(1010,780, anchor=NW, window=buttonNG)

        buttonBack = Button(window, border=3, font=('Eras Demi ITC', 33), width=3, height=1, text='⯬🢠', command=lambda: Actions.Previous())
        buttonBack_window = canvas.create_window(1010,900, anchor=NW, window=buttonBack)
        buttonNext = Button(window, border=3, font=('Eras Demi ITC', 33), width=3, height=1, text='⯮🢡', command=lambda: Actions.Next())
        buttonNext_window = canvas.create_window(1108,900, anchor=NW, window=buttonNext)

        canvas.itemconfig(buttonBack_window,state='hidden')
        canvas.itemconfig(buttonNext_window,state='hidden')

    
    def StartingScreen():
        global FirstOpponent,SecondOpponent
        FirstOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        FirstOpponent_window = canvas.create_window(1280,900, anchor=NW, window=FirstOpponent)
        FirstOpponent.insert(1.0, "1stPlayer")
        Import.StartingScreenWindow.append(FirstOpponent_window)

        SecondOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        SecondOpponent_window = canvas.create_window(1280,945, anchor=NW, window=SecondOpponent)
        SecondOpponent.insert(1.0, "2ndPlayer")
        Import.StartingScreenWindow.append(SecondOpponent_window)

        SavingTranscript = Button(window, border=5, width=16, height=3, text='Saving Game\nTranscript', font=('Tahoma', 18), command=lambda: Import.SavedGames('players'))
        SavingTranscript_window = canvas.create_window(1300,780, anchor=NW, window=SavingTranscript)
        NoTranscript = Button(window, border=5, width=12, height=4, text='Casual Game\nNo Transcript', font=('Tahoma', 27), command=lambda: Import.SavedGames(None))
        NoTranscript_window = canvas.create_window(1010,780, anchor=NW, window=NoTranscript)
        Import.StartingScreenWindow.append(SavingTranscript_window)
        Import.StartingScreenWindow.append(NoTranscript_window)

    StartingScreenWindow = []

    def ShowcaseScreen():
        global Showcase,gif,Phase
        Phase = "Start"
        gif = ImageTk.PhotoImage(Image.open(os.path.join(ImagesLocation,"ChessGame.png")))
        Showcase = Label(window, image=gif)
        Showcase.place(anchor=NW,x=0,y=0)
        window.after(13000, Import.hideShowcase)     

    def hideShowcase():
        global hideShowcase_executed
        if not hideShowcase_executed:
            Showcase.place_forget()
            Import.ButtonDict = Import.ButtonsCreating(Import.Images)
            Import.StartingScreen()
            hideShowcase_executed = True

    def SavedGames(option):
        global TranscriptName
        Player1,Player2 = None,None
        if option is not None:
            Player1 = FirstOpponent.get("1.0", "end-1c")
            Player2 = SecondOpponent.get("1.0", "end-1c")
            TranscriptName = f"{Player1}vs{Player2}"
        else:
            TranscriptName = 'Game'

        for w in Import.StartingScreenWindow:
            canvas.itemconfigure(w, state='hidden')
        try:
            with open(f'{TranscriptName}.txt','x') as f:
                pass
        except FileExistsError:
            pass
        Import.RightPanel_FirstScreen()

    ExtraPiecesButtons = [] 
    def PawnPromotionButtons():
        Import.ExtraPiecesButtons.clear()
        buttonQueen = Button(window, border=5, command=lambda: Actions.PawnPromotion(Queen(Self.side,'extra')))
        buttonQueen_window = canvas.create_window(1254,784, anchor=NW, window=buttonQueen)
        Import.ExtraPiecesButtons.append(buttonQueen_window)

        buttonBishop = Button(window, border=5, command=lambda: Actions.PawnPromotion(Bishop(Self.side,'extra')))
        buttonBishop_window = canvas.create_window(1254,892, anchor=NW, window=buttonBishop)
        Import.ExtraPiecesButtons.append(buttonBishop_window)

        buttonKnight = Button(window, border=5, command=lambda: Actions.PawnPromotion(Knight(Self.side,'extra')))
        buttonKnight_window = canvas.create_window(1392,892, anchor=NW, window=buttonKnight)
        Import.ExtraPiecesButtons.append(buttonKnight_window)

        buttonRook = Button(window, border=5, command=lambda: Actions.PawnPromotion(Rook(Self.side,'extra')))
        buttonRook_window = canvas.create_window(1392,784, anchor=NW, window=buttonRook)
        Import.ExtraPiecesButtons.append(buttonRook_window)

        if Turn == 1:
            buttonQueen.config(image=Import.Img_wPbS[1])
            buttonBishop.config(image=Import.Img_wPbS[2])
            buttonKnight.config(image=Import.Img_wPbS[3])
            buttonRook.config(image=Import.Img_wPbS[5])
        else:
            buttonQueen.config(image=Import.Img_bPwS[1])
            buttonBishop.config(image=Import.Img_bPwS[2])
            buttonKnight.config(image=Import.Img_bPwS[3])
            buttonRook.config(image=Import.Img_bPwS[5])

    # Future Updated (Nothing for now)
    def ExtraButtons():    
        buttonNormalGame = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvas.create_window(1000,880, anchor=NW, window=buttonNormalGame)

        buttonVSComputer = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvas.create_window(1000,880, anchor=NW, window=buttonVSComputer)

        buttonMateInN = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvas.create_window(1000,880, anchor=NW, window=buttonMateInN)

    def freeModeButtons():
        buttonKing = Button(window, border=5, command=lambda: Actions.PawnPromotion(King(Self.side)))
        buttonKing_window = canvas.create_window(1392,892, anchor=NW, window=buttonKing)
        Import.ExtraPiecesButtons.append(buttonKing_window)

        buttonPawn = Button(window, border=5, command=lambda: Actions.PawnPromotion(Pawn(Self.side,'extra')))
        buttonPawn_window = canvas.create_window(1392,784, anchor=NW, window=buttonPawn)
        Import.ExtraPiecesButtons.append(buttonPawn_window)

        if Turn == 1:
            buttonKing.config(image=Import.Img_wPbS[0])
            buttonPawn.config(image=Import.Img_wPbS[6])
        else:
            buttonKing.config(image=Import.Img_bPwS[0])
            buttonPawn.config(image=Import.Img_bPwS[6])

# >>> MOVES  <<<
class Actions():
    # Selecting Piece       
    def verification(position,startingTime): # Ovo je kada SELEKTUJEMO FIGURU  >>> First Click <<<
        def verify(xy):
            global Self,kW,qW,kB,qB
            if isinstance(CurrentTableDict[xy],Chess):
                Self = CurrentTableDict[xy]
                Rendering.borderDefault()
                Rendering.borderCheck(PossibleCheck,Import.ButtonDict)
                Rendering.borderColors(xy,Import.ButtonDict,Self,CurrentTableDict,possibleActionsDict,enPassant)
                try:
                    kW,qW,kB,qB=Rendering.borderCastling(Import.ButtonDict,Self,Turn,CurrentTableDict)
                except TypeError:
                    None

        try:
            if Turn == 1 and CurrentTableDict[position].side == 'w':
                verify(position)
            if Turn == -1 and CurrentTableDict[position].side == 'b':
                verify(position)
        except (AttributeError,KeyError):
            None
        verificationTime = time.time()
        Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
        endTime = time.time()
        Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,verificationTime,None) 

    # Taking Actions
    moveCounter: int
    def movingDone(newXY):
        global Self,Turn
        output = None ; transcript = None
        if CurrentTableDict[newXY] =='':
            if newXY in possibleActionsDict[Self]:
                if isinstance(Self,King):
                    output,transcript = Self.move(CurrentTableDict,newXY)
                elif enPassant == newXY and isinstance(Self,Pawn):
                    output,transcript = Actions.enPassantTake(enPassant,enPassant_objPos)
                    return output,transcript,"#FF0000"
                elif directAttackers and Self not in Defenders.keys() and newXY in DangerTeamSolve:
                    output,transcript = Self.move(CurrentTableDict,newXY)      
                elif not directAttackers and ((Self not in Defenders.keys()) or (Self in Defenders.keys() and newXY in Defenders[Self])):
                    output,transcript = Self.move(CurrentTableDict,newXY)
                else:
                    return False,False,False
            else:
                return False,False,False
            return output,transcript,"#00BB00"
        else:
            return None,None,None
           
    def takingDone(enemyXY):
        global Self,Turn
        output = None ; transcript = None
        if CurrentTableDict[enemyXY].side != Self.side:
            if enemyXY in possibleActionsDict[Self]:
                if isinstance(Self,King):
                    output,transcript = Self.take(CurrentTableDict,CurrentTableDict[enemyXY],Actions.moveCounter)
                elif directAttackers and Self not in Defenders.keys() and enemyXY in DangerTeamSolve:
                    output,transcript = Self.take(CurrentTableDict,CurrentTableDict[enemyXY],Actions.moveCounter)
                elif not directAttackers and ((Self not in Defenders.keys()) or (Self in Defenders.keys() and enemyXY in Defenders[Self])):
                    output,transcript = Self.take(CurrentTableDict,CurrentTableDict[enemyXY],Actions.moveCounter)
                else:
                    return False,False,False
            else:
                return False,False,False  
            return output,transcript,"#FF0000"
        else:
            return None,None,None

    def enPassantTake(newXY,objXY):
        global Self
        position = Chess.NotationTableDict[Self.position()]
        Self.x,Self.y = newXY
        Chess.MovesDict[Self]+=1
        if Self not in Chess.TakenDict:
            Chess.TakenDict[Self] = {}
        Chess.TakenDict[Self][Actions.moveCounter+1]=CurrentTableDict[objXY]
        transcript = f"{str(Self)[1:]} {position} take {Chess.NotationTableDict[newXY]} {str(CurrentTableDict[objXY])[1:]} {Chess.NotationTableDict[objXY]}\n"
        moveOutput = f"{str(Self).ljust(8)}{(position.ljust(4)+'❌').ljust(7)}{Chess.NotationTableDict[newXY]} {CurrentTableDict[objXY]} {Chess.NotationTableDict[objXY]}"
        Chess.pieces.remove(CurrentTableDict[objXY])
        return moveOutput,transcript

    def castlingDone(ownRook):
        global Self,Turn
        output = None ; transcript = None
        OwnRook = CurrentTableDict[ownRook]
        if isinstance(Self,King) and isinstance(OwnRook,Rook):
            try:
                output,transcript = Self.castling(OwnRook,kW,qW,kB,qB)
                return output,transcript,"#00AACC"
            except Exception:
                return None,None,None   
        else:
            return None,None,None

    def pieceChange(newSelf):
        global Self
        startingTime = time.time()
        if Self.side == CurrentTableDict[newSelf].side:
            Actions.verification(newSelf,startingTime)

    def PawnPromotion(choice):  
        global Self,Phase
        if Phase == 'Pawn Promotion':
            startingTime = time.time()
            for b in Import.ExtraPiecesButtons:
                canvas.itemconfigure(b,state='hidden')
            canvas.itemconfigure(ExecutionTime_window,state='normal')

            promote = choice
            promote.x,promote.y = Self.position()
            with open(f'{TranscriptName}.txt','a') as f:
                f.write(f"{Actions.moveCounter} promote {str(promote)[1:]} {Chess.NotationTableDict[promote.position()]}\n")
            output = f"{' -'.ljust(4)}{str(Self).ljust(8)}{(Chess.NotationTableDict[promote.position()].ljust(5)+'⛨').ljust(8)}{promote}"
            if posInTransc <-1:
                Rendering.delMovesDone(MoveOutput,posInTransc)
            Rendering.printMovesDone(MoveOutput,"#7700FF",output,None)
            Chess.PromoteDict[promote]=Self
            Chess.pieces.remove(Self)
            Self = None
            Phase = 'Game Mechanic'
            Actions.End_Turn()

            actionTime = time.time()
            Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
            endTime = time.time()
            Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,None,actionTime)

    def Previous():
        global Self,Turn,CurrentTableDict
        startingTime = time.time()
        if Phase == 'Game Mechanic':
            CurrentTableDict = Rewind.Previous(Actions.moveCounter)
            Turn *=-1 ; Self =None ; Actions.moveCounter -=1
            Actions.End_Turn()
            Rendering.printMovesDone(MoveOutput,"#0000FF",None,posInTransc)
            
            actionTime = time.time()
            Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
            endTime = time.time()
            Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,None,actionTime)  

    def Next():
        global Self,Turn,CurrentTableDict
        startingTime = time.time()
        if Phase == 'Game Mechanic':
            CurrentTableDict = Rewind.Next(Actions.moveCounter)
            Turn *=-1 ; Self =None ; Actions.moveCounter +=1
            Actions.End_Turn()
            Rendering.printMovesDone(MoveOutput,"#0000FF",None,posInTransc)

            actionTime = time.time()
            Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
            endTime = time.time()
            Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,None,actionTime) 

    # Finishing Turn
    ActionsDone = [movingDone, takingDone, castlingDone, pieceChange]
    def action(act=None):
        global Phase,Self,Turn
        for a in range(4):
            output,transcript,color = Actions.ActionsDone[a](act)
            if output is None:
                continue
            elif output is False:
                Self=None ; Rendering.borderDefault() ; Rendering.borderCheck(PossibleCheck,Import.ButtonDict)
                return
            else:
                if isinstance(Self,Pawn) and (Self.x == 7 or Self.x == 0):
                    canvas.itemconfigure(ExecutionTime_window,state='hidden')
                    Import.PawnPromotionButtons()
                    Actions.ActionResult(output,transcript,color)
                    Phase = 'Pawn Promotion'
                    return
                else:
                    Self=None
                    return output,transcript,color
    
    def ActionResult(output,transcript,color):
        global Turn,posInTransc
        Turn *=-1
        Actions.moveCounter +=1  
        with open(f'{TranscriptName}.txt','a') as f:
            f.write(f'{Actions.moveCounter} {transcript}')
        output = f"{(str(Actions.moveCounter)+'.').ljust(4)}{output}"
        if posInTransc <-1:
            Rendering.delMovesDone(MoveOutput,posInTransc)
        Rendering.printMovesDone(MoveOutput,color,output,None)
        if posInTransc < -1:
            with open(f'{TranscriptName}.txt','r+') as f:
                text = f.readlines()
                lastAction = text[-1]
                f.truncate(0)
            with open(f'{TranscriptName}.txt','a') as f:
                f.writelines(text[:posInTransc])
                f.write(lastAction)
                posInTransc = Rewind.ResetPosition() 

    def End_Turn():
        global posInTransc,DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,CurrentTableDict,PossibleCheck,possibleActionsDict,enPassant,enPassant_objPos
        GameOver=None
        CurrentTableDict = Chess.currentTableDict()
        try:
            enPassant,enPassant_objPos = Rewind.EnPassant(TranscriptName)
        except TypeError:
            enPassant=None
        selfKing,TeamOptions,DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,possibleActionsDict = AI.dangerZone(Turn,CurrentTableDict,enPassant)
        if directAttackers:
            PossibleCheck = selfKing.position()
            GameOver = AI.GameOverCheck(selfKing,TeamOptions,directAttackers,DangerKingSolve,DangerTeamSolve)
        elif not DangerKingSolve or len(Chess.pieces)<5:
            PossibleCheck = None
            GameOver = AI.GameOverCheck(selfKing,TeamOptions,directAttackers,DangerKingSolve,DangerTeamSolve)
        else:
            PossibleCheck = None

        Rendering.borderDefault()
        Rendering.borderCheck(PossibleCheck,Import.ButtonDict)
        rewindButtonsManage,posInTransc = Rewind.Get_Transcript_and_Position(TranscriptName)
        Rendering.PreviousNextButtons(canvas,buttonNext_window,buttonBack_window,rewindButtonsManage)
        GameFlow.GameOver(Turn,GameOver)

# >>> GAME <<<
class GameFlow:
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
        
    def NewGame():
        global CurrentTableDict,posInTransc
        Import.StartingScreen()
        canvas.itemconfigure(ExecutionTime_window, state='hidden')
        canvas.itemconfigure(buttonBack_window,state='hidden')
        canvas.itemconfigure(buttonNext_window,state='hidden')
        Chess.pieces.clear() ; Chess.MovesDict.clear() ; Chess.TakenDict.clear()
        CurrentTableDict = Chess.currentTableDict()
        MoveOutput.delete('1.0', END)
        Rendering.borderDefault()
        posInTransc = Rewind.ResetPosition()
        Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)

    def StandardGame():
        global Phase,Turn,Self,PossibleCheck,DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,CurrentTableDict,posInTransc,enPassant,possibleActionsDict 
        startingTime = time.time()
        
        Turn=1 ; Self=None ; Actions.moveCounter = 0 ; PossibleCheck=None ; Phase = 'Game Mechanic' ; posInTransc =-1 ; enPassant=None
        with open('Game.txt','w') as f:
            f.truncate(0)
        GameFlow.MouseKeyboard(None,None,None,'win')
        GameFlow.StartingPosition()
        CurrentTableDict = Chess.currentTableDict()
        DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,possibleActionsDict = AI.dangerZone(Turn,CurrentTableDict,enPassant)[2:]
       
        canvas.itemconfigure(buttonGM_window,state='hidden')
        canvas.itemconfigure(buttonSG_window,state='hidden')
        Import.RightPanel_SecondScreen()

        verificationTime = time.time()

        Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
        endTime = time.time()
        Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,verificationTime,None)
          
    def GameMechanic(xy):
        startingTime = time.time()
        if Phase == 'Game Mechanic':
            if Self == None:
                Actions.verification(xy,startingTime) 
            else:
                try:
                    output,transcript,color=Actions.action(xy)
                except TypeError:
                    output=None
                if output:
                    Actions.ActionResult(output,transcript,color)
                    Actions.End_Turn()
                    actionTime = time.time()
                    Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
                    endTime = time.time()
                    Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,None,actionTime)  

    def GameOver(turn,GameOver=None):
        global Phase
        if GameOver is not None:
            if GameOver == 'CheckMate':
                winner = "\tWhite WON!!!" if turn == -1 else "\tBlack WON!!!"
            elif GameOver == 'StaleMate':
                winner = ''
            with open(f'{TranscriptName}.txt','a') as f:
                f.write(GameOver)
            Phase = 'Game Over'
            output = str(GameOver+winner)
            Rendering.printMovesDone(MoveOutput,"#D2AA00",output,None)

    # Extra Methods
    def GodMode():
        GameFlow.StandardGame()
        GameFlow.MouseKeyboard('turn','remove','moving','win')

    def MouseKeyboard(rClick=None,delete=None,insert=None,win=None):
        def escPressed(event):
            global Self
            if Phase == "Start":
                Import.hideShowcase()
            elif Phase == "Game Mechanic":
                startTime = time.time()
                Self = None
                Rendering.borderDefault()
                verificationTime = time.time()
                endTime = time.time()
                Rendering.timeShowing(ExecutionTime,Turn,Self,startTime,endTime,verificationTime,None)
        window.bind("<Escape>", escPressed)

        def spacePressed(event):
            start = time.time()
            for _ in range(100):
                AllActions_Dict,AllActionsNum_Dict=ComputerAI.PositionAnalyze(Turn,CurrentTableDict,enPassant,ourTeam=True)
                AllActions_Dict_enemy,AllActionsNum_Dict_enemy=ComputerAI.PositionAnalyze(Turn,CurrentTableDict,enPassant,ourTeam=False)
                
                '''
                
                print('--'*33)
                print('--'*33)
                for k,v in AllActions_Dict.items():
                    print([k],'---',v)
                print('--'*33)
                print(AllActionsNum_Dict)
                print('--'*33)
                '''
                a = ComputerAI.PointCalulator(AllActionsNum_Dict)
                '''
                print('--'*33)
                for k,v in AllActions_Dict_enemy.items():
                    print([k],'---',v)
                print('--'*33)
                print(AllActionsNum_Dict_enemy)
                print('--'*33)
                print('+++'*33)
                '''
                b = ComputerAI.PointCalulator(AllActionsNum_Dict_enemy)
            end = time.time()
            print('our',a)
            print('enemy',b)
            print(f'{(end-start)* 1000:,.2f} ms')
        window.bind("<space>",spacePressed)   

        if rClick == 'turn':
            def rightClick(event):
                global Turn,Self,PossibleCheck,DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,CurrentTableDict
                startTime = time.time()
                Turn *=-1
                Self = None
                Actions.End_Turn()

                verificationTime = time.time()
                Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
                endTime = time.time()
                Rendering.timeShowing(ExecutionTime,Turn,Self,startTime,endTime,verificationTime,None)
            window.bind("<Button-3>", rightClick)

        if delete == 'remove':
            def deletePressed(event):
                global Self,CurrentTableDict              
                startTime = time.time()
                if Self is not None and not isinstance(Self,King):
                    Chess.pieces.remove(Self)
                    Self = None
                    Rendering.borderDefault()     
                    Actions.End_Turn()

                    verificationTime = time.time()
                    Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
                    endTime = time.time()
                    Rendering.timeShowing(ExecutionTime,Turn,Self,startTime,endTime,verificationTime,None)
            window.bind("<Delete>", deletePressed)

        if insert == 'moving':
            def insertPressed(event):
                global Self,CurrentTableDict
                startTime = time.time()  
                XY = hover.text
                if Self is not None:
                    Self.x,Self.y = XY[0],XY[1]
                    Self = None
                    Actions.End_Turn()

                    verificationTime = time.time()
                    Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.Img_wPwS,Import.Img_wPbS,Import.Img_bPwS,Import.Img_bPbS,Import.Images)
                    endTime = time.time()
                    Rendering.timeShowing(ExecutionTime,Turn,Self,startTime,endTime,verificationTime,None)
            window.bind("<Insert>", insertPressed)

        if win == 'win':
            def freeMode(event):
                global Phase
                if Phase == 'Game Over':
                    with open(f'{TranscriptName}.txt','r+') as f:
                        text = f.readlines()
                        f.truncate(0)
                    with open(f'{TranscriptName}.txt','w') as f:
                        f.writelines(text[:-1])
                    Rendering.delMovesDone(MoveOutput,-2)
                    Phase = 'Game Mechanic'
            window.bind('\u0075\u0076',freeMode)
            window.bind('\u0076\u0075',freeMode)

GameFlow.MouseKeyboard()
hideShowcase_executed = False
Import.ShowcaseScreen()

window.mainloop()