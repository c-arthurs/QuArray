# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['dab_analysis_application.py'],
             pathex=['/Users/callum/callum/dab/analysis_application/scripts', '/Users/callum/callum/dab/analysis_application'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='dab_analysis_application',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='dab_analysis_application.app',
             icon=None,
             bundle_identifier=None)
