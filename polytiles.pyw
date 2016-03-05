# ==============================================================================
# == Copyright 2016 Christopher Fuller                                        ==
# ==                                                                          ==
# == Licensed under the Apache License, Version 2.0 (the "License");          ==
# == you may not use this file except in compliance with the License.         ==
# == You may obtain a copy of the License at                                  ==
# ==                                                                          ==
# ==   http://www.apache.org/licenses/LICENSE-2.0                             ==
# ==                                                                          ==
# == Unless required by applicable law or agreed to in writing, software      ==
# == distributed under the License is distributed on an "AS IS" BASIS,        ==
# == WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. ==
# == See the License for the specific language governing permissions and      ==
# == limitations under the License.                                           ==
# ==============================================================================

import os
import os.path as osp

from src import PolyTiles, SCENE_DIR, APP_TITLE

d = osp.dirname(__file__)
if d:
   os.chdir(d)

if not osp.exists(SCENE_DIR):
   os.mkdir(SCENE_DIR)


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

   lbl = tk.Label(top, text='L: load scene', font='Sans 12')
   lbl.grid(row=2, column=0, columnspan=2, sticky='ew')

   top.resizable(False, False)

   top.bind('<Escape>', lambda e: top.quit())
   top.bind('q', set_choice)
   top.bind('t', set_choice)
   top.bind('l', set_choice)

top = tk.Tk()
top.title('Starting Tile')
buildGUI(top)
top.mainloop()
top.destroy()

if choice:
   top = Pmw.initialise(tk.Tk())
   top.title(APP_TITLE)
   app = PolyTiles(top, choice.pop(), top.quit)
   app.grid(row=0, column=0, sticky='nsew')

   top.rowconfigure(0, weight=1)
   top.columnconfigure(0, weight=1)

   # if the user selected load, but aborted, then just quit
   if app.state['tiles']:
      app.present()
      top.mainloop()
