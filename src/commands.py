
def do_key(host, e):

   # WANTED

   # maybe later, buttons/function keys might be good for these
   # save/load, start new

   # show/hide cursors
   # deselect all

   # tab to navigate among disconnected groups of tiles

   # maybe some mode selecting, such as view center follows active tile
   # other sensible modes? set new tiles as active tile, maybe

   # can't pan around if canvas too small
   # load/save would make that less interesting

   print e.keysym

   state = host.state

   # new tile
   # hold shift to keep active tile
   # otherwise new tile becomes active
   if   e.keysym in ('q', 't'):
      newtile = host.new_tile(e.keysym)

      if newtile:
         host.select_tile(newtile)

   # edges, ccw
   # hold shift to rotate scene fifteen degrees
   elif e.keysym == 'Left':
      host.prev_edge()

   # edges, cw
   # hold shift to rotate scene fifteen degrees
   elif e.keysym == 'Right':
      host.next_edge()

   # set active tile to tile across active edge
   elif e.keysym == 'space':

      tile = state['tile']

      edge = tile[state['edge']]

      newtile = edge.tile2 if edge.tile1 == tile else edge.tile1

      if newtile:
         host.select_tile(newtile)

   # center view on active tile
   # hold shift to recenter canvas on the active tile
   elif e.keysym == 'c':
      pass

   # exit program
   elif e.keysym == 'Escape':
      f = host.exitfxn
      if callable(f):
         f()

   # (un)select active tile
   elif e.keysym in ('Control_R', 'Control_L'):
      pass

   # delete the tile across active edge,
   # shift deletes selected tiles
   elif e.keysym == 'Delete':
      host.do_delete_single()

   # undo, hold shift to redo
   elif e.keysym == 'BackSpace':
      pass

   # show help window
   elif e.keysym in ('h', 'question', 'F1'):
      pass
