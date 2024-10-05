# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TobysReturn.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\balloon.gif', '.'), ('.\\bark.wav', '.'), ('.\\blip_sound.wav', '.'), ('.\\buttercup.png', '.'), ('.\\chick.png', '.'), ('.\\elephant.png', '.'), ('.\\fish.png', '.'), ('.\\fox.png', '.'), ('.\\frog.png', '.'), ('.\\highscore.txt', '.'), ('.\\lion.png', '.'), ('.\\owl.png', '.'), ('.\\rabbit.png', '.'), ('.\\Toby.gif', '.'), ('.\\Toby001.gif', '.'), ('.\\turtle.png', '.'), ('.\\worm.png', '.'), ('.\\build\\buttercupsballoonadventure\\warn-buttercupsballoonadventure.txt', 'build\\buttercupsballoonadventure'), ('.\\build\\TobysReturn\\warn-TobysReturn.txt', 'build\\TobysReturn'), ('.\\dist\\highscore.txt', 'dist'), ('.\\Sounds\\blip_sound.wav', 'Sounds')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TobysReturn',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
