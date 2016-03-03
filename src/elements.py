
from collections import namedtuple

from math import copysign

sign = lambda x: int(copysign(1.0, x))

from options import *

_Point = namedtuple('Point', ( 'x',  'y'))
_Edge  = namedtuple( 'Edge', ('p1', 'p2'))

def scale_to_ints(pt):
   return (int(round(pt.x*2**FIXEDPT, 0)), int(round(pt.y*2**FIXEDPT, 0)))

def centroid(*pts):
   xs, ys = zip(*pts)
   return Point(sum(xs) / len(pts), sum(ys) / len(pts))

def scale_sort(p, q):

   px, py = scale_to_ints(p)
   qx, qy = scale_to_ints(q)

   return (
      ((qx, px) if qx < px else (px, qx)) +
      ((qy, py) if qy < py else (py, qy)) )

class Point(_Point):
   def __eq__(self, other):
      return scale_to_ints(self) == scale_to_ints(other)

# edge may be a plain pair of Points
def edge_print(e):
   return '%.1f,%.1f - %.1f,%.1f' % sum(e, ())

class Edge(_Edge):
   def __new__(cls, cvs, p1, p2, host):
      self = super(Edge, cls).__new__(cls, p1, p2)

      self.active = False
      self.highlighted = False

      self.tile1 = None
      self.tile2 = None

      self.host = host
      self.cvs = cvs

      self.id_ = cvs.create_line(*self, width=3, fill=EDGE, state='hidden')

      return self

   @staticmethod
   def signature(p1, p2):
      return frozenset(map(scale_to_ints, (p1, p2)))

   def update(self):
      active, highlighted = self.active, self.highlighted

      if not (active or highlighted):
         self.cvs.itemconfigure(self.id_, state='hidden')
         return

      fill = (HI_N_ACTIVE if highlighted else EDGE) if active else HILIGHT_USR

      self.cvs.itemconfigure(self.id_, fill=fill, state='normal')
      self.cvs.tag_raise(self.id_)

   def activate(self):
      self.host.status['ae'].update(edge_print(self))

      self.active = True
      self.update()

   def deactivate(self):
      self.active = False
      self.update()

   def highlight_toggle(self):
      self.highlighted = not self.highlighted
      self.update()

   def add_tile(self, tile):
      if not self.tile1:
         self.tile1 = tile
      else:
         if not self.tile2:
            self.tile2 = tile
         else:
            raise RuntimeError('Edge is full!')

   def remove_tile(self, tile):
      if self.tile1 == tile:
         self.tile1 = self.tile2
         self.tile2 = None
      else:
         if self.tile2 == tile:
            self.tile2 = None
         else:
            raise RuntimeError('Tile not found!')

      # only possible when both are None, and the edge is no longer used
      if self.tile1 == self.tile2:
         self.cvs.delete(self.id_)
         self.host.edge_cleanup(self)

   def what_side(self, pt):
      p1, p2 = self
      side   = (pt.x*p1.y) + (pt.y*p2.x) + (p1.x*p2.y) - (p1.y*p2.x) - (pt.y*p1.x) - (pt.x*p2.y)

      if abs(side) < EPS:
         side = 0.0

      return sign(side)

   # assumes edges are not duplicated (parallel edges that are colinear do not intersect)
   # returns true if edges intersect
   # other edge may be a plain pair of Points
   def intersect_check(self, other, debuggery):

      if debuggery:
         print 'DEBUGERRY BEGINS'
         print edge_print(self)
         print edge_print(other)

      host = self.host

      p1, p2 = self
      q1, q2 = other

      denom = p2.x - p1.x

      mp = None if abs(denom) < EPS else (p2.y-p1.y) / denom

      denom = q2.x - q1.x

      mq = None if abs(denom) < EPS else (q2.y-q1.y) / denom

      # if the edges share an endpoint, that's an okay intersection
      if p1 == q1 or p1 == q2 or p2 == q1 or p2 == q2:
         if debuggery:
            print 'early exit a'
            print 'DEBUGERRY ENDS'
         return False

      # both edges are vertical
      if mp is None and mq is None:
         if debuggery:
            print 'early exit b'
            print 'DEBUGERRY ENDS'
         return False

      # neither side is vertical, but they are parallel
      if not mp is None and not mq is None:
         if abs(mp - mq) < EPS:
            if debuggery:
               print 'early exit c'
               print 'DEBUGERRY ENDS'
            return False

      # the lines defined by each edge do intersect, but perhaps not on the edges
      # only one coordinate is necessary

      x = ( ( (p2.y*p1.x - p1.y*p2.x)*(q2.x - q1.x) + (q1.y*q2.x - q2.y*q1.x)*(p2.x - p1.x) ) /
          ( (p2.y - p1.y)*(q2.x - q1.x) + (q1.y - q2.y)*(p2.x - p1.x) ) )

      y = ( ( (p2.y*p1.x - p1.y*p2.x)*(q1.y - q2.y) + (q1.y*q2.x - q2.y*q1.x)*(p1.y - p2.y) ) /
          ( (p1.x - p2.x)*(q1.y - q2.y) + (q2.x - q1.x)*(p1.y - p2.y) ) )

      px = Point(x, y)
      if debuggery:
         print '%.1f,%.1f' % px

      p1x, p2x, p1y, p2y = scale_sort(p1, p2)
      q1x, q2x, q1y, q2y = scale_sort(q1, q2)

      x, y = scale_to_ints(px)

      if debuggery:
         print p1x, p1y, p2x, p2y
         print q1x, q1y, q2x, q2y
         print x, y

      if p1x <= x <= p2x and q1x <= x <= q2x and p1y <= y <= p2y and q1y <= y <= q2y:
         host.highlight_edges(self, other, px)
         if debuggery:
            print 'noncompliant intersection detected'
            print 'DEBUGERRY ENDS'
         return True

      if debuggery:
         print 'deemed okay'
         print 'DEBUGERRY ENDS'

      return False

class Tile(tuple):
   def __new__(cls, cvs, vertices, edges):
      self = super(Tile, cls).__new__(cls, edges)

      self.cvs = cvs
      self.group = None
      self.selected = False
      self.vertices = vertices

      for e in self:
         e.add_tile(self)

      self.id_ = cvs.create_polygon(*vertices, **{'fill':FILL, 'outline':EDGE})

      # scaled copy, to represent the cursor
      cx, cy = centroid(*vertices)

      csrvertices = [Point(CSR_SCL*(x-cx)+cx, CSR_SCL*(y-cy)+cy) for x,y in vertices]

      self.csrid = cvs.create_polygon(*csrvertices, **{'fill':CURSOR, 'state':'hidden'})

      return self

   def select_toggle(self):
      self.selected = not self.selected
      self.cvs.itemconfigure(self.id_, fill=SELECTED if self.selected else FILL)

   def activate(self):
      self.cvs.itemconfigure(self.csrid, state='normal')

   def deactivate(self):
      self.cvs.itemconfigure(self.csrid, state='hidden')

   def delete(self):
      self.cvs.delete(self.csrid)
      self.cvs.delete(self.id_)

      for e in self:
         e.remove_tile(self)

__all__  = ('Point', 'Edge', 'Tile', 'centroid', 'edge_print')
