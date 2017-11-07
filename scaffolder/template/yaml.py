import yaml

from ..dirtree import DirTree


def build_dir(d):
    if 'sub' in d:
        subdirs = [build_dir(sub) for sub in d['sub']]
        return DirTree(name=d['dir'], subdirs=subdirs)
    else:
        return DirTree(name=d['dir'])

def parse_scheleton(filename):
    with open(filename) as f:
        scheleton = yaml.load(f)


def load_template(filename):
    with open(filename, 'r') as f:
        template = f.read()
    d = yaml.load(template)
    return build_dir(d)
