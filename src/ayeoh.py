
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
