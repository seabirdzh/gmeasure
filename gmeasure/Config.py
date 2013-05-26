
import json
import os

PREF = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'share')
#PREF = '/usr/share'
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
