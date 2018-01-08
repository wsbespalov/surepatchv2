#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import argparse

from core.api import API
from core.interface import print_line

api = API()


def create_parser():
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
        required=False,
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
    arguments = create_parser()
    api_data = dict()
    api_data['action'] = arguments.action
    api_data['team'] = arguments.team
    api_data['user'] = arguments.user
    api_data['password'] = arguments.password
    api_data['file'] = arguments.file
    api_data['target'] = arguments.target
    api_data['method'] = arguments.method
    api_data['format'] = arguments.format
    api_data['platform'] = arguments.platform
    api_data['description'] = arguments.description
    api_data['project'] = arguments.project
    api_data['set'] = arguments.set
    if api.run_action(api_data=api_data):
        print_line('Complete successfully.')
        return 0
    print_line('Complete with errors.')
    return 1


if __name__ == '__main__':
    sys.exit(main())