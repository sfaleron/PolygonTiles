
from math import sin, cos, pi

from elements import *
from options  import *

CX, CY = CVS_WIDTH/2, CVS_HEIGHT/2

def do_start_tile(shape):
   if shape == 'q':
      r  = TILE_SIDE * 2**.5 / 2
      n  = 4
      da = pi/4
   else:
      r  = TILE_SIDE / 3**.5
      n  = 3
      da = pi/2

   return [Point(r*cos(a)+CX, r*sin(a)+CY) for a in [2*pi/n*i-da for i in range(n)]]

# the principle used is the same for both shapes: perpendicular lines are extended some distance.
# for the square, one from each end; for the triangle, one from the midpoint.

def extend_line(pt, m, dsq):
   sols = {}

   if m is None:
      sols[ 1] = Point(pt.x, pt.y + dsq**.5)
      sols[-1] = Point(pt.x, pt.y - dsq**.5)

   else:
      tmp  = (dsq / (1+m**2))**.5

      x = pt.x + tmp

      y = m*(x - pt.x) + pt.y

      sols[ 1] = Point(x, y)

      x = pt.x - tmp

      y = m*(x - pt.x) + pt.y

      sols[-1] = Point(x, y)

   return sols

def make_tile(tile, edge, shape):
   p1, p2 = edge

   other = (set(tile.vertices) - set(edge)).pop()

   parent_side = edge.what_side(other)

   # note the slope computed is for the perpendicular

   denom = p1.y - p2.y

   m = None if abs(denom) < EPS else (p2.x-p1.x) / denom

   if shape == 'q':
      sols3 = extend_line(p2, m, TILE_SIDE**2)

      if edge.what_side(sols3[1]) != parent_side:
         p3 = sols3[ 1]
      else:
         p3 = sols3[-1]

      p4 = Point(p1.x+p3.x-p2.x, p1.y+p3.y-p2.y)

      return (p4, p3, p2, p1)

   else:
      sols3 = extend_line(centroid(p1, p2), m, .75*TILE_SIDE**2)

      p3    = sols3[1] if edge.what_side(sols3[1]) != parent_side else sols3[-1]

      return (p3, p2, p1)
