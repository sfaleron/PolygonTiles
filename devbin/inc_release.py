
# to restore the previous release specification, simply checkout lib/release
# from the git repository.

# the release specification is logged when the program launches, so these
# details can help with troubleshooting. If you make significant changes
# to the code and release the result, others will be able to track down any
# problems much more effectively by referencing this.
TAG = 'by sfaleron'

import os.path as osp

from time import strftime, localtime, time

fn = osp.join(osp.dirname(__file__), '..', 'lib', 'release')

with open(fn, 'rb') as f:
   n = int(f.read().rstrip().split()[0]) + 1

spec = '%d %s %s' % (n, strftime('%Y%m%d', localtime(time())), TAG)

print 'new release specification:'
print spec

with open(fn, 'wb') as f:
   f.write(spec+'\n')
