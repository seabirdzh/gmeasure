#!/usr/bin/env python3

# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in the LICENSE file.

from distutils.core import setup
from distutils.core import Command
from distutils.command.clean import clean as distutils_clean
from distutils.command.sdist import sdist as distutils_sdist
import glob
import os
import shutil


def build_data_files():
    data_files = []
    for dir, dirs, files in os.walk('share'):
        target = dir
        if files:
            files = [os.path.join(dir, f) for f in files]
            data_files.append((target, files))
    return data_files

# will be installed to /usr/local/bin
scripts = ['gmeasure-bin', ]

if __name__ == '__main__':
    setup(
        name = 'gmeasure',
        description = 'A screenruler tool for linux users.',
        version = '1.2',
        license = 'GPLv3',
        url = 'https://github.com/LiuLang/gmeasure',

        author = 'LiuLang',
        author_email = 'gsushzhsosgsu@gmail.com',

        packages = ['gmeasure', ],
        scripts = scripts,
        data_files = build_data_files(),
        long_description = '''\
gmeasure is a simple screenruler for Gnome desktop, like kruler in KDE, or
measureit in Firefox.
''',
        )

