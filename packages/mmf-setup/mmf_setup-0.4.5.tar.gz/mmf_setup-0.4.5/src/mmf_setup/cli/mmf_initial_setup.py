"""Creates symlinks to files in the specified config directories (default "./").

Run from the desired config directory, and files with a second line like

  "dest = ~/.bashrc"

will be symlinked to the specified location.  If a file
already exists, it will be backed up (copied to a file with a .bak extension).
Existing symlinks will be overwritten.
"""
from functools import partial
import os.path
import re
import sys
from optparse import OptionParser

from . import tools

__all__ = ["run", "main"]

# These are directories that should be ignored -- mainly includes
# version control information.
_IGNORE_DIRS = ["CVS", ".svn", ".hg"]

#############
# Script Body
def run(options, args):
    do_ = partial(tools.do, options=options)
    # Setup directories
    home_dir = os.path.expanduser(options.home_dir)
    tools.check_access(home_dir, os.F_OK | os.R_OK | os.W_OK | os.X_OK)
    if options.verbose:
        print("Using <home> = {}".format(home_dir))

    if not args:
        args = ["."]

    for src_dir in args:
        src_dir = os.path.expanduser(src_dir)
        if "." == src_dir or ".." in src_dir:
            src_dir = os.path.abspath(src_dir)
        if not os.path.isabs(src_dir):
            src_dir = os.path.abspath(src_dir)
        tools.check_access(src_dir, os.F_OK | os.R_OK)

        if options.verbose:
            print("Using dir = {}".format(src_dir))

        # Get all files in src_dir directory
        for (root, dirs, files) in os.walk(src_dir):
            dirs = set(dirs)
            dirs.difference_update(_IGNORE_DIRS)

            files = filter(tools.is_not_temp, files)
            sys_home = os.path.expanduser("~")

            for f in sorted(files):
                src = os.path.join(root, f)

                # Files are linked when the second line of the file
                # looks like "# dest=~/.xsession" with optional whitespace
                try:
                    with open(src, "r") as fd:
                        fd.readline()
                        dest = re.match(
                            r"\A\s*[#;\\]*\s*dest\s*=\s*(\S*)", fd.readline()
                        )
                except Exception:
                    dest = None

                if dest is None:
                    print(
                        f"Warning: No dest = 2nd line in file '{src}'... ignoring",
                        file=sys.stderr,
                    )
                    continue

                dest = os.path.expanduser(dest.group(1))
                if dest.startswith(sys_home):
                    # Replace with new home.

                    dest = os.path.join(home_dir, dest[len(sys_home + os.sep) :])

                dest_dir = os.path.dirname(dest)
                if options.abspath:
                    ln_src = os.path.abspath(src)
                else:
                    ln_src = os.path.relpath(
                        os.path.realpath(src), os.path.realpath(dest_dir)
                    )

                if not os.path.exists(dest_dir):
                    mesg = "Directory %s does not exist." % (dest_dir,)
                    query = "Create %s ?" % (dest_dir,)
                    cmds = ["os.makedirs('%s')" % (dest_dir,)]
                    do_(cmds, mesg=mesg, query=query)
                if os.path.islink(dest):
                    mesg = "Symlink %s exists." % (dest,)
                    query = "Remove and replace with link to %s?" % (ln_src,)
                    cmds = [
                        "os.remove('%s')" % (dest,),
                        "os.symlink('%s', '%s')" % (ln_src, dest),
                    ]
                    do_(cmds, mesg=mesg, query=query)
                elif os.path.isfile(dest):
                    mesg = "File %s exists." % (dest,)
                    query = "Backup and symlink '%s' -> '%s'?" % (ln_src, dest)
                    cmds = [
                        "backup('%s')" % (dest,),
                        "os.symlink('%s', '%s')" % (ln_src, dest),
                    ]
                    do_(cmds, mesg=mesg, query=query)
                else:
                    query = "Link %s to %s?" % (ln_src, dest)
                    cmds = ["os.symlink('%s', '%s')" % (ln_src, dest)]
                    do_(cmds, query=query)


def add_options(parser):
    """Add arguments to the option parser and return the updated parser."""
    parser.add_option(
        "--home",
        type="string",
        dest="home_dir",
        default="~",
        help=(
            "use <home> rather than ~ for installation."
            + "(Used to replace '~' in dest strings.)"
        ),
        metavar="<home>",
    )

    parser.add_option(
        "-a",
        "--abs-path",
        action="store_true",
        dest="abspath",
        default=False,
        help="Use absolute symlinks (defaults are relative to ~)",
    )
    return parser


def main():
    usage = "Usage: %prog [options] dir1 dir2 ..."
    parser = OptionParser(
        usage=usage,
        description=__doc__.splitlines()[0],
        epilog="\n".join(__doc__.splitlines()[2:]),
    )

    parser = add_options(parser)
    parser = tools.add_options(parser)

    # Parse arguments
    (options, args) = parser.parse_args()
    run(options=options, args=args)


if __name__ == "__main__":
    main()
