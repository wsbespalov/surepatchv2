# -*- coding: utf-8 -*-
import sys


def read_line(message: str) -> str:
    if sys.version_info[0]  == 2:
        return str(raw_input(message))
    return str(input(message))


def print_line(message: str) -> None:
    print(message)


def print_components(components: list) -> None:
    for index, component in enumerate(components):
        print('# {0}: name: {1}, version: {2}'.format(index, component['name'], component['version']))


def print_platforms(platforms: list) -> None:
    print('Platforms:')
    for index, platform in enumerate(platforms):
        print('# {0}: name: {1} description: {2}'.format(index, platform['name'], platform['description']))


def print_projects(projects: list) -> None:
    print('Projects:')
    for index, project in enumerate(projects):
        print('# {0}: name: {1} description: {2}'.format(index, project['name'], project['description']))


def print_issues(issues: list) -> None:
    print('Issues:')
    for index, issue in enumerate(issues):
        print('# {0}: name: {1} description: {2}'.format(index, issue['name'], issue['description']))
