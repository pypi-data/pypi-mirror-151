"""Tools to help with the command-line scripts."""
import os
from pathlib import Path
import subprocess
import sys

__all__ = [
    "yes_no",
    "backup",
    "do",
    "do_os",
    "add_options",
    "check_access",
    "insert_unique",
]


def yes_no(default=""):
    """This function prompts the user for a yes or no answer and will
    accept a default response.  Exceptions (such as EOF) are not
    caught.  The result is True for 'yes' and False for 'no'."""

    def validate(ans):
        ans = ans.lower()
        yes = ["y", "yes"]
        no = ["n", "no"]
        try:
            yes.index(ans)
            return True
        except:
            pass
        try:
            no.index(ans)
            return False
        except:
            pass
        return None

    def input_default(prompt, default):
        response = input(prompt)
        if 0 == len(response):
            response = default
        return response

    prompts = {None: "yes/no? ", True: "Yes/no? ", False: "yes/No? "}
    prompt = prompts[validate(default)]

    ans = validate(input_default(prompt, default))
    while ans is None:
        print('Please answer "yes" or "no".')
        ans = validate(input_default(prompt, default))
    return ans


def is_not_temp(f):
    """Return True if the file is not a temporary file (no '#' or '~')."""
    return ("#" not in f) and ("~" not in f)


def backup(file, options):
    """Backup a file and return backup name."""
    bak = ".".join([file, "bak"])
    n = 0
    while os.path.isfile(bak):
        n = n + 1
        bak = "%s.bak%i" % (file, n)

    cmds = ["os.rename('%s', '%s')" % (file, bak)]
    if do(cmds, options=options):
        return bak
    else:
        raise Exception("Could not backup %s to %s." % (file, bak))


def execute(command, cwd=None, shell=False, verbose=True):
    """Return the output of the specified command at the os level.

    Arguments
    ---------
    command : [str], str
        Command to execute.  This should generally be a list of strings, but if it is a
        string, then we will execute `command.split()`.

    Returns
    -------
    output : str, None
        Decoded string of output, or None if command failed.
    """
    if isinstance(command, str):
        command_ = command.split()
    else:
        command_ = command

    try:
        output = (
            subprocess.check_output(command_, shell=shell, cwd=cwd).strip().decode()
        )
    except subprocess.CalledProcessError as e:
        output = None
        if verbose:
            print(f"Execution failed: {e}", file=sys.stderr)
            if e.returncode < 0:
                print(
                    f"Child was terminated by signal {-e.returncode}", file=sys.stderr
                )
            else:
                print(f"Child returned {e.returncode}", file=sys.stderr)
    return output


def do_os(cmds, options, mesg=None, query=None):
    """Execute a command after first confirming with the user and
    presenting information (if verbose options are selected).

    Return False if there was an error.
    """
    success = True
    if options.verbose and mesg is not None:
        print(mesg)
    if options.action:
        perform = True
        if options.interactive:
            if query is None:
                print("Perform the following commands?")
                for c in cmds:
                    print(c)
            else:
                print(query)
            perform = yes_no("yes")
        if perform:
            for c in cmds:
                if options.verbose:
                    print(c)
                output = execute(c)
                if output is None:
                    print(f"Command {c} failed", file=sys.stderr)
                    success = False
    else:
        for c in cmds:
            print(c)
    return success


def do(cmds, options, mesg=None, query=None):
    """Execute a command after first confirming with the user and
    presenting information (if verbose options are selected).

    Return False if there was an error.
    """
    success = True
    if options.verbose and mesg is not None:
        print(mesg)
    if options.action:
        perform = True
        if options.interactive:
            if query is None:
                print("Perform the following commands?")
                for c in cmds:
                    print(c)
            else:
                print(query)
            perform = yes_no("yes")
        if perform:
            for c in cmds:
                if options.verbose:
                    print(c)
                try:
                    exec(c)
                except Exception as e:
                    print("Command {} failed: {}".format(c, e), file=sys.stderr)
                    success = False
    else:
        for c in cmds:
            print(c)
    return success


def os_do(action, options):
    if options.action:
        perform = True
        if options.interactive:
            print("Perform the following action?")
            print(action)
            perform = yes_no("yes")
        if perform:
            execute(action, shell=True)
    else:
        print(action)


class AttributeError(Exception):
    pass


def insert_unique(filename, contents, options, padding=["\n", ""]):
    """Inserts `contents` into file `filename` if it does not exist."""
    path = Path(filename).expanduser()
    if path.exists():
        with open(path) as _f:
            contains_contents = contents in _f.read()
        if not contains_contents:
            padded_contents = padding[0] + contents + padding[1]
            do(
                [f"with open({str(path)!r}, 'a') as f: f.write({padded_contents!r})"],
                options=options,
            )


def check_access(path, mode):
    """Check that path has proper access as specified by mode.

    Throws an AttributeError on failure
    """
    if not os.access(path, mode):
        err = "Path " + path + " has invalid permissions:"
        tests = [
            (os.F_OK, "exist"),
            (os.R_OK, "be readable"),
            (os.W_OK, "be writable"),
            (os.X_OK, "be executable"),
        ]
        for (test_mode, msg) in tests:
            if (mode & test_mode) and not os.access(path, test_mode):
                err = err + "\n- Path must " + msg
                raise AttributeError(err)
    else:
        return


def add_options(parser):
    """Add arguments to the option parser and return the updated parser."""
    parser.add_option(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="print lots of information",
    )
    parser.add_option(
        "-i",
        "--interactive",
        action="store_true",
        dest="interactive",
        default=False,
        help="prompt before taking action",
    )
    parser.add_option(
        "-n",
        "--no-action",
        action="store_false",
        dest="action",
        default=True,
        help=("don't do anything:" + "only print commands that would be executed"),
    )
    return parser
