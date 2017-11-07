from configparser import ConfigParser, ExtendedInterpolation
from argparse import ArgumentParser
import os

from .template import load_template_yaml


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    subparsers = parser.add_subparsers(title='commands', description='valid commands to execute', help='help me', dest='command')
    sub_create = subparsers.add_parser('create')
    sub_create.add_argument('-t', help='name of the template to use', metavar='<template>')
    sub_create.add_argument('-T', help='load the template from %(metavar)s', metavar='<file>')
    sub_create.add_argument('-d', help='where to create the scaffolding (DEFAULT: %(default)s)', metavar='<dir>', default=os.curdir)
    sub_create.add_argument('-z', default=42)
    subparsers.add_parser('list', help='help me listing!')
    namespace = parser.parse_args()

    print(namespace)

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("scaffolder.cfg")

    template_name = config['DEFAULT']['template']
    template_file = config[template_name]['source']

    tree = load_template_yaml("templates/default.yaml")
    tree.absolute(os.curdir)
    tree.mktree(year=2017)
