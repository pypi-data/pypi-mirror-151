#!/usr/bin/env python3
# coding: utf-8

import os
from volkanic.utils import ignore_arguments
from joker.filesys.utils import spread_by_prefix


@ignore_arguments
def main():
    target_dir = 'files'
    os.makedirs(target_dir, exist_ok=False)
    for line in open('sha256sum.txt'):
        line = line.strip()
        if not line:
            continue
        chksum, old_path = line.split(maxsplit=1)
        names = spread_by_prefix(chksum)
        new_path = os.path.join(target_dir, *names)
        print(old_path, '=>', new_path)
        os.renames(old_path, new_path)
