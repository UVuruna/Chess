from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
import time
from chess import Chess
from Pieces import *
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
        imageCount = 32
        ImageList = [] ; Img_wPwS = [] ; Img_wPbS = [] ; Img_bPwS = [] ; Img_bPbS = []
        for i in range(imageCount): # Image upload
            image = ImageTk.PhotoImage(Image.open(os.path.join(ImagesLocation,f"{i}.png")))
            ImageList.append(image) if i<4 else \
                (Img_wPwS.append(image) if i <11 else \
                (Img_wPbS.append(image) if i < 18 else \
                (Img_bPwS.append(image) if i < 25 else \
                (Img_bPbS.append(image)))))
        return  ImageList,Img_wPwS,Img_wPbS,Img_bPwS,Img_bPbS
    Images,Img_wPwS,Img_wPbS,Img_bPwS,Img_bPbS = ImageImport()
    AllImages = [Images,Img_wPwS,Img_wPbS,Img_bPwS,Img_bPbS]

    def Hover(event,button):    # Green                          # Red                             # Light Blue                      # Yellow  
        global hover
        hover = event.widget
        if button.cget('bg') !=Rendering.green and button.cget('bg') !=Rendering.red and button.cget('bg') !=Rendering.cyan and button.cget('bg') !=Rendering.yellow:
            button.config(background='silver')
        elif button.cget('bg') ==Rendering.green:
            button.config(background='#008800')
        elif button.cget('bg') ==Rendering.red:
            button.config(background='#AD0000')
        elif button.cget('bg') ==Rendering.cyan:
            button.config(background='#0066AD')
        elif button.cget('bg') ==Rendering.yellow:
            button.config(background='#ADAD00')

    def ClearHover(event,button):
        if button.cget('bg') == 'silver':
            button.config(background='SystemButtonFace')
        elif button.cget('bg') =='#008800':
            button.config(background=Rendering.green)
        elif button.cget('bg') =='#AD0000':
            button.config(background=Rendering.red)
        elif button.cget('bg') =='#0066AD':
            button.config(background=Rendering.cyan)
        elif button.cget('bg') =='#ADAD00':
            button.config(background=Rendering.yellow)
    # Icon   
    window.iconbitmap(os.path.join(ImagesLocation,"ico.ico"))   

    def ButtonsCreating(images):
        global canvasTable,canvasSide
        # Canvas 1
        canvasTable = Canvas(window, width=1000, height=1000)
        canvasTable.place(anchor=NW,x=0,y=0)
        canvasTable.create_image(0,0, anchor=NW, image=images[0])
        # Canvas 2
        canvasSide = Canvas(window, width=550, height=1000)
        canvasSide.place(anchor=NW,x=1000,y=0)
        canvasSide.create_image(0,0, anchor=NW, image=images[3])

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
            button_window = canvasTable.create_window(1,1, anchor=NW, window=button)               # kreiranje prozora buttona
            canvasTable.coords(button_window,(BorderDistance+y*ButtonDimension),(BorderDistance+(7-x)*ButtonDimension))                                # postavljanje buttona na EKRAN
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
        MoveOutput = Text(window, width= 550, height=22, bg= '#535a5e', font=('Tahoma', 22))
        MoveOutput.place(anchor=NW,x=1000,y=2)

        exTiText = 'Standard Game:\nNormal Chess game\nwith all rules applied\n\nGod Mode:\nDelete: Remove Piece\nInsert: Freely move Piece\nRightClick: Change Turn '
        ExecutionTime = Label(window, font=('Eras Demi ITC', 16), width=24, height=8, bd=2, relief='groove', text=exTiText)
        ExecutionTime_window = canvasSide.create_window(220, 787, anchor=NW, window=ExecutionTime)

        buttonSG = Button(window, border=3, font=('Eras Demi ITC', 24), width=9, height=2, text='Standard\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvasSide.create_window(10,780, anchor=NW, window=buttonSG)
        buttonGM = Button(window, border=3, font=('Eras Demi ITC', 24), width=9, height=2, text='God Mode', command=lambda: GameFlow.GodMode())
        buttonGM_window = canvasSide.create_window(10,890, anchor=NW, window=buttonGM)
    
    def RightPanel_SecondScreen():
        global buttonNG_window,buttonBack_window,buttonNext_window

        buttonNG = Button(window, border=3, font=('Eras Demi ITC', 24), width=9, height=2, text='New Game', command=lambda: GameFlow.NewGame())
        buttonNG_window = canvasSide.create_window(10,780, anchor=NW, window=buttonNG)

        buttonBack = Button(window, border=3, font=('Eras Demi ITC', 33), width=3, height=1, text='⯬🢠', command=lambda: GamePlay.Previous())
        buttonBack_window = canvasSide.create_window(10,900, anchor=NW, window=buttonBack)
        buttonNext = Button(window, border=3, font=('Eras Demi ITC', 33), width=3, height=1, text='⯮🢡', command=lambda: GamePlay.Next())
        buttonNext_window = canvasSide.create_window(108,900, anchor=NW, window=buttonNext)

        Rendering.HidingButtons(canvasSide,buttonBack_window,buttonNext_window)

    def StartingScreen():
        global FirstOpponent,SecondOpponent
        FirstOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        FirstOpponent_window = canvasSide.create_window(280,900, anchor=NW, window=FirstOpponent)
        FirstOpponent.insert(1.0, "1stPlayer")
        Import.StartingScreenWindow.append(FirstOpponent_window)

        SecondOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        SecondOpponent_window = canvasSide.create_window(280,945, anchor=NW, window=SecondOpponent)
        SecondOpponent.insert(1.0, "2ndPlayer")
        Import.StartingScreenWindow.append(SecondOpponent_window)

        SavingTranscript = Button(window, border=5, width=16, height=3, text='Saving Game\nTranscript', font=('Tahoma', 18), command=lambda: Import.SavedGames('players'))
        SavingTranscript_window = canvasSide.create_window(300,780, anchor=NW, window=SavingTranscript)
        NoTranscript = Button(window, border=5, width=12, height=4, text='Casual Game\nNo Transcript', font=('Tahoma', 27), command=lambda: Import.SavedGames(None))
        NoTranscript_window = canvasSide.create_window(10,780, anchor=NW, window=NoTranscript)
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

        Rendering.HidingButtons(canvasSide,*Import.StartingScreenWindow)
        try:
            with open(f'{TranscriptName}.txt','x') as f:
                pass
        except FileExistsError:
            pass
        Import.RightPanel_FirstScreen()

    def PawnPromotionButtons():
        Import.ExtraPiecesButtons.clear()
        buttonQueen = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(Queen(Self.side,'extra')))
        buttonQueen_window = canvasSide.create_window(254,784, anchor=NW, window=buttonQueen)
        Import.ExtraPiecesButtons.append(buttonQueen_window)

        buttonBishop = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(Bishop(Self.side,'extra')))
        buttonBishop_window = canvasSide.create_window(254,892, anchor=NW, window=buttonBishop)
        Import.ExtraPiecesButtons.append(buttonBishop_window)

        buttonKnight = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(Knight(Self.side,'extra')))
        buttonKnight_window = canvasSide.create_window(392,892, anchor=NW, window=buttonKnight)
        Import.ExtraPiecesButtons.append(buttonKnight_window)

        buttonRook = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(Rook(Self.side,'extra')))
        buttonRook_window = canvasSide.create_window(392,784, anchor=NW, window=buttonRook)
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
    ExtraPiecesButtons = []

    # Future Updated (Nothing for now)
    def ExtraButtons():    
        buttonNormalGame = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvasSide.create_window(0,880, anchor=NW, window=buttonNormalGame)

        buttonVSComputer = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvasSide.create_window(0,880, anchor=NW, window=buttonVSComputer)

        buttonMateInN = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        buttonSG_window = canvasSide.create_window(0,880, anchor=NW, window=buttonMateInN)

    def freeModeButtons():
        buttonKing = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(King(Self.side)))
        buttonKing_window = canvasSide.create_window(392,892, anchor=NW, window=buttonKing)
        Import.ExtraPiecesButtons.append(buttonKing_window)

        buttonPawn = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(Pawn(Self.side,'extra')))
        buttonPawn_window = canvasSide.create_window(392,784, anchor=NW, window=buttonPawn)
        Import.ExtraPiecesButtons.append(buttonPawn_window)

        if Turn == 1:
            buttonKing.config(image=Import.Img_wPbS[0])
            buttonPawn.config(image=Import.Img_wPbS[6])
        else:
            buttonKing.config(image=Import.Img_bPwS[0])
            buttonPawn.config(image=Import.Img_bPwS[6])

# >>> MOVES  <<<
class GamePlay():
    # Selecting Piece       
    def verification(position,startingTime): # Ovo je kada SELEKTUJEMO FIGURU  >>> First Click <<<
        def verify(xy):
            global Self
            if isinstance(CurrentTableDict[xy],Chess):
                Self = CurrentTableDict[xy]
                Rendering.borderDefault()
                Rendering.borderColors(xy,Import.ButtonDict,Self)
        try:
            if (Turn == 1 and CurrentTableDict[position].side == 'w') or \
                (Turn == -1 and CurrentTableDict[position].side == 'b'):
                verify(position)
        except AttributeError:
            None
        verificationTime = time.time()
        Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
        endTime = time.time()
        Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,verificationTime,None) 

    # Taking Actions
    moveCounter: int
    def movingDone(newXY):
        global Self,Turn
        if CurrentTableDict[newXY] =='':
            if isinstance(Self,Pawn):
                if newXY in Self.passiv_move:
                    output,transcript = Self.Move(newXY)
                    return output,transcript,Rendering.green
                elif newXY in Self.take:
                    output,transcript = Self.enPassantTake(newXY,enPassantEnemy,CurrentTableDict,GamePlay.moveCounter)
                    return output,transcript,Rendering.red
                else:
                    return False,False,False
            elif newXY in Self.move:
                output,transcript = Self.Move(newXY)
                return output,transcript,Rendering.green
            else:
                return False,False,False
        else:
            None,None,None
           
    def takingDone(enemyXY):
        global Self,Turn
        if CurrentTableDict[enemyXY].side != Self.side:
            if enemyXY in Self.take:
                output,transcript = Self.Take(enemyXY,CurrentTableDict,GamePlay.moveCounter)
                return output,transcript,Rendering.red
            else:
                return False,False,False  
        else:
            return None,None,None

    def castlingDone(rookXY):
        global Self,Turn
        if isinstance(Self,King) and Self.castling and  rookXY in Self.castling:
            rook = CurrentTableDict[rookXY]
            output,transcript = Self.Castling(rook)
            return output,transcript,Rendering.cyan
        else:
            return None,None,None

    def pieceChange(newSelf):
        global Self
        startingTime = time.time()
        if Self.side == CurrentTableDict[newSelf].side:
            GamePlay.verification(newSelf,startingTime)

    def PawnPromotion(choice):  
        global Self,Phase
        if Phase == 'Pawn Promotion':
            startingTime = time.time()
        
            promote = choice
            promote.x,promote.y = Self.getXY()
            Chess.PromoteDict[promote]=Self
            Chess.pieces.remove(Self)

            Rendering.printPawnPromotiong(Self,promote,posInTransc,TranscriptName,canvasSide,MoveOutput,Import.ExtraPiecesButtons,ExecutionTime_window,GamePlay.moveCounter)
            
            Self = None
            Phase = 'Game Mechanic'
            GamePlay.End_Turn()

            actionTime = time.time()
            Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
            endTime = time.time()
            Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,None,actionTime)

    def Previous():
        global Self,Turn,CurrentTableDict
        startingTime = time.time()
        if Phase == 'Game Mechanic':
            CurrentTableDict = Rewind.Previous(GamePlay.moveCounter)
            Turn *=-1 ; Self =None ; GamePlay.moveCounter -=1
            GamePlay.End_Turn()
            
            actionTime = time.time()
            Rendering.printMovesDone(MoveOutput,Rendering.blue,None,posInTransc)
            Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
            endTime = time.time()
            Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,None,actionTime)  

    def Next():
        global Self,Turn,CurrentTableDict
        startingTime = time.time()
        if Phase == 'Game Mechanic':
            CurrentTableDict = Rewind.Next(GamePlay.moveCounter)
            Turn *=-1 ; Self =None ; GamePlay.moveCounter +=1
            GamePlay.End_Turn()
            
            actionTime = time.time()
            Rendering.printMovesDone(MoveOutput,Rendering.blue,None,posInTransc)
            Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
            endTime = time.time()
            Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,None,actionTime) 

    # Finishing Turn
    ActionsDone = [movingDone, takingDone, castlingDone, pieceChange]
    def action(act):
        global Phase,Self,Turn,posInTransc
        for a in range(4):
            try:
                output,transcript,color = GamePlay.ActionsDone[a](act)
            except TypeError:
                continue
            if output is None:
                continue
            elif output is False:
                Self=None ; Rendering.borderDefault() ; Rendering.borderCheck(Import.ButtonDict)
                return
            else:
                if isinstance(Self,Pawn) and (Self.x == 7 or Self.x == 0):
                    Rendering.HidingButtons(canvasSide,ExecutionTime_window)
                    Import.PawnPromotionButtons()
                    Turn,posInTransc,GamePlay.moveCounter=Rendering.printActionResult(Turn,posInTransc,TranscriptName,GamePlay.moveCounter,MoveOutput,output,transcript,color)
                    Phase = 'Pawn Promotion'
                    return
                else:
                    Self=None
                    return output,transcript,color

    def End_Turn():
        global posInTransc,CurrentTableDict,enPassantEnemy
        CurrentTableDict = Chess.currentTableDict()

        AI.ClearPossibleActions()
        for p in Chess.pieces:
            AI.AllActions(p,CurrentTableDict)
        try:
            enPassant,enPassantEnemy = Rewind.EnPassant(TranscriptName)
            side = CurrentTableDict[enPassantEnemy].side
            wk,wlr,wrr,bk,blr,brr=AI.PossibleActions(enPassant,side)
        except TypeError:
            enPassantEnemy=None
            wk,wlr,wrr,bk,blr,brr=AI.PossibleActions()
        AI.castlingCheck(wk,wlr,wrr,bk,blr,brr)
        gameover = AI.GameOverCheck(Turn)
        GameFlow.GameOver(Turn,gameover)
        
        Rendering.borderDefault()
        Rendering.borderCheck(Import.ButtonDict)
        rewindButtonsManage,posInTransc = Rewind.Get_Transcript_and_Position(TranscriptName)
        Rendering.PreviousNextButtons(canvasSide,buttonNext_window,buttonBack_window,rewindButtonsManage)
        

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
        Rendering.HidingButtons(canvasSide,ExecutionTime_window,buttonBack_window,buttonNext_window)

        Chess.pieces.clear()
        Chess.TakenDict.clear()
        AI.ClearPossibleActions()
        CurrentTableDict = Chess.currentTableDict()

        MoveOutput.delete('1.0', END)
        Rendering.borderDefault()
        posInTransc = Rewind.ResetPosition()
        Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)

    def StandardGame():
        global Phase,Turn,Self,CurrentTableDict,posInTransc
        startingTime = time.time()

        Phase = 'Game Mechanic' ; Turn=1 ; Self=None ; GamePlay.moveCounter = 0 ; posInTransc =-1
        GameFlow.StartingPosition()
        CurrentTableDict = Chess.currentTableDict()

        with open('Game.txt','w') as f:
            f.truncate(0)
        GameFlow.MouseKeyboard(None,None,None,'Remove_Win')
        
        for p in Chess.pieces:
            AI.AllActions(p,CurrentTableDict)
        AI.PossibleActions()
       
        Rendering.HidingButtons(canvasSide,buttonGM_window,buttonSG_window)
        Import.RightPanel_SecondScreen()

        verificationTime = time.time()
        Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
        endTime = time.time()
        Rendering.timeShowing(ExecutionTime,Turn,Self,startingTime,endTime,verificationTime,None)

    def GameMechanic(xy):
        global Turn,posInTransc
        startingTime = time.time()
        if Phase == 'Game Mechanic':
            if Self == None:
                GamePlay.verification(xy,startingTime) 
            else:
                try:
                    output,transcript,color=GamePlay.action(xy)
                except TypeError:
                    return
                Turn,posInTransc,GamePlay.moveCounter=Rendering.printActionResult(Turn,posInTransc,TranscriptName,GamePlay.moveCounter,MoveOutput,output,transcript,color)
                GamePlay.End_Turn()
                actionTime = time.time()
                Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
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
            Rendering.printMovesDone(MoveOutput,Rendering.gold,output,None)

    # Extra Methods
    def GodMode():
        GameFlow.StandardGame()
        GameFlow.MouseKeyboard('Change_Turn','Free_Remove','Free_Moving','Remove_Win')

    def MouseKeyboard(rClick=None,delete=None,insert=None,win=None,space=None):
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

        if space=='Statistic':
            def spacePressed(event):
                _ = os.system('cls')
                n = 1000
                ns = 1000000

                timingsAllActionsSET = []
                timingsPossibleActionsSET = []
                timingsResetActionsSET = []
                for _ in range(n):
                    start = time.time()
                    for p in Chess.pieces:
                        AI.AllActions(p,CurrentTableDict)
                    end = time.time()
                    timingsAllActionsSET.append(end-start)
                    wk,wlr,wrr,bk,blr,brr=AI.PossibleActions()
                    AI.castlingCheck(wk,wlr,wrr,bk,blr,brr)
                    end1 = time.time()
                    timingsPossibleActionsSET.append(end1-end)
                    AI.ClearPossibleActions()
                    end2 = time.time()
                    timingsResetActionsSET.append(end2-end1)

                a = sum(timingsAllActionsSET)/len(timingsAllActionsSET)
                b = sum(timingsPossibleActionsSET)/len(timingsPossibleActionsSET)
                c = sum(timingsResetActionsSET)/len(timingsResetActionsSET)

                print('++'*66) ; print('\t'*2,'TIMINGS for ANALYZING whole TABLE','\n')  
                print(f'{str('postavljanje svih attributa :').ljust(33)}{(a)*ns:,.0f} ns')
                print(f'{str('korigovanje svih attributa :').ljust(33)}{(b)*ns:,.0f} ns')
                print(f'{str('brisanje svih attributa :').ljust(33)}{(c)*ns:,.0f} ns')

                for p in Chess.pieces:
                    AI.AllActions(p,CurrentTableDict)
                wk,wlr,wrr,bk,blr,brr=AI.PossibleActions()
                AI.castlingCheck(wk,wlr,wrr,bk,blr,brr)
                
                XY = hover.text
                selfP = CurrentTableDict[XY]
                a = "" if (isinstance(selfP,King) or isinstance(selfP,Queen)) else str(':'+selfP.name)
                print('++'*66)  ; print('\t'*2,'Selected PIECE',str(selfP)[1:],a,'\n') 
                if isinstance(selfP,Chess):
                    if isinstance(selfP,King):
                            print('castling: ',selfP.castling)
                    if isinstance(selfP,Pawn):
                        print('passive move: ',selfP.passiv_move)
                        print('attack: ',selfP.attack)
                    else:
                        print('moves: ',selfP.move)
                    print('takes: ',selfP.take)
                    print('defends: ',selfP.defend)
                    print('action Counter: ',selfP.actionsCounter)
                    print('Defender: ',selfP.Defender)
                    print("check: ",Chess.Check)

                a = "WHITE" if selfP.side=='w' else "BLACK"
                print('++'*66)  ; print('\t'*2,'ALL possible ACTIONS\t',a,'\n') 
                team = Chess.AllActions_W if selfP.side=='w'else Chess.AllActions_B
                print("Number of POSSIBLE ACTIONS: ",(len(team['move'])+len(team['passive_move'])+len(team['take'])),'\n')
                print('whole team possible moves: ',team['move'])
                print('whole team passive moves: ',team['passive_move'])
                print('whole team possible takes: ',team['take'])
                print('whole team possible defends: ',team['defend'])
                print('whole team possible attacks: ',team['attack'])
                print('++'*66)
            window.bind("<space>",spacePressed)   

        if rClick == 'Change_Turn':
            def rightClick(event):
                global Turn,Self,PossibleCheck,DangerKingSolve,directAttackers,DangerTeamSolve,Defenders,CurrentTableDict
                startTime = time.time()
                Turn *=-1
                Self = None
                GamePlay.End_Turn()

                verificationTime = time.time()
                Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
                endTime = time.time()
                Rendering.timeShowing(ExecutionTime,Turn,Self,startTime,endTime,verificationTime,None)
            window.bind("<Button-3>", rightClick)

        if delete == 'Free_Remove':
            def deletePressed(event):
                global Self,CurrentTableDict              
                startTime = time.time()
                if Self is not None and not isinstance(Self,King):
                    Chess.pieces.remove(Self)
                    Self = None
                    Rendering.borderDefault()     
                    GamePlay.End_Turn()

                    verificationTime = time.time()
                    Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
                    endTime = time.time()
                    Rendering.timeShowing(ExecutionTime,Turn,Self,startTime,endTime,verificationTime,None)
            window.bind("<Delete>", deletePressed)

        if insert == 'Free_Moving':
            def insertPressed(event):
                global Self,CurrentTableDict
                startTime = time.time()  
                XY = hover.text
                if Self is not None:
                    Self.x,Self.y = XY[0],XY[1]
                    Self = None
                    GamePlay.End_Turn()

                    verificationTime = time.time()
                    Rendering.RenderingScreen(CurrentTableDict,Import.ButtonDict,Import.AllImages)
                    endTime = time.time()
                    Rendering.timeShowing(ExecutionTime,Turn,Self,startTime,endTime,verificationTime,None)
            window.bind("<Insert>", insertPressed)

        if win == 'Remove_Win':
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
                else:
                    if not space:
                        GameFlow.MouseKeyboard(space='Statistic')
            window.bind('\u0075\u0076',freeMode)
            window.bind('\u0076\u0075',freeMode)

GameFlow.MouseKeyboard()
hideShowcase_executed = False
Import.ShowcaseScreen()

window.mainloop()