# -*- mode: python -*-

block_cipher = None


a = Analysis(['MojeRachunki.py'],
             pathex=['/Users/lukasz/Desktop/Katalog/MojeRachunki'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MojeRachunki',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='MojeRachunki.app',
             icon=None,
             bundle_identifier=None)
