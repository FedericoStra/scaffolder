import os


class DirTree:
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
        real_path = self.path.format(**kwargs)
        try:
            os.mkdir(real_path)
        except FileExistsError as e:
            if not os.path.isdir(real_path):
                raise
    def mktree(self, **kwargs):
        self.mkdir(**kwargs)
        for subdir in self.subdirs:
            subdir.mktree(**kwargs)
