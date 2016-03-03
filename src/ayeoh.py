
from elements import Point

import struct

def raw2hex(s):
   return ''.join(['%02x' % (ord(c),) for c in s])

def pt2hex(pt):
   return raw2hex(struct.pack('<2f', *pt))

def tile2hex(t):
   return ''.join(map(pt2hex, t.vertices))


def hex2raw(s):
   return ''.join([chr(int(s[2*i:2*(i+1)], 16)) for i in range(len(s)/2)])

def raw2pts(s):
   nums = struct.unpack('<%df' % (len(s)/4,), s)
   return [Point(*nums[2*i:2*(i+1)]) for i in range(len(nums)/2)]

# actually returns the vertices
# this matches the other tile creation interfaces, naturally.
def hex2vertices(s):
   return raw2pts(hex2raw(s))

__all__ = ('tile2hex', 'hex2vertices')
