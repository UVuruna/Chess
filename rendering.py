from Pieces import *
from chess import Chess
from tkinter import *
from transcript import Rewind


class Rendering():

    # AllImages[0] Rendering   
    def RenderingScreen(tableDict,buttonDict,AllImages):
        for k,v in tableDict.items(): # Ovo je glupo malo jer svaki put prolazi kroz All Images bes potrebe (moze da se izvuce ispred)
            if v != '':  #          ali nema veze jer se to radi samo u igri (nakon odigravanja poteza), ne u izracunavanju poteza (ne usporava kalkulacije)
                if isinstance(tableDict[k],King): # King
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=AllImages[1][0]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[2][0])
                    else:
                        buttonDict[k].config(image=AllImages[3][0]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[4][0])                 
                elif isinstance(tableDict[k],Queen): # Queen
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=AllImages[1][1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[2][1])
                    else:
                        buttonDict[k].config(image=AllImages[3][1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[4][1])           
                elif isinstance(tableDict[k],Bishop): # Bishop
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=AllImages[1][2]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[2][2])
                    else:
                        buttonDict[k].config(image=AllImages[3][2]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[4][2])           
                elif isinstance(tableDict[k],Knight): # Knight
                    if tableDict[k].y < 4:
                        if tableDict[k].side == 'w':
                            buttonDict[k].config(image=AllImages[1][3]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[2][3])
                        else:
                            buttonDict[k].config(image=AllImages[3][3]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[4][3])
                    else:
                        if tableDict[k].side == 'w':
                            buttonDict[k].config(image=AllImages[1][4]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[2][4])
                        else:
                            buttonDict[k].config(image=AllImages[3][4]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[4][4])            
                elif isinstance(tableDict[k],Rook): # Rook
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=AllImages[1][5]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[2][5])
                    else:
                        buttonDict[k].config(image=AllImages[3][5]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[4][5])           
                elif isinstance(tableDict[k],Pawn): # Pawn
                    if tableDict[k].side == 'w':
                        buttonDict[k].config(image=AllImages[1][6]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[2][6])
                    else:
                        buttonDict[k].config(image=AllImages[3][6]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[4][6])
            else: # Empty Square
                buttonDict[k].config(image=AllImages[0][1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=AllImages[0][2])

    # Button Borders Rendering
    ButtonChanged = []
    def borderColors(square,buttonDict,Self):
        if not isinstance(Self,Pawn):
            MoveColor,TakeColor = Self.move,Self.take
        else:
            MoveColor,TakeColor = Self.passiv_move,Self.take
        for m in MoveColor:
            buttonDict[m].config(background='#00BB00')
            Rendering.ButtonChanged.append(buttonDict[m])
        for t in TakeColor:
            buttonDict[t].config(background='#FF0000')
            Rendering.ButtonChanged.append(buttonDict[t])
        if isinstance(Self,King) and Self.castling:
            for c in Self.castling:
                buttonDict[c].config(background='#00AACC')
                Rendering.ButtonChanged.append(buttonDict[c])

    def borderCheck(buttonDict):
        if Chess.Check:
            for k in Chess.Check.keys():
                checkColor = k[2]
                break
            buttonDict[checkColor].config(background='#FFFF00')
            Rendering.ButtonChanged.append(buttonDict[checkColor])

    def borderDefault():
        for b in Rendering.ButtonChanged:
            b.config(background='SystemButtonFace')
        Rendering.ButtonChanged.clear()

    def HidingButtons(canvas,*buttons):
        for but in buttons:
            current_state = canvas.itemcget(but, 'state')
            if current_state != 'hidden':
                canvas.itemconfigure(but, state='hidden')
    def ShowingButtons(canvas,*buttons):
        for but in buttons:
            current_state = canvas.itemcget(but, 'state')
            if current_state != 'normal':
                canvas.itemconfigure(but, state='normal')

    def PreviousNextButtons(canvas,buttonNext_window,buttonBack_window,rewindButtonsManage):
        if rewindButtonsManage == None:
            Rendering.ShowingButtons(canvas,buttonNext_window,buttonBack_window)
        if rewindButtonsManage == 'noBack':
            Rendering.HidingButtons(canvas,buttonBack_window)
            Rendering.ShowingButtons(canvas,buttonNext_window)
        elif rewindButtonsManage == 'noNext':
            Rendering.HidingButtons(canvas,buttonNext_window)
            Rendering.ShowingButtons(canvas,buttonBack_window)

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

    def printActionResult(Turn,posInTransc,TranscriptName,moveCounter,MoveOutput,output,transcript,color):
        Turn *=-1
        moveCounter +=1  
        with open(f'{TranscriptName}.txt','a') as f:
            f.write(f'{moveCounter} {transcript}')
        output = f"{(str(moveCounter)+'.').ljust(4)}{output}"
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
        return Turn,posInTransc,moveCounter
    
    def printPawnPromotiong(Self,promote,posInTransc,TranscriptName,canvas,MoveOutput,ExtraPiecesButtons,ExecutionTime_window,moveCounter):
        Rendering.HidingButtons(canvas,*ExtraPiecesButtons)
        Rendering.ShowingButtons(canvas,ExecutionTime_window)
        with open(f'{TranscriptName}.txt','a') as f:
            f.write(f"{moveCounter} promote {str(promote)[1:]} {Chess.NotationTableDict[promote.getXY()]}\n")
        output = f"{' -'.ljust(4)}{str(Self).ljust(8)}{(Chess.NotationTableDict[promote.getXY()].ljust(5)+'⛨').ljust(8)}{promote}"
        if posInTransc <-1:
            Rendering.delMovesDone(MoveOutput,posInTransc)
        Rendering.printMovesDone(MoveOutput,"#7700FF",output,None)