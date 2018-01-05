# -*- coding: utf-8 -*-

from core.interface import print_line
from core.webapi import WebAPI

class API(object):

    def run_action(self, api_data: dict) -> bool:

        if not self.check_action_structure(api_data=api_data):
            return False

        if not self.check_action_type(api_data=api_data):
            return False

        if api_data['action'] == Actions.SAVE_CONFIG:
            return self.save_config(api_data=api_data)

        if not self.load_config(api_data=api_data):
            return False

        if not self.action_login(api_data=api_data):
            return False

        if api_data['action'] == Actions.CREATE_PLATFORM:
            return self.action_create_platform(api_data=api_data)

        if api_data['action'] == Actions.CREATE_PROJECT:
            return self.action_create_project(api_data=api_data)

        if api_data['action'] == Actions.CREATE_SET:
            return self.action_create_set(api_data=api_data)

    def check_action_structure(self, api_data: dict) -> bool:
        pass

    def check_action_type(self, api_data: dict) -> bool:
        pass

    def save_config(self, api_data: dict) -> bool:
        pass

    def load_config(self, api_data: dict) -> bool:
        pass

    def action_login(self, api_data: dict) -> bool:
        pass

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
