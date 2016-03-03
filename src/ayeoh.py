
from elements import Point

import struct

from collections import namedtuple

EdgeIn = namedtuple('EdgeIn', ('ax', 'ay', 'bx', 'by'))

def raw2hex(s):
   return ''.join(['%02x' % (ord(c),) for c in s])

def edge2hex(e):
   return raw2hex(struct.pack('<4f', e[0][0], e[0][1], e[1][0], e[1][1]))

def tile2hex(t):
   return ''.join(map(edge2hex, t))


def hex2raw(s):
   return ''.join([chr(int(s[2*i:2*(i+1)], 16)) for i in range(len(s)/2)])

def raw2nums(s):
   return struct.unpack('<%df' % (len(s)/4,), s)

def nums2edges(nums):
   edgesin = [EdgeIn(*nums[4*i:4*(i+1)]) for i in range(len(nums)/4)]
   return [(Point(ei.ax, ei.ay), Point(ei.bx, ei.by)) for ei in edgesin]

# actually returns the "rawedges", pairs of points that take a bit of preprocessing
# this matches the other tile creation interfaces, naturally.
def hex2tile(s):
   return nums2edges(raw2nums(hex2raw(s)))

__all__ = ('tile2hex', 'hex2tile')
