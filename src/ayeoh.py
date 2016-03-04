
from elements import Point

import struct

def raw2hex(s):
   return ''.join(['%02x' % (ord(c),) for c in s])

def hex2raw(s):
   return ''.join([chr(int(s[2*i:2*(i+1)], 16)) for i in range(len(s)/2)])


def tile2hex(t):
   return raw2hex(struct.pack('<%df' %(2*len(t),), *sum(t.vertices, ())))

def hex2vertices(s):
   nums = struct.unpack('<%df' % (len(s)/8,), hex2raw(s))
   return [Point(*nums[2*i:2*(i+1)]) for i in range(len(nums)/2)]


def readfile(fd, cb):
   for ln in fd:
      s = ln.rstrip()

      if not s:
         continue

      if s.startswith('#'):
         continue

      id_, args = s.split(' ', 1)

      if id_ == 't':
         cb('t', hex2vertices(s[2:]))


def writefile(fd, items):
   for id_, args in items:
      if id_ == 't':
         fd.write('t %s\n' % (tile2hex(args),))


__all__ = ('writefile', 'readfile')
