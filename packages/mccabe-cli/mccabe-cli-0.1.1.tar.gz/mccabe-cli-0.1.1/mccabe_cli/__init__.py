__version__ = '0.1.1'

import sys


def main() -> None:
    from mccabe import main as mccabe_main

    mccabe_main(sys.argv[1:])
