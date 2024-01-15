from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
from ChessParent import Chess
from Pieces import *
from AI import AI
from Transcript import Rewind
from Rendering import Rendering
from ImagesDecorators import Import,Decorator
import os
from Frames import *

window = Tk()
window.title("Chess")
window.resizable(False,False)
X=1550 ; Y=1000
window.geometry(f"{X}x{Y}")

Import.ImageImport()

# Icon   
window.iconbitmap(os.path.join(Import.ImagesLocation,"ico.ico")) 

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
        startingTime = time.time()
        if choice =='Q':
            promote = Queen(GamePlay.Self.side,'extra')
        elif choice =='B':
            promote = Bishop(GamePlay.Self.side,'extra')
        elif choice =='K':
            promote = Knight(GamePlay.Self.side,'extra')
        elif choice =='R':
            promote = Rook(GamePlay.Self.side,'extra')

        promote.x,promote.y = GamePlay.Self.getXY()
        Chess.PromoteDict[promote]=GamePlay.Self
        Chess.pieces.remove(GamePlay.Self)

        Rendering.ToggleVisibility(MainPanel.canvasSide,None,*SidePanel.ExtraPiecesButtons,SidePanel.Screen_2_Frames[1])
        Rendering.printPawnPromoting(GamePlay.Self,promote,Rewind.PosInTransc,
                                        Import.TranscriptName,SidePanel.MoveOutput,GamePlay.moveCounter)
        
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
                    SidePanel.PawnPromotionButtons(window,GamePlay.PawnPromotion,GamePlay.Turn)
                    Rendering.ToggleVisibility(MainPanel.canvasSide,None,*SidePanel.ExtraPiecesButtons,SidePanel.Screen_2_Frames[1])
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
        Rendering.PreviousNextButtons(MainPanel.canvasSide,SidePanel.Screen_Game_Frames[1:])
        
# >>> GAME <<<
class GameFlow:
    Phase           =None
    TablePosition   =None

    def SavedGames(option=None):
        Player1,Player2 = None,None
        if option is not None:
            Player1 = SidePanel.FirstOpponent.get("1.0", "end-1c")
            Player2 = SidePanel.SecondOpponent.get("1.0", "end-1c")
            Import.TranscriptName = f"{Player1}vs{Player2}"
        else:
            Import.TranscriptName = 'Game'
        Rendering.ToggleVisibility(MainPanel.canvasSide,None,*SidePanel.Screen_1_Frames,*SidePanel.Screen_2_Frames[1:])
        if not MainPanel.ButtonDict:
            MainPanel.ButtonDict = MainPanel.TableButtons(window,Import.AllImages[0],GameFlow.GameMechanic)
        try:
            with open(f'{Import.TranscriptName}.txt','x') as f:
                pass
        except FileExistsError:
            pass

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
        result = messagebox.askyesno("New Game", "Are you sure you want to quit Current Game?")
        if result:
            Rendering.ToggleVisibility(MainPanel.canvasSide,'hidden',*SidePanel.Screen_Game_Frames)
            Rendering.ToggleVisibility(MainPanel.canvasSide,None,*SidePanel.Screen_1_Frames,*SidePanel.Screen_2_Frames[:2])

            Chess.pieces.clear()
            Chess.TakenDict.clear()
            AI.ClearPossibleActions()
            GameFlow.TablePosition = Chess.currentTableDict()

            SidePanel.MoveOutput.delete('1.0', END)
            Rendering.borderDefault()
            Rewind.PosInTransc = Rewind.ResetPosition()
            Rendering.RenderingScreen(GameFlow.TablePosition,MainPanel.ButtonDict,Import.AllImages)
        else:
            None

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

        verificationTime = time.time()
        Rendering.ToggleVisibility(MainPanel.canvasSide,None,*SidePanel.Screen_2_Frames[2:],SidePanel.Screen_2_Frames[0],SidePanel.Screen_Game_Frames[0])
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
        window.bind("<Button-1>"    ,MouseKeyboard.leftClick)
        window.bind("<Delete>"      ,MouseKeyboard.deletePressed)
        window.bind("<Insert>"      ,MouseKeyboard.insertPressed)
        window.bind("<space>"       ,MouseKeyboard.spacePressed)

    def leftClick(event):
        if MouseKeyboard.Space=='Statistic' and SidePanel.StatisticFrame:
            current_state = MainPanel.canvasSide.itemcget(SidePanel.StatisticFrame_win, 'state')
            if current_state != 'hidden':
                Rendering.ToggleVisibility(MainPanel.canvasSide,'hidden',SidePanel.StatisticFrame_win)
                Rendering.ToggleVisibility(MainPanel.canvasSide,'normal',SidePanel.Screen_2_Frames[0])

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
        if not MainPanel.ShowcaseHidden:
            MainPanel.hideShowcase()
        if GameFlow.Phase == "Game Mechanic":
            startTime = time.time()
            GamePlay.Self = None
            Rendering.borderDefault()
            verificationTime = time.time()
            endTime = time.time()
            Rendering.timeShowing(SidePanel.ExecutionTime,GamePlay.Turn,
                                    GamePlay.Self,startTime,endTime,verificationTime,None)

    def spacePressed(event):
        def xy_to_TableNotation(*args):
            ChangedXY=[]
            for A in args:
                fixedA=[]
                if A:
                    for xy in A:
                        try:
                            fixedA.append(Chess.NotationTableDict[xy])
                        except KeyError:
                            fixedA.append(xy)
                ChangedXY.append(', '.join(fixedA))
            return ChangedXY
        
        def StatisticCalculate():
            n = 1000
            ns = 1000000
            timingsResetActionsSET = []
            timingsAllActionsSET = []
            timingsPossibleActionsSET = []
            
            for _ in range(n):
                start = time.time()
                AI.ClearPossibleActions()
                end = time.time()
                
                for p in Chess.pieces:
                    AI.AllActions(p,GameFlow.TablePosition)
                end1 = time.time()
                
                wk,wlr,wrr,bk,blr,brr=AI.PossibleActions()
                AI.castlingCheck(wk,wlr,wrr,bk,blr,brr)
                end2 = time.time()

                timingsResetActionsSET.append(end-start)
                timingsAllActionsSET.append(end1-end)
                timingsPossibleActionsSET.append(end2-end1)
            a = sum(timingsResetActionsSET)/len(timingsResetActionsSET)
            b = sum(timingsAllActionsSET)/len(timingsAllActionsSET)
            c = sum(timingsPossibleActionsSET)/len(timingsPossibleActionsSET)

            L11="\tTIMINGS for ANALYZING whole TABLE\n\n"
            L12=f'{str('  brisanje svih attributa :').ljust(33)}{(a)*ns:,.0f} ns\n'
            L13=f'{str('  postavljanje svih attributa :').ljust(33)}{(b)*ns:,.0f} ns\n'
            L14=f'{str('  korigovanje svih attributa :').ljust(33)}{(c)*ns:,.0f} ns\n\n'
            
            XY = MainPanel.hover.text
            selfP = GameFlow.TablePosition[XY]
            if isinstance(selfP,Chess):
                NAME = "" if (isinstance(selfP,King) or isinstance(selfP,Queen)) else str(':'+selfP.name)
                if isinstance(selfP,King):
                    FixedPositions = xy_to_TableNotation(selfP.move        ,selfP.take, selfP.defend, selfP.castling)
                elif isinstance(selfP,Pawn):
                    FixedPositions = xy_to_TableNotation(selfP.passiv_move ,selfP.take, selfP.defend, selfP.attack)
                elif isinstance(selfP,Chess):
                    FixedPositions = xy_to_TableNotation(selfP.move        ,selfP.take, selfP.defend)

            L21=f"\tSelected PIECE {selfP} {NAME}\n\n" if isinstance(selfP,Chess) else ""
            L22=f"  Moves: {FixedPositions[0]}\n" if (isinstance(selfP,Chess) and not isinstance(selfP,Pawn)) else ""
            L23=f"  Castling: {FixedPositions[3]}\n" if isinstance(selfP,King) else ""
            L24=f"  Passive Move: {FixedPositions[0]}\n" if isinstance(selfP,Pawn) else ""
            L25=f"  Attack: {FixedPositions[3]}\n" if isinstance(selfP,Pawn) else ""
            L26=f"  Takes: {FixedPositions[1]}\n" if isinstance(selfP,Chess) else ""
            L27=f"  Defends: {FixedPositions[2]}\n" if isinstance(selfP,Chess) else ""
            L28=f"  Action Counter: {selfP.actionsCounter}\n" if isinstance(selfP,Chess) else ""
            L29=f"  Defender: {selfP.Defender}\n\n" if (isinstance(selfP,Chess) and selfP.Defender) else "\n"

            try:
                SIDE = "WHITE" if selfP.side=='w' else "BLACK"
                team = Chess.AllActions_W if selfP.side=='w'else Chess.AllActions_B
            except AttributeError:
                SIDE = "WHITE" if GamePlay.Turn==1 else "BLACK"
                team = Chess.AllActions_W if GamePlay.Turn==1 else Chess.AllActions_B
            

            M=team['move'] ; PM=team['passive_move'] ; T=team['take'] ; A=team['attack'] ; D=team['defend']
            TeamFixedPositions = xy_to_TableNotation(M,PM,T,A,D,*Chess.Check)

            L30=f"\tALL possible ACTIONS {SIDE}\n\n"
            L31=f"  Check: {TeamFixedPositions[5:]}\n" if Chess.Check else ""
            L32=f"  Number of POSSIBLE ACTIONS: {(len(team['move'])+len(team['passive_move'])+len(team['take']))}\n\n"
            L33=f"  Team possible Moves: {TeamFixedPositions[0]}\n"
            L35=f"  Team passive Moves: {TeamFixedPositions[1]}\n"
            L34=f"  Team possible Takes: {TeamFixedPositions[2]}\n\n"
            L36=f"  Team possible Attacks: {TeamFixedPositions[3]}\n\n"
            L37=f"  Team possible Defends: {TeamFixedPositions[4]}\n"

            StatisticTextList = [ L11, L12, L13, L14,
                            L21, L22, L23, L24, L25, L26, L27, L28, L29,
                            L30, L31, L32, L33, L34, L35, L36, L37]
            StatisticText = str()
            for l in StatisticTextList:
                StatisticText+=l
            return StatisticText
        
        if MouseKeyboard.Space=='Statistic':
            if not SidePanel.StatisticFrame:
                StatisticText=StatisticCalculate()
                SidePanel.Statistic(window,StatisticText)
                Rendering.ToggleVisibility(MainPanel.canvasSide,None,SidePanel.Screen_2_Frames[0])
            else:
                current_state = MainPanel.canvasSide.itemcget(SidePanel.StatisticFrame_win, 'state')
                if current_state == 'hidden':
                    StatisticText=StatisticCalculate()
                    SidePanel.StatisticFrame.config(text=StatisticText)
                Rendering.ToggleVisibility(MainPanel.canvasSide,None,SidePanel.StatisticFrame_win,SidePanel.Screen_2_Frames[0])

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


MainPanel.CanvasCreate(window,Import.AllImages[0])
MainPanel.ShowcaseScreen(window)
SidePanel.Screen_1(window,GameFlow.SavedGames)
SidePanel.Screen_2(window,GameFlow.StandardGame,GameFlow.GodMode)
SidePanel.Screen_Game(window,GameFlow.NewGame,GamePlay.Previous,GamePlay.Next)
Import.InitializeSigns()        
MouseKeyboard()

window.mainloop()