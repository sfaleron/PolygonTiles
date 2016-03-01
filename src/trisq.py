
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

      status['e'] = w = StatusItem(fr, 'Exposed Edges:', padx=6)
      w.grid(row=0, column=2, sticky='w')

      status['g'] = w = StatusItem(fr, 'Group:')
      w.grid(row=0, column=3, sticky='e')

      fr.grid(row=1, column=0, sticky='ew')

      fr.columnconfigure(2, weight=1)

   def new_tile(self, shape):
      state = self.state

      tile  = state['tile']

      edge  = tile[state['edge']]

      if edge.tile2:
         print 'edge full!'
         return None

      rawedges = make_tile(tile, edge, shape)

      for e1 in rawedges:
         if not Edge.signature(*e1) in state['edges']:
            for e2 in state['edges'].itervalues():
               if e2.intersect_check(e1):
                  print 'overlap!'
                  return None

      newtile = self.add_tile(rawedges)

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
      state = self.state

      tile  = state['tile']

      edge  = tile[state['edge']]

      state['tile'] = newtile

      tile.deactivate()
      newtile.activate()

      for e in range(len(newtile)):
         if newtile[e] == edge:
            state['edge'] = e

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
      state = self.state

      edges = state['tile']
      i = state['edge']

      edges[i].deactivate()

      state['edge'] = \
      i = (i-1) % len(edges)

      edges[i].activate()

   def next_edge(self):
      state = self.state

      edges = state['tile']
      i = state['edge']

      edges[i].deactivate()

      state['edge'] = \
      i = (i+1) % len(edges)

      edges[i].activate()

   def make_edges(self, rawedges):
      return [self.add_edge(*i) for i in rawedges]

   def do_delete_single(self):
      state = self.state
      tile  = state['tile']
      edge  = tile[state['edge']]

      rmtile = edge.tile2 if edge.tile1 == tile else edge.tile1

      if rmtile:
         state['tiles'].remove(rmtile)
         rmtile.delete()

      else:
         print 'no tile to delete'

   # tile0 is "q" or "t"
   def __init__(self, parent, shape0, exitfxn=None):
      tk.Frame.__init__(self)

      self.buildGUI(parent)

      self.exitfxn = exitfxn

      self.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)

      self.state = {
         'tiles' : set(), 'edges' : {}, 'q': 0,
         'tile'  :  None, 'edge'  :  0, 't': 0
      }

      self.state['tile'] = tile0 = self.add_tile(do_start_tile(shape0))

      tile0[0].activate()

      tile0.activate()
