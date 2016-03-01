
from collections import namedtuple

from math import copysign

sign = lambda x: int(copysign(1.0, x))

from options import *

_Point = namedtuple('Point', ( 'x',  'y'))
_Edge  = namedtuple( 'Edge', ('p1', 'p2'))

def scale_to_ints(pt):
   return (int(round(pt.x*2**20, 0)), int(round(pt.y*2**20, 0)))

def centroid(*pts):
   xs, ys = zip(*pts)
   return Point(sum(xs) / len(pts), sum(ys) / len(pts))


class Point(_Point):
   def __eq__(self, other):
      return scale_to_ints(self) == scale_to_ints(other)

class Edge(_Edge):
   def __new__(cls, cvs, p1, p2, cleanup=None):
      self = super(Edge, cls).__new__(cls, p1, p2)

      self.cleanup = cleanup

      self.tile1 = None
      self.tile2 = None
      self.cvs = cvs

      self.id_ = cvs.create_line(*self, width=3, fill=EDGE, state='hidden')

      return self

   @staticmethod
   def signature(p1, p2):
      return frozenset(map(scale_to_ints, (p1, p2)))

   def activate(self):
      self.cvs.itemconfigure(self.id_, state='normal')
      self.cvs.tag_raise(self.id_)

   def deactivate(self):
      self.cvs.itemconfigure(self.id_, state='hidden')

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
         self.deactivate()
         f = self.cleanup
         if callable(f):
            f(self)

   def what_side(self, pt):
      p1, p2 = self
      side   = (pt.x*p1.y) + (pt.y*p2.x) + (p1.x*p2.y) - (p1.y*p2.x) - (pt.y*p1.x) - (pt.x*p2.y)

      if abs(side) < EPS:
         side = 0.0

      return sign(side)

   # assumes edges are not duplicated (parallel edges that are colinear do not intersect)
   # returns true if edges intersect
   def intersect_check(self, other):
      p1, p2 = self
      q1, q2 = other

      if p2.x < p1.x:
         p1, p2 = p2, p1

      if q2.x < q1.x:
         q1, q2 = q2, q1

      denom = p2.x - p1.x

      mp = None if abs(denom) < EPS else (p2.y-p1.y) / denom

      denom = q2.x - q1.x

      mq = None if abs(denom) < EPS else (q2.y-q1.y) / denom

      # if the edges share an endpoint, that's an okay intersection
      if p1 == q1 or p1 == q2 or p2 == q1 or p2 == q2:
         return False

      # both edges are vertical
      if mp is None and mq is None:
         return False

      # neither side is vertical, but they are parallel
      if not mp is None and not mq is None:
         if abs(mp - mq) < EPS:
            return False

      # the lines defined by each edge do intersect, but perhaps not on the edges
      # only one coordinate is necessary

      x = ( ( (p2.y*p1.x - p1.y*p2.x)*(q2.x - q1.x) + (q1.y*q2.x - q2.y*q1.x)*(p2.x - p1.x) ) /
          ( (p2.y - p1.y)*(q2.x - q1.x) + (q1.y - q2.y)*(p2.x - p1.x) ) )

      #y = ( ( (p2.y*p1.x - p1.y*p2.x)*(q1.y - q2.y) + (q1.y*q2.x - q2.y*q1.x)*(p1.y - p2.y) ) /
      #    ( (p1.x - p2.x)*(q1.y - q2.y) + (q2.x - q1.x)*(p1.y - p2.y) ) )

      if p1.x < x < p2.x and q1.x < x < q2.x:
         return True

      return False

class Tile(tuple):
   def __new__(cls, cvs, pts, edges):
      self = super(Tile, cls).__new__(cls, edges)

      self.cvs = cvs
      self.group = None
      self.selected = False
      self.pts = set(pts)

      for e in self:
         e.add_tile(self)

      self.id_ = cvs.create_polygon(*pts, **{'fill':FILL, 'outline':EDGE})

      # scaled copy, to represent the cursor
      cx, cy = centroid(*pts)

      csrpts = [Point(CSR_SCL*(x-cx)+cx, CSR_SCL*(y-cy)+cy) for x,y in pts]

      self.csrid = cvs.create_polygon(*csrpts, **{'fill':CURSOR, 'state':'hidden'})

      return self

   def activate(self):
      self.cvs.itemconfigure(self.csrid, state='normal')

   def deactivate(self):
      self.cvs.itemconfigure(self.csrid, state='hidden')

   def delete(self):
      self.cvs.delete(self.csrid)
      self.cvs.delete(self.id_)

      for e in self:
         e.remove_tile(self)

__all__  = ('Point', 'Edge', 'Tile', 'centroid')
