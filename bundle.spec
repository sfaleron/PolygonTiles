# -*- mode: python -*-

import os.path as osp

xtrafiles = sum([[(osp.join(d, f), d) for f in files] for d, files in (
   ('.',   ('LICENSE', 'README.rst')),
   ('lib', ('options.cfg', 'release')),
   ('doc', ('interface.txt', 'overview.txt', 'intersect.txt', 'unbundle.txt', 'rst.txt')) ) ], [])

block_cipher = None


a = Analysis(['polytiles.pyw'],
             pathex=['C:\\work\\python\\PolygonTiles'],
             binaries=None,
             datas=xtrafiles,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pgt_exec',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='polytiles')
