# -*- mode: python -*-

block_cipher = None


a = Analysis(['ParseExcel.py'],
             pathex=['/Users/lujiji/WorkPlace/Python/workplace/untitled'],
             binaries=None,
             datas=None,
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
          name='ParseExcel',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='ParseExcel.app',
             icon=None,
             bundle_identifier=None)
