# -*- coding: utf-8 -*-
import sys
import colorama


def print_logo():
    print('\n')
    print('+----------------------------------------------------------------------------------------+')
    text = """
                 #####                       ######                             
                #     # #    # #####  ###### #     #   ##   #####  ####  #    # 
                #       #    # #    # #      #     #  #  #    #   #    # #    # 
                 #####  #    # #    # #####  ######  #    #   #   #      ###### 
                      # #    # #####  #      #       ######   #   #      #    # 
                #     # #    # #   #  #      #       #    #   #   #    # #    # 
                 #####   ####  #    # ###### #       #    #   #    ####  #    # 
                (c) WebSailors, 2017
     """
    print(colorama.Fore.RED + text)
    print(colorama.Fore.WHITE + '+----------------------------------------------------------------------------------------+')


def print_line(message: str, effect: str = None) -> None:
    if effect == 'r':
        print(colorama.Fore.RED + message + colorama.Fore.WHITE)
    elif effect == 'g':
        print(colorama.Fore.GREEN + message + colorama.Fore.WHITE)
    elif effect == 'y':
        print(colorama.Fore.YELLOW + message + colorama.Fore.WHITE)
    else:
        print(colorama.Fore.WHITE + message)


def print_table(elements: list) -> None:
    print(elements)


def print_components(components: list) -> None:
    print_line('Components:', 'g')
    print_table(elements=components)


def print_platforms(platforms: list) -> None:
    print_line('Platforms:', 'g')
    print_table(elements=platforms)


def print_projects(projects: list) -> None:
    print_line('Projects:', 'g')
    print_table(elements=projects)


def print_issues(issues: list) -> None:
    print_line('Issues:')
    print_table(elements=issues)


def ask(message: str) -> str:
    if sys.version_info > (3, 0):
        return input(message)
    else:
        return raw_input(message)
