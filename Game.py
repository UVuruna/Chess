from tkinter import *
from PIL import ImageTk, Image
import time
from ChessParent import Chess
from Pieces import *
from AI import AI
from Transcript import Rewind
from Rendering import Rendering
from ImagesDecorators import *
import os

window = Tk()
window.title("Chess")
window.resizable(False,False)
X=1550 ; Y=1000
window.geometry(f"{X}x{Y}")
Import.ImageImport()


class MainPanel():
    ButtonDict      = None
    hover           = None
    canvasTable     = None
    canvasSide      = None
    Showcase        = None
    ShowcaseImage   = None
    ShowcaseHidden  = False
    
    def Hover(event,button):    # Green                          # Red                             # Light Blue                      # Yellow  
        MainPanel.hover = event.widget
        if button.cget('bg') !=Rendering.green and button.cget('bg') !=Rendering.red and button.cget('bg') !=Rendering.cyan and button.cget('bg') !=Rendering.yellow:
            button.config(background='silver')
        elif button.cget('bg') ==Rendering.green:
            button.config(background=Rendering.dark_green)
        elif button.cget('bg') ==Rendering.red:
            button.config(background=Rendering.dark_red)
        elif button.cget('bg') ==Rendering.cyan:
            button.config(background=Rendering.dark_cyan)
        elif button.cget('bg') ==Rendering.yellow:
            button.config(background=Rendering.dark_yellow)

    def ClearHover(event,button):
        if button.cget('bg') == 'silver':
            button.config(background='SystemButtonFace')
        elif button.cget('bg') ==Rendering.dark_green:
            button.config(background=Rendering.green)
        elif button.cget('bg') ==Rendering.dark_red:
            button.config(background=Rendering.red)
        elif button.cget('bg') ==Rendering.dark_cyan:
            button.config(background=Rendering.cyan)
        elif button.cget('bg') ==Rendering.dark_yellow:
            button.config(background=Rendering.yellow)
    # Icon   
    window.iconbitmap(os.path.join(Import.ImagesLocation,"ico.ico"))   

    def MainPanel_Parts(images):
        # Canvas 1
        MainPanel.canvasTable = Canvas(window, width=1000, height=1000)
        MainPanel.canvasTable.place(anchor=NW,x=0,y=0)
        MainPanel.canvasTable.create_image(0,0, anchor=NW, image=images[0])
        # Canvas 2
        MainPanel.canvasSide = Canvas(window, width=550, height=1000)
        MainPanel.canvasSide.place(anchor=NW,x=1000,y=0)
        MainPanel.canvasSide.create_image(0,0, anchor=NW, image=images[3])

            # Square buttons
        border_Dist = 97 ; butt_Dimension = 101.7
        ButtonReferences = list(Chess.emptyTableDict().keys())
        ButtonDict = {}
        for i in range(64): 
            n=8             # Ovaj deo je da se napravi matrica (8*8) od liste 
            x = i//n        # zbog postavke BUTTONA na CANVAS (pozicije XY)
            y = i-x*n       # Radi izracunavanja koordinata preko FORMULE
                                        
            button = Button(window)               # kreiranje Buttona
            button.text = ButtonReferences[i]     # ubacivanje Atributa koji opisuje poziciju. Improvizovana ButtonID
            button.config(border=2,command=lambda text = button.text: (GameFlow.GameMechanic(text)))                       # FUNKCIJA Buttona
            button.bind("<Enter>",lambda event, text = button: MainPanel.Hover(event,text))                                # Set Hover
            button.bind("<Leave>",lambda event, text = button: MainPanel.ClearHover(event,text))                           # Clear Hover
            button_window = MainPanel.canvasTable.create_window(1,1, anchor=NW, window=button)                             # kreiranje prozora buttona
            MainPanel.canvasTable.coords(button_window,(border_Dist+y*butt_Dimension),(border_Dist+(7-x)*butt_Dimension))  # postavljanje buttona na EKRAN
            ButtonDict[button.text] = button     # Ubacivanje Buttona u RECNIK                            

                # Default Square Color
            button.config(image=images[2]) if (x%2==0 and y%2==0) or (x%2==1 and y%2==1) else button.config(image=images[1])
            button.color =             'b' if (x%2==0 and y%2==0) or (x%2==1 and y%2==1) else 'w'
        return ButtonDict

    def ShowcaseScreen():
        GameFlow.Phase = "Start"
        MainPanel.ShowcaseImage = ImageTk.PhotoImage(Image.open(os.path.join(Import.ImagesLocation,"ChessGame.png")))
        MainPanel.Showcase = Label(window, image=MainPanel.ShowcaseImage)
        MainPanel.Showcase.place(anchor=NW,x=0,y=0)
        window.after(13000, MainPanel.hideShowcase)     

    def hideShowcase():
        if not MainPanel.ShowcaseHidden:
            MainPanel.Showcase.place_forget()
            MainPanel.ButtonDict = MainPanel.MainPanel_Parts(Import.AllImages[0])
            SidePanel.Screen_1()
            MainPanel.ShowcaseHidden =True

class SidePanel():
    FirstOpponent       =None
    SecondOpponent      =None
    MoveOutput          =None
    ExecutionTime       =None
    ExecutionTime_win   =None
    but_SG_win          =None
    but_GM_win          =None
    but_Back_win        =None
    but_Next_win        =None

    def SideCanvas_Parts(ObjType, bordeR, x,y, w=None,h=None, txt=None, fontStyle=None, method=None,args=None):
        if ObjType ==Button:
            button = ObjType(window, border=bordeR, font=fontStyle, width=w, height=h, text=txt, command=lambda: method(args) if args else method())
            button_window = MainPanel.canvasSide.create_window(x,y, anchor=NW, window=button)
            return button_window,button

    Screen_1_Frames = []
    @Decorator.ListAppend(Screen_1_Frames)
    def Screen_1():
        SidePanel.FirstOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        text_FirstOpponent_win = MainPanel.canvasSide.create_window(280,900, anchor=NW, window=SidePanel.FirstOpponent)
        SidePanel.FirstOpponent.insert(1.0, "1stPlayer")

        SidePanel.SecondOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        text_SecondOpponent_win = MainPanel.canvasSide.create_window(280,945, anchor=NW, window=SidePanel.SecondOpponent)
        SidePanel.SecondOpponent.insert(1.0, "2ndPlayer")

        but_SaveTransc_win =SidePanel.SideCanvas_Parts(Button, 5, 300,780,  16,3, 'Saving Game\nTranscript',('Tahoma', 18), SidePanel.SavedGames,'players')[0]
        but_GameTransc_win =SidePanel.SideCanvas_Parts(Button, 5,  10,780,  12,4, 'Casual Game\nNo Transcript',('Tahoma', 27), SidePanel.SavedGames)[0]

        return text_FirstOpponent_win,text_SecondOpponent_win,but_SaveTransc_win,but_GameTransc_win

    def Screen_2():
        SidePanel.MoveOutput = Text(window, width= 550, height=22, bg= '#535a5e', font=('Tahoma', 22))
        SidePanel.MoveOutput.place(anchor=NW,x=1000,y=2)

        exTiText = 'Standard Game:\nNormal Chess game\nwith all rules applied\n\nGod Mode:\nDelete: Remove Piece\nInsert: Freely move Piece\nRightClick: Change GamePlay.Turn '
        SidePanel.ExecutionTime = Label(window, font=('Eras Demi ITC', 16), width=24, height=8, bd=2, relief='groove', text=exTiText)
        SidePanel.ExecutionTime_win = MainPanel.canvasSide.create_window(220, 787, anchor=NW, window=SidePanel.ExecutionTime)

        SidePanel.but_SG_win =SidePanel.SideCanvas_Parts(Button, 3, 10,780,  9,2, 'Standard\nGame',('Eras Demi ITC', 24), GameFlow.StandardGame)[0]
        SidePanel.but_GM_win =SidePanel.SideCanvas_Parts(Button, 3, 10,890,  9,2, 'God Mode',('Eras Demi ITC', 24), GameFlow.GodMode)[0]
    
    def Screen_Game():
        SidePanel.SideCanvas_Parts(Button, 3,  10,780,  9,2, 'New Game',('Eras Demi ITC', 24), GameFlow.NewGame)[0]
        SidePanel.but_Back_win =SidePanel.SideCanvas_Parts(Button, 3,  10,900,  3,1, '⯬🢠',('Eras Demi ITC', 33), GamePlay.Previous)[0]
        SidePanel.but_Next_win =SidePanel.SideCanvas_Parts(Button, 3, 108,900,  3,1, '🢡⯮',('Eras Demi ITC', 33), GamePlay.Next)[0]

        Rendering.HidingButtons(MainPanel.canvasSide,SidePanel.but_Back_win,SidePanel.but_Next_win)

    def SavedGames(option=None):
        Player1,Player2 = None,None
        if option is not None:
            Player1 = SidePanel.FirstOpponent.get("1.0", "end-1c")
            Player2 = SidePanel.SecondOpponent.get("1.0", "end-1c")
            Import.TranscriptName = f"{Player1}vs{Player2}"
        else:
            Import.TranscriptName = 'Game'

        Rendering.HidingButtons(MainPanel.canvasSide,*SidePanel.Screen_1_Frames)
        try:
            with open(f'{Import.TranscriptName}.txt','x') as f:
                pass
        except FileExistsError:
            pass
        SidePanel.Screen_2()

    ExtraPiecesButtons = []
    @Decorator.ListAppend(ExtraPiecesButtons)
    def PawnPromotionButtons():
        SidePanel.ExtraPiecesButtons.clear()
        but_Q_win,but_Q =SidePanel.SideCanvas_Parts(Button, 5, 254,784, method =GamePlay.PawnPromotion, args=Queen(GamePlay.Self.side,'extra'))
        but_B_win,but_B =SidePanel.SideCanvas_Parts(Button, 5, 254,892, method =GamePlay.PawnPromotion, args=Bishop(GamePlay.Self.side,'extra'))
        but_K_win,but_K =SidePanel.SideCanvas_Parts(Button, 5, 392,892, method =GamePlay.PawnPromotion, args=Knight(GamePlay.Self.side,'extra'))
        but_R_win,but_R =SidePanel.SideCanvas_Parts(Button, 5, 392,784, method =GamePlay.PawnPromotion, args=Rook(GamePlay.Self.side,'extra'))

        if GamePlay.Turn == 1:
            but_Q.config(image=Import.AllImages[2][1] if GamePlay.Turn==1 else Import.AllImages[3][1])
            but_B.config(image=Import.AllImages[2][2] if GamePlay.Turn==1 else Import.AllImages[3][2])
            but_K.config(image=Import.AllImages[2][3] if GamePlay.Turn==1 else Import.AllImages[3][3])
            but_R.config(image=Import.AllImages[2][5] if GamePlay.Turn==1 else Import.AllImages[3][5])
        return but_Q_win,but_B_win,but_K_win,but_R_win
    
    # Future Updated (Nothing for now)
    def ExtraButtons():    
        buttonNormalGame = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        SidePanel.but_SG_win = MainPanel.canvasSide.create_window(0,880, anchor=NW, window=buttonNormalGame)

        buttonVSComputer = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        SidePanel.but_SG_win = MainPanel.canvasSide.create_window(0,880, anchor=NW, window=buttonVSComputer)

        buttonMateInN = Button(window, border=5, font=('Arial', 27), width=13, height=2, text='New\nGame', command=lambda: GameFlow.StandardGame())
        SidePanel.but_SG_win = MainPanel.canvasSide.create_window(0,880, anchor=NW, window=buttonMateInN)

    def freeModeButtons():
        buttonKing = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(King(GamePlay.Self.side)))
        buttonKing_window = MainPanel.canvasSide.create_window(392,892, anchor=NW, window=buttonKing)
        SidePanel.ExtraPiecesButtons.append(buttonKing_window)

        buttonPawn = Button(window, border=5, command=lambda: GamePlay.PawnPromotion(Pawn(GamePlay.Self.side,'extra')))
        buttonPawn_window = MainPanel.canvasSide.create_window(392,784, anchor=NW, window=buttonPawn)
        SidePanel.ExtraPiecesButtons.append(buttonPawn_window)

        if GamePlay.Turn == 1:
            buttonKing.config(image=Import.AllImages[2][0])
            buttonPawn.config(image=Import.AllImages[2][6])
        else:
            buttonKing.config(image=Import.AllImages[3][0])
            buttonPawn.config(image=Import.AllImages[3][6])

# >>> MOVES  <<<
class GamePlay():
    Self            =None
    Turn            =None
    EnPassantPawn   =None

    def verification(position,startingTime): # Ovo je kada SELEKTUJEMO FIGURU  >>> First Click <<<
        def verify(xy):
            if isinstance(GameFlow.TablePosition[xy],Chess):
                GamePlay.Self = GameFlow.TablePosition[xy]
                Rendering.borderDefault()
                Rendering.borderColors(xy,MainPanel.ButtonDict,GamePlay.Self)
        try:
            if (GamePlay.Turn == 1 and GameFlow.TablePosition[position].side == 'w') or \
                (GamePlay.Turn == -1 and GameFlow.TablePosition[position].side == 'b'):
                verify(position)
        except AttributeError:
            None
        verificationTime = time.time()
        Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
        endTime = time.time()
        Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                              GamePlay.Self,startingTime,endTime,verificationTime,None) 

    # Taking Actions
    moveCounter: int
    def movingDone(newXY):
        if GameFlow.TablePosition[newXY] =='':
            if isinstance(GamePlay.Self,Pawn):
                if newXY in GamePlay.Self.passiv_move:
                    output,transcript = GamePlay.Self.Move(newXY)
                    return output,transcript,Rendering.green
                elif newXY in GamePlay.Self.take:
                    output,transcript = GamePlay.Self.enPassantTake(newXY,GamePlay.EnPassantPawn,GameFlow.TablePosition,GamePlay.moveCounter)
                    return output,transcript,Rendering.red
                else:
                    return False,False,False
            elif newXY in GamePlay.Self.move:
                output,transcript = GamePlay.Self.Move(newXY)
                return output,transcript,Rendering.green
            else:
                return False,False,False
        else:
            None,None,None
           
    def takingDone(enemyXY):
        if GameFlow.TablePosition[enemyXY].side != GamePlay.Self.side:
            if enemyXY in GamePlay.Self.take:
                output,transcript = GamePlay.Self.Take(enemyXY,GameFlow.TablePosition,GamePlay.moveCounter)
                return output,transcript,Rendering.red
            else:
                return False,False,False  
        else:
            return None,None,None

    def castlingDone(rookXY):
        if isinstance(GamePlay.Self,King) and GamePlay.Self.castling and  rookXY in GamePlay.Self.castling:
            rook = GameFlow.TablePosition[rookXY]
            output,transcript = GamePlay.Self.Castling(rook)
            return output,transcript,Rendering.cyan
        else:
            return None,None,None

    def pieceChange(newSelf):
        startingTime = time.time()
        if GamePlay.Self.side == GameFlow.TablePosition[newSelf].side:
            GamePlay.verification(newSelf,startingTime)

    def PawnPromotion(choice):  
        if GameFlow.Phase == 'Pawn Promotion':
            startingTime = time.time()
        
            promote = choice
            promote.x,promote.y = GamePlay.Self.getXY()
            Chess.PromoteDict[promote]=GamePlay.Self
            Chess.pieces.remove(GamePlay.Self)

            Rendering.printPawnPromotiong(GamePlay.Self,promote,Rewind.PosInTransc,Import.TranscriptName,
                                          MainPanel.canvasSide,SidePanel.MoveOutput,SidePanel.ExtraPiecesButtons,
                                          SidePanel.ExecutionTime_win,GamePlay.moveCounter)
            
            GamePlay.Self = None
            GameFlow.Phase = 'Game Mechanic'
            GamePlay.End_Turn()

            actionTime = time.time()
            Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
            endTime = time.time()
            Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                  GamePlay.Self,startingTime,endTime,None,actionTime)

    def Previous():
        startingTime = time.time()
        if GameFlow.Phase == 'Game Mechanic':
            GameFlow.TablePosition = Rewind.Previous(GamePlay.moveCounter)
            GamePlay.Turn *=-1 ; GamePlay.Self =None ; GamePlay.moveCounter -=1
            GamePlay.End_Turn()
            
            actionTime = time.time()
            Rendering.printMovesDone(SidePanel.MoveOutput,Rendering.blue,None,Rewind.PosInTransc)
            Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
            endTime = time.time()
            Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                  GamePlay.Self,startingTime,endTime,None,actionTime)  

    def Next():
        startingTime = time.time()
        if GameFlow.Phase == 'Game Mechanic':
            GameFlow.TablePosition = Rewind.Next(GamePlay.moveCounter)
            GamePlay.Turn *=-1 ; GamePlay.Self =None ; GamePlay.moveCounter +=1
            GamePlay.End_Turn()
            
            actionTime = time.time()
            Rendering.printMovesDone(SidePanel.MoveOutput,Rendering.blue,None,Rewind.PosInTransc)
            Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
            endTime = time.time()
            Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                  GamePlay.Self,startingTime,endTime,None,actionTime) 

    # Finishing GamePlay.Turn
    ActionsDone = [movingDone, takingDone, castlingDone, pieceChange]
    def action(act):
        for a in range(4):
            try:
                output,transcript,color = GamePlay.ActionsDone[a](act)
            except TypeError:
                continue
            if output is None:
                continue
            elif output is False:
                GamePlay.Self=None ; Rendering.borderDefault() ; Rendering.borderCheck(MainPanel.ButtonDict)
                return
            else:
                if isinstance(GamePlay.Self,Pawn) and (GamePlay.Self.x ==8 or GamePlay.Self.x ==1):
                    Rendering.HidingButtons(MainPanel.canvasSide,SidePanel.ExecutionTime_win)
                    SidePanel.PawnPromotionButtons()
                    GamePlay.Turn,Rewind.PosInTransc,GamePlay.moveCounter =Rendering.printActionResult(GamePlay.Turn,Rewind.PosInTransc,Import.TranscriptName,
                                                                                                GamePlay.moveCounter,SidePanel.MoveOutput,output,transcript,color)
                    GameFlow.Phase = 'Pawn Promotion'
                    return
                else:
                    GamePlay.Self=None
                    return output,transcript,color

    def End_Turn():
        GameFlow.TablePosition = Chess.currentTableDict()

        AI.ClearPossibleActions()
        for p in Chess.pieces:
            AI.AllActions(p,GameFlow.TablePosition)
        try:
            enPassant,GamePlay.EnPassantPawn = Rewind.EnPassant(Import.TranscriptName)
            side = GameFlow.TablePosition[GamePlay.EnPassantPawn].side
            wk,wlr,wrr,bk,blr,brr=AI.PossibleActions(enPassant,side)
        except TypeError:
            GamePlay.EnPassantPawn=None
            wk,wlr,wrr,bk,blr,brr=AI.PossibleActions()
        AI.castlingCheck(wk,wlr,wrr,bk,blr,brr)
        gameover = AI.GameOverCheck(GamePlay.Turn)
        GameFlow.GameOver(GamePlay.Turn,gameover)
        
        Rendering.borderDefault()
        Rendering.borderCheck(MainPanel.ButtonDict)
        Rewind.UpdateTranscript(Import.TranscriptName)
        Rendering.PreviousNextButtons(MainPanel.canvasSide,SidePanel.but_Next_win,SidePanel.but_Back_win)
        
# >>> GAME <<<
class GameFlow:
    Phase           =None
    TablePosition   =None

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
        SidePanel.Screen_1()
        Rendering.HidingButtons(MainPanel.canvasSide,SidePanel.ExecutionTime_win,SidePanel.but_Back_win,SidePanel.but_Next_win)

        Chess.pieces.clear()
        Chess.TakenDict.clear()
        AI.ClearPossibleActions()
        GameFlow.TablePosition = Chess.currentTableDict()

        SidePanel.MoveOutput.delete('1.0', END)
        Rendering.borderDefault()
        Rewind.PosInTransc = Rewind.ResetPosition()
        Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)

    def StandardGame():
        startingTime = time.time()

        GameFlow.Phase = 'Game Mechanic' ; GamePlay.Turn=1 ; GamePlay.Self=None ; GamePlay.moveCounter = 0 ; Rewind.PosInTransc =-1
        GameFlow.StartingPosition()
        GameFlow.TablePosition = Chess.currentTableDict()

        with open('Game.txt','w') as f:
            f.truncate(0)
        
        for p in Chess.pieces:
            AI.AllActions(p,GameFlow.TablePosition)
        AI.PossibleActions()
       
        Rendering.HidingButtons(MainPanel.canvasSide,SidePanel.but_GM_win,SidePanel.but_SG_win)
        SidePanel.Screen_Game()

        verificationTime = time.time()
        Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
        endTime = time.time()
        Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                              GamePlay.Self,startingTime,endTime,verificationTime,None)

    def GameMechanic(xy):
        startingTime = time.time()
        if GameFlow.Phase == 'Game Mechanic':
            if GamePlay.Self == None:
                GamePlay.verification(xy,startingTime) 
            else:
                try:
                    output,transcript,color=GamePlay.action(xy)
                except TypeError:
                    return
                GamePlay.Turn,Rewind.PosInTransc,GamePlay.moveCounter=Rendering.printActionResult(GamePlay.Turn,Rewind.PosInTransc,Import.TranscriptName,
                                                                                            GamePlay.moveCounter,SidePanel.MoveOutput,output,transcript,color)
                GamePlay.End_Turn()
                actionTime = time.time()
                Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
                endTime = time.time()
                Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                      GamePlay.Self,startingTime,endTime,None,actionTime)  

    def GameOver(turn,GameOver=None):
        if GameOver is not None:
            if GameOver == 'CheckMate':
                winner = "\tWhite WON!!!" if turn == -1 else "\tBlack WON!!!"
            elif GameOver == 'StaleMate':
                winner = ''
            with open(f'{Import.TranscriptName}.txt','a') as f:
                f.write(GameOver)
            GameFlow.Phase = 'Game Over'
            output = str(GameOver+winner)
            Rendering.printMovesDone(SidePanel.MoveOutput,Rendering.gold,output,None)

    # Extra Methods
    def GodMode():
        GameFlow.StandardGame()
        MouseKeyboard.RightClick='Change_Turn'
        MouseKeyboard.Delete='Free_Remove'
        MouseKeyboard.Insert='Free_Moving'

class MouseKeyboard():
    RightClick  =None
    Delete      =None
    Insert      =None
    UV          =None
    Space       =None

    @classmethod
    def __init__(cls):
        window.bind('\u0075\u0076'  ,MouseKeyboard.UVStatistic)
        window.bind('\u0076\u0075'  ,MouseKeyboard.UVStatistic)
        window.bind("<Escape>"      ,MouseKeyboard.escPressed)
        window.bind("<Button-3>"    ,MouseKeyboard.rightClick)
        window.bind("<Delete>"      ,MouseKeyboard.deletePressed)
        window.bind("<Insert>"      ,MouseKeyboard.insertPressed)
        window.bind("<space>"       ,MouseKeyboard.spacePressed)

    def UVStatistic(event):
        if GameFlow.Phase == 'Game Over':
            with open(f'{Import.TranscriptName}.txt','r+') as f:
                text = f.readlines()
                f.truncate(0)
            with open(f'{Import.TranscriptName}.txt','w') as f:
                f.writelines(text[:-1])
            Rendering.delMovesDone(SidePanel.MoveOutput,-2)
            GameFlow.Phase = 'Game Mechanic'
            Rewind.UpdateTranscript(Import.TranscriptName)
        else:
            if not MouseKeyboard.Space:
                MouseKeyboard.Space='Statistic'

    def escPressed(event):
        if GameFlow.Phase == "Start":
            MainPanel.hideShowcase()
        elif GameFlow.Phase == "Game Mechanic":
            startTime = time.time()
            GamePlay.Self = None
            Rendering.borderDefault()
            verificationTime = time.time()
            endTime = time.time()
            Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                    GamePlay.Self,startTime,endTime,verificationTime,None)

    def spacePressed(event):
        if MouseKeyboard.Space=='Statistic':
            _ = os.system('cls')
            n = 1000
            ns = 1000000

            timingsAllActionsSET = []
            timingsPossibleActionsSET = []
            timingsResetActionsSET = []
            for _ in range(n):
                start = time.time()
                for p in Chess.pieces:
                    AI.AllActions(p,GameFlow.TablePosition)
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
                AI.AllActions(p,GameFlow.TablePosition)
            wk,wlr,wrr,bk,blr,brr=AI.PossibleActions()
            AI.castlingCheck(wk,wlr,wrr,bk,blr,brr)
            
            XY = MainPanel.hover.text
            selfP = GameFlow.TablePosition[XY]
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

    def rightClick(event):
        if MouseKeyboard.RightClick == 'Change_Turn':
            startTime = time.time()
            GamePlay.Turn *=-1
            GamePlay.Self = None
            GamePlay.End_Turn()

            verificationTime = time.time()
            Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
            endTime = time.time()
            Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                    GamePlay.Self,startTime,endTime,verificationTime,None)
    
    def deletePressed(event):
        if MouseKeyboard.Delete == 'Free_Remove':         
            startTime = time.time()
            if GamePlay.Self is not None and not isinstance(GamePlay.Self,King):
                Chess.pieces.remove(GamePlay.Self)
                GamePlay.Self = None
                Rendering.borderDefault()     
                GamePlay.End_Turn()

                verificationTime = time.time()
                Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
                endTime = time.time()
                Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                        GamePlay.Self,startTime,endTime,verificationTime,None)
        
    def insertPressed(event):
        if MouseKeyboard.Insert == 'Free_Moving':
            startTime = time.time()  
            XY = MainPanel.hover.text
            if GamePlay.Self is not None:
                GamePlay.Self.x,GamePlay.Self.y = XY[0],XY[1]
                GamePlay.Self = None
                GamePlay.End_Turn()

                verificationTime = time.time()
                Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
                endTime = time.time()
                Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                        GamePlay.Self,startTime,endTime,verificationTime,None)

Import.InitializeSigns()        
MouseKeyboard()
MainPanel.ShowcaseScreen()

window.mainloop()