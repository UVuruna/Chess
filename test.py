import tkinter as tk
from tkinter import messagebox

def NewGame_YesNo():
    result = messagebox.askyesno("New Game", "Are you sure you want to quit current Game?")
    
    if result:
        print("Korisnik je odabrao Yes.")
    else:
        print("Korisnik je odabrao No.")

# Kreiranje glavnog prozora
root = tk.Tk()
root.title("Yes/No Window Example")

# Dugme koje prikazuje Yes/No prozor
button = tk.Button(root, text="Prikaži Yes/No prozor", command=show_yes_no_window)
button.pack(pady=30)

# Pokretanje glavne petlje
root.mainloop()