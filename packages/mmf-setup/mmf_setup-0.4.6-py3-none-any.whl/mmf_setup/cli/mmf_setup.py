"""Setup environment.

Use this in your initialization files as:

     eval "$(mmf_setup [options])"

The `--cocalc` option can be used to run a set of initializations on cocalc.
"""

from functools import partial
from optparse import OptionParser
from os.path import exists

import mmf_setup

from . import tools, mmf_initial_setup

__all__ = ["run", "main", "add_options"]

# List of (variable, value, filename)
# Will print a statement like the following iff filename is None or exists:
#
#    export variable=value
#
VARIABLES = [
    ("MMF_SETUP", mmf_setup.MMF_SETUP, mmf_setup.MMF_SETUP),
]


def get_HGRCPATH(full_hg=False):
    """Return the HGRCPATH.

    Arguments
    ---------
    full_hg : bool
       If True, then include the potentially dangerous HGRC_FULL file which includes the
       update hook.
    """
    paths = [mmf_setup.HGRC_FULL if full_hg else mmf_setup.HGRC_LGA]
    paths = [path for path in paths if exists(path)]
    paths.insert(0, "${HGRCPATH:-~/.hgrc}")
    return ":".join(paths)


def run(options, args):
    debug = options.debug
    full_hg = options.full_hg
    global VARIABLES
    vars = list(VARIABLES)
    vars.append(("HGRCPATH", get_HGRCPATH(full_hg=full_hg), None))
    env = []

    for var, value, filename in vars:
        if not filename or exists(filename):
            env.append('export {var}="{value}"'.format(var=var, value=value))
        elif debug:
            print(
                "# processing {}={} failed:\n   no file '{}'".format(
                    var, value, filename
                )
            )

    print("\n".join(env))


def add_options(parser):
    """Add arguments to the option parser and return the updated parser."""
    parser.add_option(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
        default=False,
        help="debug missing files",
    )

    parser.add_option(
        "-H",
        "--hg",
        action="store_true",
        dest="full_hg",
        default=False,
        help="""Include hgrc.full in HGRCPATH with a complete set of mercurial options
    including: the evolve extension with topics enabled, the hggit extension so you can
    clone from git, and an update hook to include project-specific .hgrc file to .hg/hgrc.
    (Note: this is a POTENTIAL SECURITY RISK.  Make sure you inspect the .hgrc file
    before running further mercurial commands.)""",
    )
    return parser


def main():
    usage = """usage: %prog [options]"""
    parser = OptionParser(
        usage=usage,
        description=__doc__.splitlines()[0],
        epilog="\n".join(__doc__.splitlines()[2:]),
    )

    parser = add_options(parser)
    parser = mmf_initial_setup.add_options(parser)
    parser = tools.add_options(parser)

    (options, args) = parser.parse_args()
    run(options=options, args=args)


if __name__ == "__main__":
    main()
