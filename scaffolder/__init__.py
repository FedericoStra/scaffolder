import yaml
import os

class Directory:
    def __init__(self, name, subdirs=None):
        self.name = name
        if subdirs is None:
            self.subdirs = []
        else:
            self.subdirs = subdirs
    def absolute(self, where):
        self.path = os.path.join(where, self.name)
        for subdir in self.subdirs:
            subdir.absolute(self.path)
    def mkdir(self, **kwargs):
        try:
            os.mkdir(self.path.format(**kwargs))
        except FileExistsError as e:
            if not os.path.isdir(self.path):
                raise
    def mktree(self, **kwargs):
        self.mkdir(**kwargs)
        for subdir in self.subdirs:
            subdir.mktree(**kwargs)

def build_dir(d):
    if 'sub' in d:
        subdirs = [build_dir(sub) for sub in d['sub']]
        return Directory(name=d['dir'], subdirs=subdirs)
    else:
        return Directory(name=d['dir'])

def parse_scheleton(filename):
    with open(filename) as f:
        scheleton = yaml.load(f)

def main():
    with open("sls_ditta_std.yaml") as f:
        d = yaml.load(f)
    D = build_dir(d)
    D.absolute(os.curdir)
    D.mktree(ditta="ditta_std", anno=2017)


if __name__ == '__main__':
    main()