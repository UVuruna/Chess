


class Rendering():

    # Images Rendering   
    def RenderingScreen(TableDict):
        CurrentTableDict = TableDict
        for k,v in CurrentTableDict.items():
            if v != '': 
                if isinstance(CurrentTableDict[k],King): # King
                    if CurrentTableDict[k].side == 'w':
                        buttonDict[k].config(image=Import.Img_wPwS[0]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_wPbS[0])
                    else:
                        buttonDict[k].config(image=Import.Img_bPwS[0]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_bPbS[0])                 
                elif isinstance(CurrentTableDict[k],Queen): # Queen
                    if CurrentTableDict[k].side == 'w':
                        buttonDict[k].config(image=Import.Img_wPwS[1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_wPbS[1])
                    else:
                        buttonDict[k].config(image=Import.Img_bPwS[1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_bPbS[1])           
                elif isinstance(CurrentTableDict[k],Bishop): # Bishop
                    if CurrentTableDict[k].side == 'w':
                        buttonDict[k].config(image=Import.Img_wPwS[2]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_wPbS[2])
                    else:
                        buttonDict[k].config(image=Import.Img_bPwS[2]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_bPbS[2])           
                elif isinstance(CurrentTableDict[k],Knight): # Knight
                    if CurrentTableDict[k].y < 4:
                        if CurrentTableDict[k].side == 'w':
                            buttonDict[k].config(image=Import.Img_wPwS[3]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_wPbS[3])
                        else:
                            buttonDict[k].config(image=Import.Img_bPwS[3]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_bPbS[3])
                    else:
                        if CurrentTableDict[k].side == 'w':
                            buttonDict[k].config(image=Import.Img_wPwS[4]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_wPbS[4])
                        else:
                            buttonDict[k].config(image=Import.Img_bPwS[4]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_bPbS[4])            
                elif isinstance(CurrentTableDict[k],Rook): # Rook
                    if CurrentTableDict[k].side == 'w':
                        buttonDict[k].config(image=Import.Img_wPwS[5]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_wPbS[5])
                    else:
                        buttonDict[k].config(image=Import.Img_bPwS[5]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_bPbS[5])           
                elif isinstance(CurrentTableDict[k],Pawn): # Pawn
                    if CurrentTableDict[k].side == 'w':
                        buttonDict[k].config(image=Import.Img_wPwS[6]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_wPbS[6])
                    else:
                        buttonDict[k].config(image=Import.Img_bPwS[6]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Img_bPbS[6])
            else: # Empty Square
                buttonDict[k].config(image=Import.Images[1]) if buttonDict[k].color == 'w' else buttonDict[k].config(image=Import.Images[2])

    # Button Borders Rendering
    ButtonChanged = []
    def borderColors(square):
        Move,Take = CurrentTableDict[square].possibleMoves(CurrentTableDict)[:2]
        if isinstance(Self,Pawn) and enPassant in possibleActionsDict[Self]:
            Take.append(enPassant)
        for m in Move:
            buttonDict[m].config(background='#00BB00')
            Rendering.ButtonChanged.append(buttonDict[m])
        for t in Take:
            buttonDict[t].config(background='#FF0000')
            Rendering.ButtonChanged.append(buttonDict[t])

    def borderCheck(PossibleCheck):
        if PossibleCheck:
            buttonDict[PossibleCheck].config(background='#FFFF00')
            Rendering.ButtonChanged.append(buttonDict[PossibleCheck])

    def borderCastling():
        global kW,qW,kB,qB
        try:
            if isinstance(Self,King):
                squares,kW,qW,kB,qB = AI.CastlingCheck(Turn,CurrentTableDict,Self)
                for v in squares:
                    buttonDict[v].config(background='#00AACC')
                    Rendering.ButtonChanged.append(buttonDict[v])
        except TypeError:
            None

    def borderDefault():
        for b in Rendering.ButtonChanged:
            b.config(background='SystemButtonFace')
        Rendering.ButtonChanged.clear()

    def PreviousNextButtons(rewindButtonsManage):
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
    def timeShowing(sta,end,ver,act):
        ExecutionTime.config( text=f"Turn: {'White' if Turn == 1 else 'Black'}\n{Self if Self is not None else ''}\n\n"
                                    f">>> Calculation Time <<<\n"
                                    f"{'Action' if act else 'Verification'}: {((act if act else ver) - sta) * 1000:,.2f} ms\n"
                                    f"Rendering: {(end - (act if act else ver)) * 1000:,.2f} ms\n"
                                    f"Execution time: {(end - sta) * 1000:,.2f} ms")    

    def printMovesDone(color,output=None,rewindPos=None,delete=None):
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

    def delMovesDone(delete):
        deleteFrom = f"end{delete+1}l"
        MoveOutput.delete(deleteFrom, END)