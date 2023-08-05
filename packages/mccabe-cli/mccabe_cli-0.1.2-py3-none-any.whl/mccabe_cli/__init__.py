__version__ = '0.1.2'

import sys


def show_help():
    """
    Usage:

    $ mccabe --min 5 mccabe.py

    ("185:1: 'PathGraphingAstVisitor.visitIf'", 5)
    ("71:1: 'PathGraph.to_dot'", 5)
    ("245:1: 'McCabeChecker.run'", 5)
    ("283:1: 'main'", 7)
    ("203:1: 'PathGraphingAstVisitor.visitTryExcept'", 5)
    ("257:1: 'get_code_complexity'", 5)
    """
    # print the docstring of this function, unindented, with textwrap
    # print(show_help.__doc__)
    from textwrap import dedent

    print(dedent(show_help.__doc__).strip())  # type: ignore


def main() -> None:
    from mccabe import main as mccabe_main

    try:
        mccabe_main(sys.argv[1:])
    except:
        show_help()
