
import Tkinter as tk
import Pmw

from commands import do_key
from elements import *
from options  import *
from shapes   import *
from ayeoh    import *

import tkFileDialog

from time import time

import inspect

import os.path as osp

fileDlgOpts = dict(initialdir=SCENE_DIR, defaultextension='.'+SCENE_EXT, filetypes=((SCENE_DESC, '*.'+SCENE_EXT),('All Files', '*')))

def make_rawedges(vertices):
   return [(vertices[i], vertices[i+1]) for i in range(len(vertices)-1)] + [(vertices[-1], vertices[0])]

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

      self.status = \
      status = {}

      fr = tk.Frame(parent)

      status[ 'q'] = w = StatusItem(fr, 'Squares:')
      w.grid(row=0, column=0, sticky='w')

      status[ 't'] = w = StatusItem(fr, 'Triangles:', padx=6)
      w.grid(row=0, column=1, sticky='w')

      status['ee'] = w = StatusItem(fr, 'Exposed Edges:', padx=6)
      w.grid(row=0, column=2, sticky='w')

      status[ 'g'] = w = StatusItem(fr, 'Group:')
      w.grid(row=0, column=3, sticky='e')

      fr.grid(row=1, column=0, sticky='ew')

      fr.columnconfigure(2, weight=1)

   def trythis(self, modifiers=0):
      pass

   def save_scene(self, fn=None):
      if fn is None:
         fn = tkFileDialog.asksaveasfilename(**fileDlgOpts)

         if not fn:
            self.log('save aborted')
            return

      self.log('save: ' + fn)

      tiles = self.state['tiles']

      with open(fn, 'wb') as f:
         writefile(f, zip(['t']*len(tiles), tiles))

   def itemproc(self, id_, *args, **kwargs):
      if id_ == 't':
         vertices = args[0]
         rawedges = make_rawedges(vertices)
         self.add_tile(vertices, rawedges)

   def load_scene(self, fn=None):
      if fn is None:
         fn = tkFileDialog.askopenfilename(**fileDlgOpts)

         if not fn:
            self.log('load aborted')
            return

      self.log('load: ' + fn)
      state = self.state

      for t in state['tiles']:
         t.delete()

      state.update(tiles=set(), edges={}, q=0, t=0)

      with open(fn, 'rb') as f:
         readfile(f, self.itemproc)

      tile = state['tiles'].copy().pop()
      state['tile'] = tile
      state['edge'] = 0

      tile[0].activate()

      tile.activate()

   def new_tile(self, shape, debuggery):
      state = self.state

      tile  = state['tile']

      edge  = tile[state['edge']]

      if edge.tile2:
         self.log('edge full!')
         return None

      vertices = make_tile(tile, edge, shape)
      rawedges = make_rawedges(vertices)

      for e1 in rawedges:
         if not Edge.signature(*e1) in state['edges']:
            for e2 in state['edges'].itervalues():
               if e2.intersect_check(e1, debuggery):
                  self.log('overlap!')
                  return None

      newtile = self.add_tile(vertices, rawedges)

      self.cvs.tag_raise(edge.id_)

      return newtile

   def add_tile(self, vertices, rawedges):
      st    = self.state

      tile  = Tile(self.cvs, vertices, self.make_edges(rawedges), self)
      st['tiles'].add(tile)

      shape = 'q' if len(vertices) == 4 else 't'

      st[shape] += 1
      self.status[shape].update(st[shape])

      self.scrfr.resizescrollregion()

      return tile

   def activate_tile(self, newtile):
      state = self.state

      tile  = state['tile']

      edge  = tile[state['edge']]

      state['tile'] = newtile

      tile.deactivate()
      newtile.activate()

      for i in range(len(newtile)):
         if newtile[i] == edge:
            state['edge'] = i

   def add_edge(self, p1, p2):

      edges = self.state['edges']
      sign = Edge.signature(p1, p2)

      # order of points may be reversed
      if sign in edges:
         e = edges[sign]

      else:
         e = Edge(self.cvs, p1, p2, self)
         edges[sign] = e

      return e

   def edge_cleanup(self, e):

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
         if len(tile) == 4:
            shape = 'q'
         else:
            shape = 't'

         state[shape] -= 1

         self.status[shape].update(state[shape])

         state['tiles'].remove(rmtile)
         rmtile.delete()

      else:
         self.log('no tile to delete')

   def do_delete_many(self):
      state    = self.state

      alltiles = state['tiles']
      rmtiles  = [t for t in alltiles if t.selected]

      if len(alltiles) == len(rmtiles):
         self.log('at least one tile must remain!')
         return

      oh_noes = False

      for tile in rmtiles:
         if tile  == state['tile']:
            self.log('oh noes!')
            oh_noes = True
            tile[state['edge']].deactivate()

         if len(tile) == 4:
            shape = 'q'
         else:
            shape = 't'

         state[shape] -= 1

         alltiles.remove(tile)
         tile.delete()

      if oh_noes:
         tile = alltiles.copy().pop()
         state['tile'] = tile
         state['edge'] = 0

         tile[0].activate()

         tile.activate()

      self.status['q'].update(state['q'])
      self.status['t'].update(state['t'])

   # e1, e2 may be a plain pair of Points
   def highlight_edges(self, e1, e2, pt):

      cvs = self.cvs
      hilites = self.highlights

      if hilites[0]:
         cvs.delete(hilites[0])
         cvs.delete(hilites[1])
         cvs.delets(hilites[2])

      hilites[0] = cvs.create_line(*e1, width=3, fill=HILIGHT_ERR)
      hilites[1] = cvs.create_line(*e2, width=3, fill=HILIGHT_ERR)
      hilites[2] = cvs.create_oval(pt.x-4, pt.y-4, pt.x+4, pt.y+4, width=0, fill=HILIGHT_ERR)

   def clear_highlights(self):
      hilites = self.highlights

      if hilites[0] is None:
         return

      self.cvs.delete(hilites[0])
      self.cvs.delete(hilites[1])
      self.cvs.delete(hilites[2])

      hilites[0] = hilites[1] = hilites[2] = None

   def log(self, *msgitems):
      msg = ' '.join(map(str, msgitems))

      s = time()-self.t0
      h, s = divmod(s, 3600)
      m, s = divmod(s, 60)

      # as per https://docs.python.org/2/library/inspect.html#the-interpreter-stack
      caller = inspect.stack()[1][0]
      try:
         info = inspect.getframeinfo(caller)
      finally:
         del caller

      logentry = '%d:%02d:%02.1f [%s/%s:%d] %s' % ( h, m, s,
         osp.basename(info.filename), info.function, info.lineno, msg )

      print logentry

   # shape0 is "q", "t" or "l" to load from a file
   def __init__(self, parent, shape0, exitfxn=None):
      tk.Frame.__init__(self)

      self.t0 = time()

      self.log('initial tile: ' + shape0)

      self.buildGUI(parent)

      self.exitfxn = exitfxn

      self.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)

      self.highlights = [None, None, None]

      self.state = {
         'tiles'  : set(), 'edges' : {}, 'q': 0,
         'tile'   :  None, 'edge'  :  0, 't': 0,
      }

      if shape0 == 'l':
         self.load_scene()

      else:
         vertices = do_start_tile(shape0)
         rawedges = make_rawedges(vertices)

         self.state['tile'] = tile0 = self.add_tile(vertices, rawedges)

         tile0[0].activate()

         tile0.activate()
