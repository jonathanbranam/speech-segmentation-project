#!/usr/bin/env python3
# merge-wsj0.py
# Merge the wsj0 disk download directories
# By Jonathan Branam
# Indiana University
# ENG-R 511 Fall 2018

"""Merge the different WSJ0 folders into a single directory

Usage:
    merge-wsj0.py [-dcn] [-v...] [-l LIMIT] SOURCE DEST [MERGE-ROOT]

Options:
    -n, --dry-run                 # do a dry run without changing the disk
    -v, --verbose                 # verbosity level: more vs increases
    -d, --debug                   # output extra debug information
    -c, --copy                    # perform a copy instead of a move
    -l LIMIT, --limit=LIMIT       # only process LIMIT files (for debugging)
    MERGE-ROOT                    # directory to merge: defaults to wsj0

Examples:
    merge-wsj0.py -d csr_1 wsj0-merged

    # Test copy run over 10 files
    merge-wsj0.py csr_1 wsj0-merged -cvv -l 10

    # Print every directory found
    merge-wsj0.py -cv csr_1 wsj0-merged -l 10

    # Print every filename copied
    merge-wsj0.py -cvv csr_1 wsj0-merged -l 10
"""

from docopt import docopt
from pathlib import Path
import shutil

debug = False
verbosity = 0
dry_run = False

defaults = {
    '--debug': False,
    '--limit': None,
    '--copy': False,
    '--dry-run': False,
    '--verbose': 0,
    'MERGE-ROOT': 'wsj0',
}

def vprint(*args, **kargs):
    """print if debug"""
    global verbosity
    level = 1
    if "level" in kargs:
        level = kargs["level"]
        del kargs["level"]
    if verbosity >= level:
        print(*args, **kargs)

def dprint(*args, **kargs):
    """print if debug"""
    global debug
    if debug:
        print(*args, **kargs)

def merge_dir(source, dest, copy=False, limit=None):
    """Perform the actual merging of source to dest."""
    vprint(f"{'Copying' if copy else 'Moving'} files from {source} to {dest}.",
            level=1)
    count = 0
    # Only loop over files using a generator expression
    for src_file in (f for f in source.rglob("**/*") if f.is_file()):
        dest_file = dest / src_file.relative_to(source)
        vprint(f"{src_file} to {dest_file}", level=2)
        if dest_file.exists():
            vprint(f" * Warning: overwriting {dest_file}.", level=2)
        if not dry_run:
            # Checking parent directories for every file is pretty inefficient
            # and would be better to loop over directories directly creating
            # them as we go
            if not dest_file.parent.exists():
                vprint(f"Creating parent directory(ies) {dest_file.parent}.",
                        level=2)
                dest_file.parent.mkdir(exist_ok=True, parents=True)
            if copy:
                shutil.copy(src_file, dest_file)
            else:
                src_file.replace(dest_file)
        count += 1
        if limit is not None and count >= limit:
            break

    return count

def merge(source, dest, merge_root, copy=False, limit=None):
    """
    Search source for merge_root and then recursively move files below
    the merge_root into dest.
    """
    print(f"Merge {merge_root} from {source} to {dest}.")

    def merge_r(source, dest):
        """Perform the recursive search and merge"""
        count = 0
        # For every file at this level
        for path in source.iterdir():
            # if it's a directory
            if path.is_dir():
                # if it matches our merge_root
                if path.name == merge_root:
                    # then do the merge and don't recurse further
                    count += merge_dir(path, dest, copy, limit)
                else:
                    # it doesn't match merge_root
                    # so recurse into it
                    count += merge_r(path, dest)
            if limit is not None and count >= limit:
                break
        return count


    # Recursively search for the merge_root
    count = merge_r(source, dest)

    print(f"Successfully processed {count} file(s).")

    return 0

def main(args):
    global verbosity, debug, dry_run
    debug = args['--debug']
    verbosity = args['--verbose']
    dry_run = args['--dry-run']

    source = Path(args['SOURCE'])
    dest = Path(args['DEST'])
    merge_root = args['MERGE-ROOT']
    copy = args['--copy']
    limit = args['--limit']
    if limit is not None:
        limit = int(limit)

    if not source.is_dir():
        print(f"Source directory {source} doesn't exist.")
        return 1

    if dry_run:
        print("-n or --dry_run specified: no changes will be made to the filesystem")

    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    return merge(source, dest, merge_root, copy, limit)

if __name__ == "__main__":
    arguments = docopt(__doc__)

    # Drop arguments that are None
    arguments = {key:val for key, val in arguments.items() if val is not None}
    # merge dictionaries
    arguments = {**defaults, **arguments}

    exit(main(arguments))
