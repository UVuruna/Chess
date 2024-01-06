from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from rook import Rook
from AI import AI
from tkinter import *


class Rendering():

    # Images Rendering   
    def RenderingScreen(tableDict,buttonDict,wPwS,wPbS,bPwS,bPbS,Images):
        for k,v in tableDict.items():
            if v != '': 
                if isinstance(tableDict[k],King): # King
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=wPwS[0]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=wPbS[0])
                    else:
                        buttonDict[k].config(image=bPwS[0]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=bPbS[0])                 
                elif isinstance(tableDict[k],Queen): # Queen
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=wPwS[1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=wPbS[1])
                    else:
                        buttonDict[k].config(image=bPwS[1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=bPbS[1])           
                elif isinstance(tableDict[k],Bishop): # Bishop
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=wPwS[2]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=wPbS[2])
                    else:
                        buttonDict[k].config(image=bPwS[2]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=bPbS[2])           
                elif isinstance(tableDict[k],Knight): # Knight
                    if tableDict[k].y < 4:
                        if tableDict[k].side == 'w':
                            buttonDict[k].config(image=wPwS[3]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=wPbS[3])
                        else:
                            buttonDict[k].config(image=bPwS[3]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=bPbS[3])
                    else:
                        if tableDict[k].side == 'w':
                            buttonDict[k].config(image=wPwS[4]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=wPbS[4])
                        else:
                            buttonDict[k].config(image=bPwS[4]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=bPbS[4])            
                elif isinstance(tableDict[k],Rook): # Rook
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=wPwS[5]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=wPbS[5])
                    else:
                        buttonDict[k].config(image=bPwS[5]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=bPbS[5])           
                elif isinstance(tableDict[k],Pawn): # Pawn
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=wPwS[6]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=wPbS[6])
                    else:
                        buttonDict[k].config(image=bPwS[6]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=bPbS[6])
            else: # Empty Square
                buttonDict[k].config(image=Images[1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Images[2])

    # Button Borders Rendering
    ButtonChanged = []
    def borderColors(square,buttonDict,Self,tableDict,possibleActionsDict,enPassant):
        Move,Take = tableDict[square].possibleMoves(tableDict)[:2]
        if isinstance(Self,Pawn) and enPassant in possibleActionsDict[Self]:
            Take.append(enPassant)
        for m in Move:
            buttonDict[m].config(background='#00BB00')
            Rendering.ButtonChanged.append(buttonDict[m])
        for t in Take:
            buttonDict[t].config(background='#FF0000')
            Rendering.ButtonChanged.append(buttonDict[t])

    def borderCheck(PossibleCheck,buttonDict):
        if PossibleCheck:
            buttonDict[PossibleCheck].config(background='#FFFF00')
            Rendering.ButtonChanged.append(buttonDict[PossibleCheck])

    def borderCastling(buttonDict,Self,Turn,tableDict):
        try:
            if isinstance(Self,King):
                squares,kW,qW,kB,qB = AI.CastlingCheck(Turn,tableDict,Self)
                for v in squares:
                    buttonDict[v].config(background='#00AACC')
                    Rendering.ButtonChanged.append(buttonDict[v])
                return kW,qW,kB,qB
        except TypeError:
            None

    def borderDefault():
        for b in Rendering.ButtonChanged:
            b.config(background='SystemButtonFace')
        Rendering.ButtonChanged.clear()

    def PreviousNextButtons(canvas,buttonNext_window,buttonBack_window,rewindButtonsManage):
        if rewindButtonsManage == None:
            canvas.itemconfigure(buttonNext_window,state='normal')
            canvas.itemconfigure(buttonBack_window,state='normal')
        if rewindButtonsManage == 'noBack':
            canvas.itemconfigure(buttonBack_window,state='hidden')
            canvas.itemconfigure(buttonNext_window,state='normal')
        elif rewindButtonsManage == 'noNext':
            canvas.itemconfigure(buttonNext_window,state='hidden')
            canvas.itemconfigure(buttonBack_window,state='normal')

    # Text Rendering
    def timeShowing(ExecutionTime,Turn,Self,sta,end,ver,act):
        ExecutionTime.config( text=f"Turn: {'White' if Turn == 1 else 'Black'}\n{Self if Self is not None else ''}\n\n"
                                    f">>> Calculation Time <<<\n"
                                    f"{'Action' if act else 'Verification'}: {((act if act else ver) - sta) * 1000:,.2f} ms\n"
                                    f"Rendering: {(end - (act if act else ver)) * 1000:,.2f} ms\n"
                                    f"Execution time: {(end - sta) * 1000:,.2f} ms")    

    def printMovesDone(MoveOutput,color,output=None,rewindPos=None):
        if rewindPos:
            placeForColorStart = f"end{rewindPos}l"
            if (rewindPos+1):
                placeForColorEnd = f"end{rewindPos+1}l"
            else:
                placeForColorEnd="end"
            tags_to_remove = ["#FF0000","#00AACC","#FDD017","#00BB00","#7700FF","#0000FF"]
            for tag in tags_to_remove:
                MoveOutput.tag_remove(tag, "1.0", END)
            MoveOutput.tag_add(color, placeForColorStart, placeForColorEnd)
            MoveOutput.tag_config(color, foreground=color)
            MoveOutput.see(END)
        try:
            MoveOutput.insert(END,'\n'+output)
            tags_to_remove = ["#FF0000","#00AACC","#FDD017","#00BB00","#7700FF","#0000FF"]
            for tag in tags_to_remove:
                MoveOutput.tag_remove(tag, "1.0", END)
            MoveOutput.tag_add(color, "end-1l", "end")
            MoveOutput.tag_config(color, foreground=color)
            MoveOutput.see(END)
        except TypeError:
            None

    def delMovesDone(MoveOutput,delete):
        deleteFrom = f"end{delete+1}l"
        MoveOutput.delete(deleteFrom, END)