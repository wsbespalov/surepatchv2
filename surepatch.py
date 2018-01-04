#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import argparse

from core.api import API
api = API()

def argument_parser():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="SurePatch Argument Parser")

    parser.add_argument(
        '--action',
        type=str,
        required=False,
        help='Define action: '
             'save_config, '
             'create_platform, '
             'create_project, '
             'create_set, '
             'show_platforms, '
             'show_projects, '
             'show_set, '
             'show_issues')

    parser.add_argument(
        '--file',
        type=str,
        required=False,
        help="Define file name")

    parser.add_argument(
        '--target',
        type=str,
        required=False,
        help="Define SurePatch target (os/pip/requirements/npm/packages_json/gem/gemlist/gemfile...)")

    parser.add_argument(
        '--method',
        type=str,
        required=False,
        help="Define packages collection mode (auto/manual/file)")

    parser.add_argument(
        '--format',
        type=str,
        requred=False,
        help='Define file format (system/user)')

    parser.add_argument(
        '--team',
        type=str,
        required=False,
        help="Define your team")
    parser.add_argument(
        '--user',
        type=str,
        required=False,
        help="Define Username/email")
    parser.add_argument(
        '--password',
        type=str,
        required=False,
        help="Define Password")

    parser.add_argument(
        '--platform',
        type=str,
        required=False,
        help="Define Platform name")
    parser.add_argument(
        '--description',
        type=str,
        required=False,
        nargs='?',
        help="Define Project description")
    parser.add_argument(
        '--project',
        type=str,
        required=False,
        help="Define Project name")
    parser.add_argument(
        '--set',
        type=str,
        required=False,
        help='Define Set name. If is set "auto" - \
            set name will be incremented automatically')
    return parser.parse_args()

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())