"""Tools for working with ipython and jupyter."""
from . import nbinit

from IPython.core import magic_arguments
from IPython.core.magics.pylab import magic_gui_arg
from IPython.core.magic import Magics, magics_class, line_magic


__all__ = [
    "nbinit",
    "load_ipython_extension",
    "unload_ipython_extension",
    "register_magics",
]


@magics_class
class MMFMagics(Magics):
    """Magics related to mmf_setup."""

    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "-l",
        "--list",
        action="store_true",
        help="Show available matplotlib backends",
    )
    @magic_gui_arg
    def nbinit(self, line=""):
        """Initialize jupyter notebook with MathJaX etc."""

        args = magic_arguments.parse_argstring(self.nbinit, line)

        self.shell.magic(f"matplotlib {args.gui}")


def register_magics(ip=None):
    if ip is None:
        ip = get_ipython()
    ip.register_magics(MMFMagics)


def load_ipython_extension(ipython):
    print("mmf_setup extension loaded")
    ns = {}

    # Add various imports to the user namespace
    ipython.user_ns.update(ns)

    # If we add variables here, they will not show up with %who
    ipython.user_ns_hdden.update(ns)


def unload_ipython_extension(ipython):
    print("mmf_setup extension unloaded")
