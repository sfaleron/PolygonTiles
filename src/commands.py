
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

   host.clear_highlights()

   shifty = bool(e.state&1)

   keysym = e.keysym

   msgbits = ['key:']

   if shifty:
      msgbits.append('shift')

   msgbits.append(e.keysym)

   host.log(*msgbits)

   state = host.state

   # new tile
   # hold shift to keep active tile
   # hold alt key to add debug info to messages
   # otherwise new tile becomes active
   if   keysym.lower() in ('q', 't'):
      newtile = host.new_tile(e.keysym, bool(e.state&0x88))

      if newtile and not shifty:
         host.activate_tile(newtile)

   elif keysym.lower() == 'l':
      host.load_scene()

   elif keysym.lower() == 's':
      host.save_scene()

   # edges, ccw
   # hold shift to rotate scene fifteen degrees
   elif keysym == 'Left':
      host.prev_edge()

   # edges, cw
   # hold shift to rotate scene fifteen degrees
   elif keysym == 'Right':
      host.next_edge()

   # set active tile to tile across active edge
   elif keysym =='KP_Insert':

      tile = state['tile']

      edge = tile[state['edge']]

      newtile = edge.tile2 if edge.tile1 == tile else edge.tile1

      if newtile:
         host.activate_tile(newtile)

   # center view on active tile
   # hold shift to recenter canvas on the active tile
   elif keysym == 'c':
      pass

   # exit program
   elif keysym == 'Escape':
      f = host.exitfxn
      if callable(f):
         f()

   # (un)select active tile
   elif keysym in ('Control_R', 'Control_L'):
      state['tile'].select_toggle()

   # delete the tile across active edge,
   # shift deletes selected tiles
   elif keysym == 'Delete':
      if shifty:
         host.do_delete_many()
      else:
         host.do_delete_single()

   # undo, hold shift to redo
   elif keysym == 'BackSpace':
      pass

   # show help window
   elif keysym in ('h', 'question', 'F1'):
      pass

   elif keysym in ('plus', 'KP_Add'):
      state['tile'][state['edge']].highlight_toggle()

   # fill-in-the-blank debuging/test function, possibly ignored
   elif keysym == 'KP_Begin':
      host.trythis(e.state)
