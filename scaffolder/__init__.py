from configparser import ConfigParser, ExtendedInterpolation
import argparse
import os

from .template import load_template_yaml


def main():
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("scaffolder.cfg")

    template_name = config['DEFAULT']['template']
    template_file = config[template_name]['source']

    tree = load_template_yaml("templates/default.yaml")
    tree.absolute(os.curdir)
    tree.mktree(year=2017)
