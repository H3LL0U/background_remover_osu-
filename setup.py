from cx_Freeze import setup, Executable

build_options = {'packages':[], 'excludes':[]}
import sys
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base)
]

setup(name = 'Osu! background remover', version = '1.1' , description = 'with this program you can delete and save all the unwanted osu! backgrounds from all the osu! folders. And restore them if you want to get them back',
      options = {'build_exe':build_options},
      executables = executables
      )