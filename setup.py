from cx_Freeze import setup, Executable

build_options = {'packages':[], 'excludes':[]}
import sys
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base)
]

setup(name = 'Osu! background remover', version = '1' , description = 'with this program you can delete all the unwanted osu! backgrounds from all the osu! folders',
      options = {'build_exe':build_options},
      executables = executables
      )