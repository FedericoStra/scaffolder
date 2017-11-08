from configparser import ConfigParser, ExtendedInterpolation
from argparse import ArgumentParser
from appdirs import AppDirs
import os

from .template import load_template_yaml

__author__ = 'Federico Stra'
__version__ = '0.0.0'
__version_info__ = tuple(map(int, __version__.split('.')))


CONFIG_FILENAME = "scaffy.cfg"


def make_argument_parser():
    parser = ArgumentParser(
        description="Create a scaffolding based on a template.",
        epilog="Copyright 2017 Federico Stra")
    parser.add_argument('-i', '--interactive', action='store_true',
        help="run in interactive mode")
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help="be more verbose (cumulative up to 2 levels)")
    parser.add_argument('-q', '--quiet', action='store_true',
        help="be quiet (do not report errors, but infer them from return code)")
    subparsers = parser.add_subparsers(title="available commands", dest='command',
        description="valid commands to execute",
        # help="specify exactly one command"
        )
    sub_create = subparsers.add_parser('create',
        help="create a scaffolding based on a template",
        description="TODO: FILL THIS DESCRIPTION")
    sub_create.add_argument('-t', help='name of the template to use', metavar='<template>')
    sub_create.add_argument('-T', help='load the template from %(metavar)s', metavar='<file>')
    sub_create.add_argument('-d', help='where to create the scaffolding (DEFAULT: %(default)s)', metavar='<dir>', default=os.curdir, required=True)
    sub_create.add_argument('values', nargs='*', metavar='key=value')
    sub_list = subparsers.add_parser('list',
        help='list available templates',
        description="TODO: FILL THIS DESCRIPTION")

    subparsers.add_parser('info',
        help="show configuration",
        description="TODO: FILL THIS DESCRIPTION")
    return parser


def main():
    parser = make_argument_parser()
    progargs = parser.parse_args()

    print(progargs)

    appdirs = AppDirs('scaffy')

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read([
        os.path.join(appdirs.user_config_dir, CONFIG_FILENAME),
        os.path.join(os.curdir, CONFIG_FILENAME)])

    template_name = config['DEFAULT']['template']
    template_file = config[template_name]['source']

    tree = load_template_yaml(template_file)
    tree.absolute(os.curdir)
    tree.mktree(year=2017)
