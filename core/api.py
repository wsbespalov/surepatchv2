# -*- coding: utf-8 -*-

from core.interface import print_line
from core.interface import print_platforms
from core.interface import print_projects
from core.interface import print_components
from core.interface import print_issues

from core.webapi import RequestLogin
from core.webapi import RequestCreatePlatform

requestLogin = RequestLogin()
requestCreatePlatform = RequestCreatePlatform()


class API(object):

    def route(self, action: dict) -> bool:
        if isinstance(action, dict):
            if self.check_action_structure(action):
                # Action -> Save config
                if action['action'] == Actions.SAVE_CONFIG:
                    if 'team' not in action:
                        print_line('Team is not defined. Use --team=your_team parameter.')
                        return False
                    if 'user' not in action:
                        print_line('User is not defined. Use --user=your_user_name parameter.')
                        return False
                    if 'password' not in action:
                        print_line('Password is not defined. Use --password=your_password parameter.')
                        return False
                    # Save config
                # Action -> Load config
                if action['action'] == Actions.LOAD_CONFIG:
                    pass
                # Action -> Create platform
                if action['action'] == Actions.CREATE_PLATFORM:
                    if 'platform' in action:
                        if action['platform'] is not None:
                            if action['platform'] != '':
                                if 'description' not in action:
                                    action['description'] = Messages.DEFAULT
                                if action['description'] == '':
                                    action['description'] = Messages.DEFAULT
                                platforms = self.get_platforms()
                                if action['platform'] not in platforms:
                                    # Call Create Platform method
                                    if self.action_create_platform(action=action):
                                        print_line('Platform created successfully.')
                                        return True
                                    else:
                                        print_line('Platform creation failed.')
                                        return False
                                else:
                                    print_line('Platform already exists.')
                                    return True
                            else:
                                print_line('Empty platform name.')
                                return False
                        else:
                            print_line('Platform parameter is None.')
                            return False
                    else:
                        print_line('Empty --platform parameter')
                        return False
                # Action -> Create project
                if action['action'] == Actions.CREATE_PROJECT:
                    if 'platform' in action:
                        if action['platform'] is not None and action['platform'] != '':
                            platforms = self.get_platforms()
                            if action['platform'] in platforms:
                                projects = self.get_projects(action['platform'])
                                if action['platform'] not in projects:
                                    # Call Create Project
                                    if self.action_create_project(action=action):
                                        print_line('Project created successfully.')
                                        return True
                                    else:
                                        print_line('Project creation failed.')
                                        return False
                                else:
                                    print_line('Project already exists.')
                                    return True
                            else:
                                print_line('Platform does not exists.')
                                return False
                        else:
                            print_line('Project parameter is empty or None.')
                            return False
                    else:
                        print_line('Empty --project parameter.')
                        return False
                # Action Create Set
                if action['action'] == Actions.CREATE_SET:
                    if 'platform' in action:
                        if action['platform'] is not None and action['platform'] != '':
                            platforms = self.get_platforms()
                            if action['platform'] in platforms:
                                if 'project' in action:
                                    projects = self.get_projects(action['platform'])
                                    if action['project'] in projects:
                                        if self.action_create_set(action=action):
                                            print_line('Set created successfully.')
                                            return True
                                        else:
                                            print_line('Set creation failed.')
                                            return False
                                    else:
                                        print_line('Project does not specified for defined platform.')
                                        return False
                                else:
                                    print_line('Project does defined.')
                                    return False
                            else:
                                print_line('Platform does not exists.')
                                return False
                        else:
                            print_line('Project parameter is empty or None.')
                            return False
                    else:
                        print_line('Empty --platform parameter.')
                        return False
            else:
                print_line('Unknown action type.')
                return False
        else:
            print_line('Wrong command object format.')
            return False

    # SAVE CONFIG

    def save_config(self, action: dict) -> bool:
        pass

    # LOAD CONFIG

    def load_config(self, action: dict) -> dict:
        pass

    # GET PLATFORMS

    def get_platforms(self) -> list:
        return []

    # GET PROJECTS

    def get_projects(self, platform: str) -> list:
        return []

    # CREATE_PLATFORM

    def action_create_platform(self, action: dict) -> bool:
        # Create Platform
        pass

    # CREATE_PROJECT

    def action_create_project(self, action: dict) -> bool:
        pass

    # CREATE_SET

    def action_create_set(self, action: dict) -> bool:
        pass

    @staticmethod
    def check_action_structure(action: dict) -> bool:
        if 'command' in action and \
                'target' in action and \
                'format' in action and \
                'method' in action and \
                'file' in action:
            return True
        return False


class Actions(object):
    SAVE_CONFIG = 'save_config'
    LOAD_CONFIG = 'load_config'
    CREATE_PLATFORM = 'create_platform'
    CREATE_PROJECT = 'create_project'
    CREATE_SET = 'create_set'
    SHOW_PLATFORMS = 'show_platforms'
    SHOW_PROJECTS = 'show_projects'
    SHOW_SET = 'show_set'
    SHOW_ISSUES = 'show_issues'

class Messages(object):
    DEFAULT = 'default'