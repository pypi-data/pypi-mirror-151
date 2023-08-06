"""Initialize a CoCalc Project."""

from functools import partial
from optparse import OptionParser
from pathlib import Path

import mmf_setup

from . import tools, mmf_initial_setup

__all__ = ["run", "main", "add_options"]


_bash_aliases_contents = """
if [ -f "{home_dir}/.bashrc_aliases_mmf-setup" ]; then
    . "{home_dir}/.bashrc_aliases_mmf-setup"
fi
""".strip()


def run(options, args):
    breakpoint()
    do_ = partial(tools.do, options=options)
    do_os_ = partial(tools.do_os, options=options)
    # hg = tools.execute("type -p hg", verbose=options.verbose)
    print("# Installing mercurial, hg-evolve, hg-git, jupytext for python3...")
    do_os_(
        [
            "python3 -m pip install --upgrade --user pip mercurial hg-evolve hg-git jupytex"
        ]
    )
    print("# Installing poetry...")
    do_os_(
        [
            "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -"
        ]
    )

    data_dir = Path(mmf_setup.DATA) / "config_files" / "cocalc"

    print("# Setting up config files for CoCalc...")
    _bashrc = Path("~/.bashrc").expanduser()
    if _bashrc.exists() and not _bashrc.is_symlink():
        do_(["os.rename('~/.bashrc', '~/.bashrc_cocalc')"])
    mmf_initial_setup.run(options, args=[str(data_dir)])

    _bash_aliases = Path("~/.bash_aliases").expanduser()
    if not _bash_aliases.exists():
        do_os_("touch {_bash_aliases}")

    if options.home_dir not in set(["~", "${HOME}", "$HOME"]):
        options.home_dir = Path(options.home_dir).expanduser().absolute()

    tools.insert_unique(
        _bash_aliases,
        contents=_bash_aliases_contents.format(home_dir=options.home_dir),
        options=options,
    )

    with open(data_dir / "message.txt") as f:
        print(f.read())


def add_options(parser):
    """Add arguments to the option parser and return the updated parser."""
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
