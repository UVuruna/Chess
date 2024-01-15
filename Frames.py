from tkinter import *
from PIL import ImageTk, Image
from Pieces import *
from Rendering import Rendering
from ImagesDecorators import *
import os


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

    def CanvasCreate(window,images):
        # Canvas 1
        MainPanel.canvasTable = Canvas(window, width=1000, height=1000)
        MainPanel.canvasTable.place(anchor=NW,x=0,y=0)
        MainPanel.canvasTable.create_image(0,0, anchor=NW, image=images[0])
        # Canvas 2
        MainPanel.canvasSide = Canvas(window, width=550, height=1000)
        MainPanel.canvasSide.place(anchor=NW,x=1000,y=0)
        MainPanel.canvasSide.create_image(0,0, anchor=NW, image=images[3])

    def TableButtons(window,images,GameMechanic):
        border_Dist = 97 ; butt_Dimension = 101.7
        ButtonReferences = list(Chess.emptyTableDict().keys())
        ButtonDict = {}
        for i in range(64): 
            n=8             # Ovaj deo je da se napravi matrica (8*8) od liste 
            x = i//n        # zbog postavke BUTTONA na CANVAS (pozicije XY)
            y = i-x*n       # Radi izracunavanja koordinata preko FORMULE
                                        
            button = Button(window)               # kreiranje Buttona
            button.text = ButtonReferences[i]     # ubacivanje Atributa koji opisuje poziciju. Improvizovana ButtonID
            button.config(border=2,command=lambda text = button.text: (GameMechanic(text)))                       # FUNKCIJA Buttona
            button.bind("<Enter>",lambda event, text = button: MainPanel.Hover(event,text))                                # Set Hover
            button.bind("<Leave>",lambda event, text = button: MainPanel.ClearHover(event,text))                           # Clear Hover
            button_window = MainPanel.canvasTable.create_window(1,1, anchor=NW, window=button)                             # kreiranje prozora buttona
            MainPanel.canvasTable.coords(button_window,(border_Dist+y*butt_Dimension),(border_Dist+(7-x)*butt_Dimension))  # postavljanje buttona na EKRAN
            ButtonDict[button.text] = button     # Ubacivanje Buttona u RECNIK                            

                # Default Square Color
            button.config(image=images[2]) if (x%2==0 and y%2==0) or (x%2==1 and y%2==1) else button.config(image=images[1])
            button.color =             'b' if (x%2==0 and y%2==0) or (x%2==1 and y%2==1) else 'w'
        return ButtonDict

    def ShowcaseScreen(window,Phase):
        Phase = "Start"
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
    FirstOpponent       = None
    SecondOpponent      = None
    MoveOutput          = None
    ExecutionTime       = None
    ExecutionTime_win   = None
    StatisticFrame      = None
    StatisticFrame_win  = None
    but_SG_win          = None
    but_GM_win          = None
    but_Back_win        = None
    but_Next_win        = None

    def SideCanvas_Parts(window,ObjType, bordeR, x,y, w=None,h=None, txt=None, fontStyle=None, method=None,args=None):
        if ObjType ==Button:
            button = ObjType(window, background='#969696', border=bordeR, font=fontStyle, width=w, height=h, text=txt, command=lambda: method(args) if args else method())
            button_window = MainPanel.canvasSide.create_window(x,y, anchor=NW, window=button)
            return button_window,button

    Screen_1_Frames = []
    @Decorator.ListAppend(Screen_1_Frames)
    def Screen_1(window):
        SidePanel.FirstOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        text_FirstOpponent_win = MainPanel.canvasSide.create_window(280,900, anchor=NW, window=SidePanel.FirstOpponent)
        SidePanel.FirstOpponent.insert(1.0, "1stPlayer")

        SidePanel.SecondOpponent = Text(window, width= 16, height=1, bg= '#CCCCCC', fg='black', font=('Tahoma', 22))
        text_SecondOpponent_win = MainPanel.canvasSide.create_window(280,945, anchor=NW, window=SidePanel.SecondOpponent)
        SidePanel.SecondOpponent.insert(1.0, "2ndPlayer")

        but_SaveTransc_win =SidePanel.SideCanvas_Parts(Button, 5, 300,780,  16,3, 'Saving Game\nwith\nTranscript',('Tahoma', 18), SidePanel.SavedGames,'players')[0]
        but_GameTransc_win =SidePanel.SideCanvas_Parts(Button, 5,  10,780,  8,3, 'Casual\nGame',('Tahoma', 33, 'bold'), SidePanel.SavedGames)[0]

        return text_FirstOpponent_win,text_SecondOpponent_win,but_SaveTransc_win,but_GameTransc_win

    def Screen_2(window,StandardGame,GodMode):
        SidePanel.MoveOutput = Text(window, width= 550, height=22, bg= '#535a5e', font=('Tahoma', 22))
        SidePanel.MoveOutput.place(anchor=NW,x=1000,y=2)

        exTiText = 'Standard Game:\nNormal Chess game\nwith all rules applied\n\nGod Mode:\nDelete: Remove Piece\nInsert: Freely move Piece\nRightClick: Change Turn'
        SidePanel.ExecutionTime = Label(window, font=('Eras Demi ITC', 16), width=24, height=8, bd=2, background='#969696', text=exTiText)
        SidePanel.ExecutionTime_win = MainPanel.canvasSide.create_window(220, 787, anchor=NW, window=SidePanel.ExecutionTime)

        SidePanel.but_SG_win =SidePanel.SideCanvas_Parts(Button, 3, 10,780,  9,2, 'Standard\nGame',('Eras Demi ITC', 24), StandardGame)[0]
        SidePanel.but_GM_win =SidePanel.SideCanvas_Parts(Button, 3, 10,890,  9,2, 'God Mode',('Eras Demi ITC', 24), GodMode)[0]
    
    def Screen_Game(NewGame,Previous,Next):
        SidePanel.SideCanvas_Parts(Button, 3,  10,780,  9,2, 'New Game',('Eras Demi ITC', 24), NewGame)[0]
        SidePanel.but_Back_win =SidePanel.SideCanvas_Parts(Button, 3,  10,900,  3,1, '⯬🢠',('Eras Demi ITC', 33), Previous)[0]
        SidePanel.but_Next_win =SidePanel.SideCanvas_Parts(Button, 3, 108,900,  3,1, '🢡⯮',('Eras Demi ITC', 33), Next)[0]

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

    def Statistic(window,StatisticText):
        SidePanel.StatisticFrame = Label(window, font=('Eras Demi ITC', 15), background= '#535a5e', width=45, height=33, bd=2, text=StatisticText, anchor="w", justify="left", wraplength=544)
        SidePanel.StatisticFrame_win = MainPanel.canvasSide.create_window(1, 1, anchor=NW, window=SidePanel.StatisticFrame)

    ExtraPiecesButtons = []
    @Decorator.ListAppend(ExtraPiecesButtons)
    def PawnPromotionButtons(PawnPromotion,Self,Turn):
        SidePanel.ExtraPiecesButtons.clear()
        but_Q_win,but_Q =SidePanel.SideCanvas_Parts(Button, 5, 254,784, method =PawnPromotion, args=Queen(Self.side,'extra'))
        but_B_win,but_B =SidePanel.SideCanvas_Parts(Button, 5, 254,892, method =PawnPromotion, args=Bishop(Self.side,'extra'))
        but_K_win,but_K =SidePanel.SideCanvas_Parts(Button, 5, 392,892, method =PawnPromotion, args=Knight(Self.side,'extra'))
        but_R_win,but_R =SidePanel.SideCanvas_Parts(Button, 5, 392,784, method =PawnPromotion, args=Rook(Self.side,'extra'))

        if Turn == 1:
            but_Q.config(image=Import.AllImages[2][1] if Turn==1 else Import.AllImages[3][1])
            but_B.config(image=Import.AllImages[2][2] if Turn==1 else Import.AllImages[3][2])
            but_K.config(image=Import.AllImages[2][3] if Turn==1 else Import.AllImages[3][3])
            but_R.config(image=Import.AllImages[2][5] if Turn==1 else Import.AllImages[3][5])
        return but_Q_win,but_B_win,but_K_win,but_R_win