# -*- coding: utf-8 -*-

import os
import yaml

from core.interface import print_line
from core.webapi import WebAPI


class API(object):

    def __init__(self):
        self.web_api = WebAPI()

    def run_action(self, api_data: dict) -> bool:

        if not self.check_action_type(api_data=api_data):
            return False

        if api_data['action'] == Actions.SAVE_CONFIG:
            return self.save_config(api_data=api_data)

        if not self.load_config(api_data=api_data):
            return False

        if not self.action_login(api_data=api_data):
            return False

        if not self.web_api.get_organization_parameters(api_data=api_data):
            return False

        if api_data['action'] == Actions.CREATE_PLATFORM:
            return self.action_create_platform(api_data=api_data)

        if api_data['action'] == Actions.CREATE_PROJECT:
            return self.action_create_project(api_data=api_data)

        if api_data['action'] == Actions.CREATE_SET:
            return self.action_create_set(api_data=api_data)

    @staticmethod
    def check_action_type(api_data: dict) -> bool:
        if 'action' not in api_data:
            return False
        if api_data['action'] != Actions.SAVE_CONFIG and \
                api_data['action'] != Actions.CREATE_PLATFORM and \
                api_data['action'] != Actions.CREATE_PROJECT and \
                api_data['action'] != Actions.CREATE_SET:
            return False
        return True

    @staticmethod
    def save_config(api_data: dict) -> bool:
        file_name = '.surepatch.yaml'
        file_path = os.path.expanduser('~')
        full_path = os.path.join(file_path, file_name)
        config = dict(
            team=api_data['team'],
            user=api_data['user'],
            password=api_data['password']
        )
        with open(full_path, 'w') as yaml_config_file:
            try:
                yaml.dump(config, yaml_config_file)
                return True
            except yaml.YAMLError as yaml_exception:
                print_line(f'Config file save in yaml format exception: {yaml_exception}')
                return False
            finally:
                yaml_config_file.close()

    @staticmethod
    def load_config(api_data: dict) -> bool:
        file_name = '.surepatch.yaml'
        file_path = os.path.expanduser('~')
        full_path = os.path.join(file_path, file_name)
        if not os.path.isfile(full_path):
            print_line(f'Config file does not exist: ~/{file_name}')
            print_line('Create config file first with parameter --action=save_config.')
            return False
        with open(full_path, 'r') as yaml_config_file:
            try:
                config = yaml.load(yaml_config_file)
                if 'team' not in config or config['team'] is None or config['team'] == '':
                    return False
                api_data['team'] = config['team']
                if 'user' not in config or config['user'] is None or config['user'] == '':
                    return False
                api_data['user'] = config['user']
                if 'password' not in config or config['password'] is None or config['password'] == '':
                    return False
                return True
            except yaml.YAMLError as yaml_exception:
                print_line(f'Config file save in yaml format exception: {yaml_exception}')
                return False
            finally:
                yaml_config_file.close()

    def action_login(self, api_data: dict) -> bool:
        return self.web_api.login(api_data=api_data)

    def action_create_platform(self, api_data: dict) -> bool:
        pass

    def action_create_project(self, api_data: dict) -> bool:
        pass

    def action_create_set(self, api_data: dict) -> bool:
        pass


class Actions(object):
    SAVE_CONFIG = 'save_config'
    CREATE_PLATFORM = 'create_platform'
    CREATE_PROJECT = 'create_project'
    CREATE_SET = 'create_set'
