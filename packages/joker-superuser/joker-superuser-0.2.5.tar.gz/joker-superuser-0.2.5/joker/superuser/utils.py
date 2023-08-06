#!/usr/bin/env python3
# coding: utf-8

import os
from functools import wraps


def under_asset_dir(*paths):
    from joker.superuser.environ import JokerInterface
    ji = JokerInterface()
    return ji.under_package_dir('asset', *paths)


def load_config(name):
    import yaml
    from joker.superuser.environ import JokerInterface
    ji = JokerInterface
    path = ji.under_joker_subdir(name)
    if os.path.isfile(path):
        return yaml.safe_load(open(path))


def report(data, name):
    import json
    from joker.superuser.environ import JokerInterface
    ji = JokerInterface()
    if not name.endswith('.json'):
        name += '.json'
    path = ji.under_joker_subdir(name, mkdirs=True)
    with open(path, 'w') as fout:
        fout.write(json.dumps(data))


def silent_function(func):
    """Do not report any error"""

    @wraps(func)
    def sfunc(*args, **kwargs):
        # noinspection PyBroadException
        try:
            return func(*args, **kwargs)
        except Exception:
            pass

    return sfunc


def startswith(s, *prefixes):
    for p in prefixes:
        if s.startswith(p):
            return True
    return False


def find_regular_files(dirpath, **kwargs):
    for root, dirs, files in os.walk(dirpath, **kwargs):
        for name in files:
            path = os.path.join(root, name)
            if os.path.isfile(path):
                yield path


def check_filesys_case_sensitivity(dirname='.'):
    from tempfile import TemporaryDirectory
    with TemporaryDirectory(prefix='.sus-tmp', dir=dirname) as tmp:
        return not os.path.exists(tmp.upper())
