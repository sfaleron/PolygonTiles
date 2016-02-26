
import Tkinter as tk
import Pmw

from commands import do_key
from elements import *
from options  import *
from shapes   import *

class StatusItem(tk.Frame):
   def __init__(self, parent, label, **kwargs):
      tk.Frame.__init__(self, parent, **kwargs)
      lbl = tk.Label(self, text=label, font='sans 10')
      lbl.grid(row=0, column=0)
      self.field = tk.Label(self, text='--', font='sans 10')
      self.field.grid(row=0, column=1)

   def update(self, val):
      self.field['text'] = str(val)

class TriSq(tk.Frame):
   def buildGUI(self, parent):
      self.scrfr = \
      scrfr = Pmw.ScrolledCanvas(parent, usehullsize=True,
           hull_width = VIEW_WIDTH, hull_height = VIEW_HEIGHT,
           canvas_width = CVS_WIDTH, canvas_height = CVS_HEIGHT )

      self.cvs = \
      cvs = scrfr.component('canvas')

      cvs.bind('<KeyRelease>', lambda e: do_key(self, e))
      cvs.focus_set()

      scrfr.grid(row=0, column=0, sticky='nsew')

      fr = tk.Frame(parent)

      self.status = \
      status = {}

      status['q'] = w = StatusItem(fr, 'Squares:')
      w.grid(row=0, column=0, sticky='w')

      status['t'] = w = StatusItem(fr, 'Triangles:', padx=6)
      w.grid(row=0, column=1, sticky='w')

      status['g'] = w = StatusItem(fr, 'Group:')
      w.grid(row=0, column=3, sticky='e')

      fr.grid(row=1, column=0, sticky='ew')

      fr.columnconfigure(2, weight=1)

   def new_tile(self, shape):
      tile = self.active_tile
      edge = tile.edges[self.active_edge]

      newtile = self.add_tile(make_tile(tile, edge, shape))

      self.cvs.tag_raise(edge.id_)

      return newtile

   def add_tile(self, rawedges):
      st    = self.state

      tile  = Tile(self.cvs, zip(*rawedges)[0], self.make_edges(rawedges))
      st['tiles'].add(tile)

      shape = 'q' if len(rawedges) == 4 else 't'

      st[shape] += 1
      self.status[shape].update(st[shape])

      self.scrfr.resizescrollregion()

      return tile

   def select_tile(self, newtile):
      tile = self.active_tile
      self.active_tile = newtile
      edge = tile.edges[self.active_edge]

      tile.deactivate()
      newtile.activate()

      for e in range(len(newtile.edges)):
         if newtile.edges[e] == edge:
            self.active_edge = e

   def add_edge(self, p1, p2):

      edges = self.state['edges']
      sign = Edge.signature(p1, p2)

      # order of points may be reversed
      if sign in edges:
         e = edges[sign]

      else:
         e = Edge(self.cvs, p1, p2, self.remove_edge)
         edges[sign] = e

      return e

   def remove_edge(self, e):

      edges = self.state['edges']
      sign = Edge.signature(*e)

      edges.pop(sign)

   def prev_edge(self):
      edges = self.active_tile.edges
      i  = self.active_edge

      edges[i].deactivate()

      self.active_edge = \
      i = (i-1) % len(edges)

      edges[i].activate()

   def next_edge(self):
      edges = self.active_tile.edges
      i  = self.active_edge

      edges[i].deactivate()

      self.active_edge = \
      i = (i+1) % len(edges)

      edges[i].activate()

   def make_edges(self, rawedges):
      return [self.add_edge(*i) for i in rawedges]

   # tile0 is "q" or "t"
   def __init__(self, parent, shape0, exitfxn=None):
      tk.Frame.__init__(self)

      self.buildGUI(parent)

      self.exitfxn = exitfxn

      self.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)

      self.state = { 'tiles' : set(), 'edges': {}, 'q': 0, 't': 0 }

      tile0 = self.add_tile(do_start_tile(shape0))

      self.active_tile = tile0
      self.active_edge = 0

      tile0.edges[0].activate()

      tile0.activate()
