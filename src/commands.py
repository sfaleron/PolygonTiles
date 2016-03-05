
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

# getting these straight is nuttier than I thought. A point/click interface
# might have been less pain to get going, after all.
def do_key(host, e):

   host.clear_highlights()

   ks  = e.keysym

   if len(ks) == 1:
      ks = ks.lower()

   kc  = e.keycode
   ksn = e.keysym_num

   shifty = bool(e.state&1)

   msgbits = ['key:']

   if shifty:
      msgbits.append('shift')

   msgbits.append(ks)
   host.log(*msgbits)

   state = host.state

   # new tile
   # hold shift to keep active tile
   # hold alt key to add debug info to messages
   # otherwise new tile becomes active
   if   ks in ('q', 't'):
      newtile = host.new_tile(ks, bool(e.state&4))

      if newtile and not shifty:
         host.activate_tile(newtile)

   elif ks == 'l':
      host.load_scene()

   elif ks == 's':
      host.save_scene()

   # edges, ccw
   # hold shift to rotate scene fifteen degrees
   elif ks == 'Left':
      host.prev_edge()

   # edges, cw
   # hold shift to rotate scene fifteen degrees
   elif ks == 'Right':
      host.next_edge()

   # set active tile to tile across active edge
   # not detected on windows with numlock on
   elif ks.endswith('Insert'):

      tile = state['tile']

      edge = tile[state['edge']]

      newtile = edge.tile2 if edge.tile1 == tile else edge.tile1

      if newtile:
         host.activate_tile(newtile)

   # center view on active tile
   # hold shift to recenter canvas on the active tile
   elif ks == 'c':
      pass

   # exit program
   elif ks == 'Escape':
      f = host.exitfxn
      if callable(f):
         f()

   # (un)select active tile
   elif ks == 'space':
      state['tile'].select_toggle()

   # delete the tile across active edge,
   # shift deletes selected tiles
   elif ks == 'Delete':
      if shifty:
         host.do_delete_many()
      else:
         host.do_delete_single()

   # undo, hold shift to redo
   elif ks == 'BackSpace':
      pass

   # show help window
   elif ks in ('h', 'question', 'F1'):
      pass

   elif ks in ('plus', 'KP_Add'):
      state['tile'][state['edge']].highlight_toggle()

   # fill-in-the-blank debuging/test function, possibly ignored
   # center key on keypad, num lock needs to be off on windows
   elif ks in ('KP_Begin', 'Clear'):
      host.trythis(e.state)
