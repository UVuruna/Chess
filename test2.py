def TimeForOperations(n,AllActions,PossibleActions,castlingCheck,ClearPossibleActions):
    timingsAllActionsSET = []
    timingsPossibleActionsSET = []
    timingsResetActionsSET = []
    for _ in range(n):
        start = time.time()
        for p in Chess.pieces:
            AllActions(p,CurrentTableDict)
        end = time.time()
        timingsAllActionsSET.append(end-start)
        wk,wlr,wrr,bk,blr,brr=PossibleActions()
        castlingCheck(wk,wlr,wrr,bk,blr,brr)
        end1 = time.time()
        timingsPossibleActionsSET.append(end1-end)
        ClearPossibleActions()
        end2 = time.time()
        timingsResetActionsSET.append(end2-end1)

    a = sum(timingsAllActionsSET)/len(timingsAllActionsSET)
    b = sum(timingsPossibleActionsSET)/len(timingsPossibleActionsSET)
    c = sum(timingsResetActionsSET)/len(timingsResetActionsSET)
    return a,b,c