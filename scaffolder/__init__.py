import yaml
import os

from .template import load_template_yaml

def main():
    tree = load_template_yaml("templates/default.yaml")
    tree.absolute(os.curdir)
    tree.mktree(year=2017)
