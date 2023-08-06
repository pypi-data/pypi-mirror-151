import importlib

mmf_setup = importlib.import_module(__package__)

mmf_setup.nbinit_count = 1 + getattr(mmf_setup, "nbinit_count", 0)

print(f"hello {mmf_setup.nbinit_count}")

from .notebook_configuration import nbinit

mmf_setup.nbinit = "Hello"


def load_ipython_extension(ipython):
    print("mmf_setup.nbinit extension loaded")
    ns = {}

    # Add various imports to the user namespace
    ipython.user_ns.update(ns)

    # If we add variables here, they will not show up with %who
    # ipython.user_ns_hdden.update(ns)


def unload_ipython_extension(ipython):
    print("mmf_setup.nbinit extension unloaded")
