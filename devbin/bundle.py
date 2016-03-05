
import os.path as osp
import subprocess
import zipfile
import os

if os.name != 'nt':
   print "Bundling probably isn't even necessary/useful on this system, but"
   print "we'll try it your way. It's your fault if it blows up, though!"
   print 'Resuming after a short delay..'
   import time
   time.sleep(2)

os.chdir(osp.join(osp.dirname(__file__), '..'))

if not osp.exists('bundles'):
   os.mkdir('bundles')

fn = osp.join(osp.dirname(__file__), '..', 'lib', 'release')

with open(fn, 'rb') as f:
   n = int(f.read().rstrip().split()[0])

base  = osp.join('bundles', 'PolygonTiles_r' + str(n))
logfn = base + '.log'
zipfn = base + '.zip'

if osp.exists(zipfn):
   print 'Bundle %s exists. If replacement is desired, you must remove it.' % (zipfn,)
   raise SystemExit(1)

print 'calling pyinstaller. output is saved to: ' + logfn

with open(logfn, 'w') as f:
   subprocess.check_call(['pyinstaller', '--noconfirm', 'bundle.spec'], stderr=f)

print 'pyinstaller complete'

print 'tidying up..'

src = osp.join('dist', 'polytiles')

print 'hiding the mess..'

okfiles = set(['LICENSE', 'README.rst'])

os.mkdir(osp.join(src, 'messy'))

for file_ in os.listdir(src):
   path = osp.join(src, file_)
   if osp.isdir(path):
      continue
   if file_ in okfiles:
      continue

   os.rename(path, osp.join(src, 'messy', file_))

os.rename(osp.join(src, 'tcl'), osp.join(src, 'messy', 'tcl'))
os.rename(osp.join(src, 'tk'), osp.join(src, 'messy', 'tk'))

print 'mess hidden'

print 'cleanup complete'

# no messages, as it's safe and fast
with open(osp.join(src, 'polytiles.bat'), 'w') as f:
   f.write('@echo off\n')
   f.write('cd %~dp0\n')
   f.write('messy\\pgt_exec.exe\n')

print 'creating zipfile..'

zipfd = zipfile.ZipFile(zipfn, 'w')

for path, dirs, files in os.walk(src):
   for fn in files:
      pn = osp.join(path, fn)
      zipfd.write(pn, osp.relpath(pn, 'dist'))

zipfd.close()

print 'zipfile complete'

print "that's all! enjoy!"
