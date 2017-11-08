"""
Scaffy - Simple but powerful scaffolder based on templates

Scaffy is a library and command line tool to create scaffoldings based on
user defined templates.
"""

from configparser import ConfigParser, ExtendedInterpolation
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from textwrap import dedent, fill
from appdirs import AppDirs
import os

from .template import load_template_yaml

__author__ = 'Federico Stra'
__version__ = '0.0.0'
__version_info__ = tuple(map(int, __version__.split('.')))


CONFIG_FILENAME = "scaffy.cfg"

appdirs = AppDirs('scaffy')


def do_create(progargs, config):
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read([
        os.path.join(appdirs.user_config_dir, CONFIG_FILENAME),
        os.path.join(os.curdir, CONFIG_FILENAME)])

    if progargs.template_file is not None:
        template_file = progargs.template_file
    elif progargs.template_name is not None:
        template_name = progargs.template_name
        template_file = config[template_name]['source']
    else:
        template_name = config['DEFAULT']['template']
        template_file = config[template_name]['source']

    if progargs.verbose >= 1:
        print("creating", template_file)

    tree = load_template_yaml(template_file)
    tree.absolute(os.curdir)
    tree.mktree(**{k: v for k, v in config[template_name].items()
        if k not in ('source', 'loader')})


def do_list(progargs, config):
    for section in config.sections():
        if 'source' in config[section]:
            print("{}: {}".format(section, config[section]['source']))


def do_info(progargs, config):
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config_files = config.read([
        os.path.join(appdirs.user_config_dir, CONFIG_FILENAME),
        os.path.join(os.curdir, CONFIG_FILENAME)])

    print("progargs:", progargs)
    print("user_config_dir:", appdirs.user_config_dir)
    print("config_files:", config_files)
    print("config:", config.sections())


COMMAND_TABLE = {
    'create': do_create,
    'list': do_list,
    'info': do_info}


def make_argument_parser():
    def reformat(string):
        return "\n\n".join(map(fill, dedent(string).strip().split("\n\n")))

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=__doc__,
        epilog="Copyright 2017 Federico Stra")
    parser.add_argument('-i', '--interactive', action='store_true',
        help="run in interactive mode")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', action='store_true',
        help="be quiet (do not report errors, but infer them from return code)")
    group.add_argument('-v', '--verbose', action='count', default=0,
        help="be more verbose (cumulative up to 2 levels)")

    subparsers = parser.add_subparsers(title="available commands", dest='command')

    sub_create = subparsers.add_parser('create', aliases=['mk'],
        help="create a scaffolding based on a template",
        description="TODO: FILL THIS DESCRIPTION")
    sub_create.add_argument('-t', dest='template_name',
        help='name of the template to use', metavar='<template>')
    sub_create.add_argument('-T', dest='template_file',
        help='load the template from %(metavar)s', metavar='<file>')
    sub_create.add_argument('-d', default=os.curdir,
        help="where to create the scaffolding (DEFAULT: %(default)s)", metavar='<dir>')
    sub_create.add_argument('values', nargs='*', metavar='key=value',
        help="key-value pairs to customize the template")

    sub_list = subparsers.add_parser('list', aliases=['ls'],
        help='list available templates',
        description="TODO: FILL THIS DESCRIPTION")

    subparsers.add_parser('info',
        help="show configuration",
        description="TODO: FILL THIS DESCRIPTION")

    return parser


def main():
    parser = make_argument_parser()
    progargs = parser.parse_args()

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config_files = config.read([
        os.path.join(appdirs.user_config_dir, CONFIG_FILENAME),
        os.path.join(os.curdir, CONFIG_FILENAME)])

    if progargs.verbose >= 2:
        print("progargs:", progargs)
        print("config_files:", config_files)
        print("config:", config.sections())

    if progargs.command is None:
        parser.error("you must issue exactly one command")

    return COMMAND_TABLE[progargs.command](progargs, config)
