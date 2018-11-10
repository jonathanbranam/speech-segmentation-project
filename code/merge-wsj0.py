#!/usr/bin/env python3
# merge-wsj0.py
# Merge the wsj0 disk download directories
# By Jonathan Branam
# Indiana University
# ENG-R 511 Fall 2018

"""Merge the different WSJ0 folders into a single directory

Usage:
    merge-wsj0.py [-d] [-l LIMIT] SOURCE DEST

Options:
    -d, --debug                   # output extra debug information
    -l LIMIT, --limit=LIMIT       # only process LIMIT files (for debugging)

Examples:
    ./merge-wsj0.py -d csr_1 wsj0-merged

    # Test run over 10 files
    ./merge-wsj0.py -d csr_1 wsj0-merged -l 10
"""

from docopt import docopt
from pathlib import Path

defaults = {
    '--debug': False,
    '--limit': None,
}

def merge(source, dest):
    print(f"Merge wsj0 from {source} to {dest}.")


def main(args):
    source = Path(args['SOURCE'])
    dest = Path(args['DEST'])

    if not source.is_dir():
        print(f"Source directory {source} doesn't exist.")
        return 1
    dest.mkdir(parents=True, exist_ok=True)
    return merge(source, dest)

if __name__ == "__main__":
    arguments = docopt(__doc__)

    # Drop arguments that are None
    arguments = {key:val for key, val in arguments.items() if val is not None}
    # merge dictionaries
    arguments = {**defaults, **arguments}

    exit(main(arguments))
