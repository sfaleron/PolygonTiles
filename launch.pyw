
import Tkinter as tk

import Pmw

choice = set()

def set_choice(e):
   ch  = e.keysym
   top = e.widget

   choice.add(ch)
   top.quit()

def buildGUI(top):

   top['borderwidth'] = 8

   lbl = tk.Label(top, text='Choose starting tile:', font='Sans 14 underline')
   lbl.grid(row=0, column=0, columnspan=2, sticky='ew')

   lbl = tk.Label(top, text='Q: square', font='Sans 12')
   lbl.grid(row=1, column=0, sticky='ew')

   lbl = tk.Label(top, text='T: triangle', font='Sans 12')
   lbl.grid(row=1, column=1, sticky='ew')

   top.resizable(False, False)

   top.bind('<Escape>', lambda e: top.quit())
   top.bind('q', set_choice)
   top.bind('t', set_choice)

from src import TriSq

top = tk.Tk()
top.title('Starting Tile')
buildGUI(top)
top.mainloop()
top.destroy()

if choice:
   top = Pmw.initialise(tk.Tk())
   top.title('TriSq')
   app = TriSq(top, choice.pop(), top.quit)
   app.grid(row=0, column=0, sticky='nsew')

   top.rowconfigure(0, weight=1)
   top.columnconfigure(0, weight=1)

   top.mainloop()
