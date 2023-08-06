"""Shortcut to set the path.

This module provides the following shortcut to set the path:

    import mmf_setup.set_path_

which is equivalent to:

    import mmf_setup; mmf_setup.set_path()

The latter is generally preferred.
"""
from .set_path import set_path

set_path()
