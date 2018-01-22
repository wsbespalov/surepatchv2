#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import platform
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
    parser.add_argument(
        '--token',
        type=str,
        required=False,
        help='Define token from your web dashboard \
        to login without password'
    )
    return parser.parse_args()


def get_os_platform() -> str:
    if sys.platform == 'darwin' or platform.system() == 'Darwin':
        return 'macos'
    if sys.platform == 'linux2' or sys.platform == 'linux':
        dist = platform.dist()[0]
        if 'debian' in dist:
            return 'debian'
        if 'fedora' in dist:
            return 'fedora'
    if sys.platform == 'win32' or sys.platform == 'win64':
        return 'windows'


def get_os_version(os_platform: str) -> str:
    if os_platform == 'windows':
        return platform.uname()[2]
    return ''


def get_os_sp(os_platform: str) -> str:
    if os_platform == 'windows':
        return platform.win32_ver()[2][2:]
    return ''


def get_os_release() -> str:
    return platform.release()


def get_os_machine() -> str:
    return platform.machine()


def main():
    arguments = create_parser()
    api_data = dict(
        action=arguments.action,
        team=arguments.team,
        user=arguments.user,
        password=arguments.password,
        file=arguments.file,
        target=arguments.target,
        method=arguments.method,
        format=arguments.format,
        platform=arguments.platform,
        description=arguments.description,
        project=arguments.project,
        set=arguments.set,
        os_type=get_os_platform(),
        os_version=get_os_version(get_os_platform()),
        os_sp=get_os_sp(get_os_platform()),
        os_release=get_os_release(),
        os_machine=get_os_machine(),
        components=[],
        auth_token=arguments.token
    )

    if api.run_action(api_data=api_data):
        print_line('Complete successfully.')
        return 0
    print_line('Complete with errors.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
