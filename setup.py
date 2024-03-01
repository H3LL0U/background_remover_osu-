from cx_Freeze import setup, Executable

build_options = {'packages':[], 'excludes':[]}
import sys
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base)
]

setup(name = 'Osu! background remover', version = '1.6.0' , description = 'Simple app to remove and set backgrounds in osu!',
      options = {'build_exe':build_options},
      executables = executables
      )