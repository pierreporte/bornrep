from cx_Freeze import setup, Executable
import PIL._tkinter_finder

# Dependencies are automatically detected, but it might need
# fine tuning.
buildop_packaages = [
    "pyx.attr",
    "pyx.box",
    "pyx.bitmap",
    "pyx.connector",
    "pyx.svgfile",
    "pyx.mesh",
    "pyx.pattern",
    "pyx.pdfextra",
    "PIL._tkinter_finder"
]
buildOptions = dict(packages = buildop_packaages, excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('bornrep.py', base=base)
]

setup(name='Bornographe',
      version = '0.1',
      description = 'Traceur de repères',
      options = dict(build_exe = buildOptions),
      executables = executables)
