
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>

# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import json
import os

if __file__.startswith('/usr/local/'):
    PREF = '/usr/local/share'
elif __file__.startswith('/usr/'):
    PREF = '/usr/share'
else:
    PREF = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'share')
GLADE_FILE = os.path.join(PREF, 'gmeasure', 'gmeasure.glade')
HOME_DIR = os.path.expanduser('~')

_conf_file = os.path.join(HOME_DIR, '.config', 'gmeasure', 'conf.json')
_default_conf = {
        'colors':{
            'win': (0.308, 0.314, 0.191, 0.918),
            'mark': (0.918, 0.843, 0.113, 1.0),
            'line': (0.934, 0.866, 0.195, 1.0),
            'num': (0.073, 0.874, 0.399, 0.925),
            },
        'window': {
            'size': (300, 300),
            'pos': (200, 200),
            },
        }

def dump_conf(conf):
    with open(_conf_file, 'w') as fh:
        fh.write(json.dumps(conf))

def load_conf():
    if os.path.exists(_conf_file):
        with open(_conf_file) as fh:
            return json.loads(fh.read())
    else:
        try:
            os.makedirs(os.path.dirname(_conf_file))
        except OSError as e:
            print(e)
        dump_conf(_default_conf)
        return _default_conf
