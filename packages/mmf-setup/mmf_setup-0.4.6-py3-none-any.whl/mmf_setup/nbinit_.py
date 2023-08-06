"""Initialize notebooks.

This module is intended to provide a shortcut at the start of notebooks to initialize
them.  I.e. the first cell can be simply:

    import mmf_setup.nbinit

This essentially does the following:

    import os.path, mmf_setup
    _ROOT = mmf_setup.set_path()
    _nbinit_file = os.path.join(_ROOT, 'nbinit.py')
    if os.path.exists(_nbinit_file):
        with open(_nbinit_file, "r") as _f:
            exec(f.read())
    else:
        mmf_setup.nbinit()
"""
import os.path

from .set_path import set_path
from .notebook_configuration import nbinit


def run(filename="nbinit.py"):
    ROOT = set_path()
    nbinit_file = os.path.join(ROOT, "nbinit.py")
    if os.path.exists(nbinit_file):
        with open(nbinit_file, "r") as f:
            exec(f.read())
    else:
        nbinit()


run()
