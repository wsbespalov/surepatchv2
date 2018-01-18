# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
import importlib
import subprocess

from core.interface import print_line
from core.interface import print_platforms
from core.interface import print_projects
from core.interface import print_components

from core.webapi import WebAPI

try:
    import pip
    from pip.utils import get_installed_distributions
except ImportError as import_exception:
    print_line(f"Can't import pip get_installed_distributions. Get an exception: {import_exception}.")
    sys.exit(0)


raw_npm_components = []

def walkdict(data):
    for k, v in data.items():
        if isinstance(v, dict):
            walkdict(v)
        else:
            raw_npm_components.append({"name": k, "version": v})


class API(object):

    def __init__(self):
        self.web_api = WebAPI()

    # -------------------------------------------------------------------------
    # Run actions
    # -------------------------------------------------------------------------

    def run_action(self, api_data: dict) -> bool:
        if not self.check_action_type(api_data=api_data):
            return False

        if api_data['action'] == Actions.SAVE_CONFIG:
            return self.save_config(api_data=api_data)

        if not self.load_config(api_data=api_data):
            return False

        if not self.action_login(api_data=api_data):
            return False

        if not self.get_organization_parameters(api_data=api_data):
            return False

        if api_data['action'] == Actions.CREATE_PLATFORM:
            return self.action_create_platform(api_data=api_data)

        elif api_data['action'] == Actions.CREATE_PROJECT:
            return self.action_create_project(api_data=api_data)

        elif api_data['action'] == Actions.CREATE_SET:
            return self.action_create_set(api_data=api_data)

        elif api_data['action'] == Actions.SHOW_PLATFORMS or \
                api_data['action'] == Actions.SHOW_PROJECTS or \
                api_data['action'] == Actions.SHOW_SET:
            return self.action_show(api_data=api_data)

        print_line(f"Unknown action code: {api_data['action']}.")
        return False


    # -------------------------------------------------------------------------
    # LOGIN
    # -------------------------------------------------------------------------

    def action_login(self, api_data: dict) -> bool:
        return self.web_api.login(api_data=api_data)

    # -------------------------------------------------------------------------
    # GET ORGANIZATION PARAMETERS
    # -------------------------------------------------------------------------

    def get_organization_parameters(self, api_data: dict) -> bool:
        return self.web_api.get_organization_parameters(api_data=api_data)

    # -------------------------------------------------------------------------
    # PLATFORM
    # -------------------------------------------------------------------------

    def action_create_platform(self, api_data: dict) -> bool:
        if api_data['platform'] is None or api_data['platform'] == '':
            print_line('Empty platform name, please use --platform flag.')
            return False
        if api_data['description'] is None or api_data['description'] == '':
            print_line('Empty platform description. Change description to "default platform".')
            api_data['description'] = "default platform"
        return self.web_api.create_new_platform(api_data=api_data)

    # -------------------------------------------------------------------------
    # PROJECT
    # -------------------------------------------------------------------------

    def action_create_project(self, api_data: dict) -> bool:
        if api_data['platform'] is None or api_data['platform'] == '':
            print_line('Empty platform name.')
            return False
        if api_data['project'] is None or api_data['project'] == '':
            print_line('Empty project name.')
            return False
        platforms = self.get_platforms(api_data=api_data)
        if api_data['platform'] not in platforms:
            print_line(f"Platform {api_data['platform']} does not exists.")
            return False
        projects = self.get_projects(api_data=api_data)
        if api_data['project'] in projects:
            print_line(f"Project {api_data['project']} already exists.")
            return False

        # Select variant

        # Create new project with OS packages {from shell request}
        if api_data['target'] == Targets.OS and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_project_os_auto_system_none(api_data=api_data)

        # Create new project with OS packages from shell request unloading file {from path}
        if api_data['target'] == Targets.OS and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_os_auto_system_path(api_data=api_data)

        # Create new project with PIP packages {from shell request}
        if api_data['target'] == Targets.PIP and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_project_pip_auto_system_none(api_data=api_data)

        # Create new project with PIP from file {from path}
        if api_data['target'] == Targets.PIP and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_pip_auto_system_path(api_data=api_data)

        # Create new project with PIP requirements.txt {from path}
        if api_data['target'] == Targets.REQ and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_requirements_auto_system_path(api_data=api_data)

        # Create new project with NPM packages {from shell request} - global
        if api_data['target'] == Targets.NPM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_project_npm_auto_system_none(api_data=api_data)

        # Create new project with NPM packages {from shell request} - local
        if api_data['target'] == Targets.NPM_LOCAL and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_npm_local_auto_system_none(api_data=api_data)

        # Create new project with NPM packages {from file}
        if api_data['target'] == Targets.NPM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_npm_auto_system_path(api_data=api_data)

        # Create new project with NPM package.json file {from path}
        if api_data['target'] == Targets.PACKAGE_JSON and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_package_json_auto_system_path(api_data=api_data)

        # Create new project with NPM package_lock.json file {from path}
        if api_data['target'] == Targets.PACKAGE_LOCK_JSON and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_package_lock_json_auto_system_path(api_data=api_data)

        # Create new project with GEM packages {from shell request}
        if api_data['target'] == Targets.GEM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_project_gem_auto_system_none(api_data=api_data)

        # Create new project with GEM packages from shell request unloading file {from path}
        if api_data['target'] == Targets.GEM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_gem_auto_system_path(api_data=api_data)

        # Create new project with GEMFILE file {from path}
        if api_data['target'] == Targets.GEMFILE and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_gemfile_auto_system_path(api_data=api_data)

        # Create new project with GEMFILE.lock file {from path}
        if api_data['target'] == Targets.GEMFILE_LOCK and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_project_gemfile_lock_auto_system_path(api_data=api_data)

        print_line('Something wrong with app parameters. Please, look through README.md')
        return False

    # OS

    def create_project_os_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_os_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_os_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_os_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    # Python

    def create_project_pip_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_pip_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_pip_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_pip_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_requirements_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_requirements_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    # NPM

    def create_project_npm_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_npm_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_npm_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_npm_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_npm_local_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_npm_local_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_package_lock_json_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_npm_lock_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_package_json_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_package_json_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    # Ruby GEM

    def create_project_gem_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_gem_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_gem_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_gem_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_gemfile_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_gemfile_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_gemfile_lock_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_gemfile_lock_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    # -------------------------------------------------------------------------
    # SET
    # -------------------------------------------------------------------------

    def action_create_set(self, api_data: dict) -> bool:
        if api_data['platform'] is None:
            print_line('Empty Platform name. Please use --platform=platform_name parameter.')
            return False
        platforms = self.get_platforms(api_data=api_data)
        if api_data['platform'] not in platforms:
            print_line(f"Platform {api_data['platform']} does not exists.")
            return False
        if api_data['project'] is None:
            print_line('Empty Project name. Please use --project=project_name parameter.')
            return False
        projects = self.get_projects(api_data=api_data)
        if api_data['project'] not in projects:
            print_line(f"Project {api_data['project']} does not exists.")
            return False

        set_name = api_data['set']
        current_set_name = self.get_current_set_name(api_data=api_data)[0]

        if current_set_name == set_name:
            print_line(f'Current set with name {set_name} already exists.')
            print_line('Please, use another name, or use no --set parameter to autoincrement set name.')
            return False

        if set_name is None:
            if current_set_name[-1].isdigit():
                d = int(current_set_name[-1])
                d = d + 1
                current_set_name = current_set_name[:-1]
                set_name = current_set_name + str(d)
            else:
                set_name = current_set_name + '.1'
            api_data['set'] = set_name

        # Create new set with OS packages {from shell request}
        if api_data['target'] == Targets.OS and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_set_os_auto_system_none(api_data=api_data)

        # Create set with OS packages from shell request unloading file {from path}
        if api_data['target'] == Targets.OS and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_os_auto_system_path(api_data=api_data)

        # Create set with PIP packages {from shell request}
        if api_data['target'] == Targets.PIP and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_set_pip_auto_system_none(api_data=api_data)

        # Create set with PIP from file {from path}
        if api_data['target'] == Targets.PIP and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_pip_auto_system_path(api_data=api_data)

        # Create set with PIP requirements.txt {from path}
        if api_data['target'] == Targets.REQ and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_requirements_auto_system_path(api_data=api_data)

        if api_data['target'] == Targets.REQUIREMENTS and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_requirements_auto_system_path(api_data=api_data)

        # Create set with NPM packages {from shell request}
        if api_data['target'] == Targets.NPM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_set_npm_auto_system_none(api_data=api_data)

        # Create set with NPM packages {from file}
        if api_data['target'] == Targets.NPM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_npm_auto_system_path(api_data=api_data)

        # Create set with NPM package.json file {from path}
        if api_data['target'] == Targets.PACKAGE_JSON and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_package_json_auto_system_path(api_data=api_data)

        # Create set with NPM package_lock.json file {from path}
        if api_data['target'] == Targets.PACKAGE_LOCK_JSON and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_package_lock_json_auto_system_path(api_data=api_data)

        # Create set with GEM packages {from shell request}
        if api_data['target'] == Targets.GEM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is None:
            return self.create_set_gem_auto_system_none(api_data=api_data)

        # Create set with GEM packages from shell request unloading file {from path}
        if api_data['target'] == Targets.GEM and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_gem_auto_system_path(api_data=api_data)

        # Create set with GEMLIST file {from path}
        if api_data['target'] == Targets.GEMFILE and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_gemfile_auto_system_path(api_data=api_data)

        # Create set with GEMLIST file {from path}
        if api_data['target'] == Targets.GEMFILE_LOCK and \
                api_data['method'] == Methods.AUTO and \
                api_data['format'] == Formats.SYSTEM and \
                api_data['file'] is not None:
            return self.create_set_gemfile_lock_auto_system_path(api_data=api_data)

    def create_set_os_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_os_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_os_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_os_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_pip_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_pip_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_pip_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_pip_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_requirements_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_requirements_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_npm_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_npm_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_npm_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_npm_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_package_json_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_package_json_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_package_lock_json_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_npm_local_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_gem_auto_system_none(self, api_data: dict) -> bool:
        components = self.get_components_gem_auto_system_none(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_gem_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_gem_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_gemfile_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_gemfile_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    def create_set_gemfile_lock_auto_system_path(self, api_data: dict) -> bool:
        components = self.get_components_gemfile_lock_auto_system_path(api_data=api_data)
        if components[0] is None:
            return False
        api_data['components'] = components
        return self.web_api.create_new_component_set(api_data=api_data)

    # -------------------------------------------------------------------------
    # Show
    # -------------------------------------------------------------------------

    def action_show(self, api_data: dict) -> bool:
        if api_data['action'] == Actions.SHOW_PLATFORMS:
            return self.action_show_platforms(api_data=api_data)

        elif api_data['action'] == Actions.SHOW_PROJECTS:
            if api_data['platform'] is None or \
                    api_data['platform'] == '':
                print_line('Empty platform name.')
                return False
            platform_number = self.web_api.get_platform_number_from_name(api_data=api_data)
            if platform_number == -1:
                print_line(f"No such platform: {api_data['platform']}.")
                return False
            return self.action_show_projects(api_data=api_data)

        elif api_data['action'] == Actions.SHOW_SET:
            if api_data['platform'] is None or \
                    api_data['platform'] == '':
                print_line('Empty platform name.')
                return False
            platform_number = self.web_api.get_platform_number_from_name(api_data=api_data)
            if platform_number == -1:
                print_line(f"No such platform: {api_data['platform']}.")
                return False
            if api_data['project'] is None or \
                    api_data['project'] == '':
                print_line('Empty platform name.')
                return False
            project_number = self.web_api.get_project_number_from_name(api_data=api_data)
            if project_number == -1:
                print_line(f"No such project {api_data['project']} in platform {api_data['platform']}.")
                return False
            return self.show_set(api_data=api_data)

    @staticmethod
    def action_show_platforms(api_data: dict) -> bool:
        platforms = []
        for platform in api_data['organization']['platforms']:
            platforms.append({'name': platform['name'], 'description': platform['description']})
        print_platforms(platforms=platforms)
        return True

    def action_show_projects(self, api_data: dict) -> bool:
        projects = []
        platform_number = self.web_api.get_platform_number_from_name(api_data=api_data)
        for project in api_data['organization']['platforms'][platform_number]['projects']:
            projects.append({'name': project['name'], 'description': 'default project'})
        print_projects(projects=projects)
        return True

    def show_set(self, api_data: dict) -> bool:
        set = self.get_current_set_name(api_data=api_data)
        print_line(f'Current component set: {set}.')
        components = self.get_components(api_data=api_data)['components']
        print_components(components=components)
        return True

    # -------------------------------------------------------------------------
    # Menu
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Components
    # -------------------------------------------------------------------------

    def get_components_os_auto_system_none(self, api_data: dict) -> list:
        if api_data['os_type'] == OSs.WINDOWS:
            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                os_packages = self.load_windows_10_packages_from_powershell()[0]
                if os_packages is None:
                    print_line('Failed to load OS components.')
                    return [None]
                report = os_packages.decode('utf-8').replace('\r', '').split('\n')[9:]
                components = self.parse_windows_10_packages(report)
                if components[0] is None:
                    print_line('Failed parse OS components.')
                    return [None]
                return components
            if api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return [None]
        return [None]

    def get_components_os_auto_system_path(self, api_data: dict) -> list:
        if api_data['os_type'] == OSs.WINDOWS:
            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                report = self.load_windows_10_packages_from_powershell_unloaded_file(api_data['file'])[0]
                if report is None:
                    return [None]
                components = self.parse_windows_10_packages(report=report)
                if components[0] is None:
                    return [None]
                return components
            if api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return [None]

    def get_components_pip_auto_system_none(self, api_data: dict) -> list:
        return self.load_pip_packages_from_frozen_requirement()

    def get_components_pip_auto_system_path(self, api_data: dict) -> list:
        packages = self.load_pip_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_pip_packages_from_path(packages=packages)
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_requirements_auto_system_path(self, api_data: dict) -> list:
        packages = self.load_pip_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_pip_packages_from_path(packages=packages)
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_npm_auto_system_path(self, api_data: dict) -> list:
        packages = self.load_npm_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_npm_packages(raw_npm_components)
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_package_json_auto_system_path(self, api_data: dict) -> list:
        packages = self.load_package_json_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_package_json_packages_from_path(packages[0])
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_gem_auto_system_path(self, api_data: dict) -> list:
        packages = self.load_gem_packages_from_path(api_data['file'])
        if packages[0] is not None:
            return self.parse_gem_packages_from_path(packages[0])
        print_line('Something wrong with packages in file path')
        return [None]

    def get_components_npm_auto_system_none(self, api_data: dict) -> list:
        if api_data['os_type'] == 'windows':
            packages = self.load_npm_packages(path='', local=False)
            if packages[0] is not None:
                return self.parse_npm_packages(raw_npm_components)
            print_line('Something wrong with packages in file path')
            return [None]
        else:
            print_line('Dont check yet')
            return [None]

    def get_components_npm_local_auto_system_none(self, api_data: dict) -> list:
        if api_data['os_type'] == 'windows':
            packages = self.load_npm_packages(path=api_data['file'], local=True)
            if packages[0] is not None:
                return self.parse_npm_packages(raw_npm_components)
            print_line('Something wrong with packages in file path')
            return [None]
        else:
            print_line('Dont check yet')
            return [None]

    def get_components_npm_lock_auto_system_path(self, api_data: dict) -> list:
        if api_data['os_type'] == 'windows':
            packages = self.load_npm_lock_packages_from_path(filename=api_data['file'])
            if packages[0] is not None:
                return self.parse_npm_lock_packages(packages[0])
            print_line('Something wrong with packages in file path')
            return [None]
        else:
            print_line('Dont check yet')
            return [None]

    def get_components_gem_auto_system_none(self, api_data: dict) -> list:
        print_line('Dont check yet')
        return [None]

    def get_components_gemfile_auto_system_path(self, api_data: dict) -> list:
        print_line('Dont check yet')
        return [None]

    def get_components_gemfile_lock_auto_system_path(self, api_data: dict) -> list:
        print_line('Dont check yet')
        return [None]

    # -------------------------------------------------------------------------
    # Loaders
    # -------------------------------------------------------------------------

    @staticmethod
    def load_windows_10_packages_from_powershell() -> list:
        cmd = "Get-AppxPackage -AllUsers | Select Name, PackageFullName"
        try:
            proc = subprocess.Popen(
                ["powershell", cmd],
                stdout=subprocess.PIPE)
            output, error = proc.communicate()
            if error:
                print_line(f'Powershell command throw {proc.returncode} code and {error.strip()} error message.')
                return [None]
            if output:
                return [output]
        except OSError as os_error:
            print_line(f'Powershell command throw errno: {os_error.errno}, '
                       f'strerror: {os_error.strerror} and '
                       f'filename: {os_error.filename}.')
            return [None]
        except Exception as common_exception:
            print_line(f'Powershell command throw an exception: {common_exception}.')
            return [None]

    def load_windows_10_packages_from_powershell_unloaded_file(self, filename: str) -> list:
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename=filename)
            if enc == 'undefined':
                print_line('Undefined file encoding. Please, use utf-8 or utf-16.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as cf:
                    os_packages = cf.read()
                    if os_packages is None:
                        print_line(f'Cant read file: {filename}.')
                        return [None]
                    report = os_packages.replace('\r', '').split('\n')[9:]
                    return [report]
            except:
                print_line(f'File read exception.')
                return [None]
        print_line(f'File {filename} does not exists.')
        return [None]

    @staticmethod
    def load_pip_packages_from_frozen_requirement():
        components = []
        installations = {}
        try:
            for dist in get_installed_distributions(local_only=False, skip=[]):
                req = pip.FrozenRequirement.from_dist(dist, [])
                installations[req.name] = dist.version
            for key in installations:
                components.append({'name': key, 'version': installations[key]})
            return components
        except Exception as e:
            print_line(f'Get an exception: {e}.')
            return [None]

    def load_pip_packages_from_path(self, filename: str) -> list:
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line(f'Undefined file {filename} encoding.')
                return [None]
            try:
                with open(filename, encoding=enc) as cf:
                    rfp = cf.read()
                    rfps = rfp.replace(' ', '').split('\n')
                    return rfps
            except:
                print_line(f'Get an exception, when read file {filename}')
                return [None]
        print_line(f'File {filename} does not exists.')
        return [None]

    def load_npm_packages_from_path(self, filename: str) -> list:
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line(f'Undefined file {filename} encoding.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    data = json.load(pf)
                    walkdict(data)
                    return [True]
            except Exception as e:
                print_line(f'File read exception: {e}')
                return [None]
        print_line('File does not exist.')
        return [None]

    def load_npm_packages(self, path: str, local: bool) -> list:
        tmp_file_name = 'tmp_npm_list_json.txt'
        file_path = os.path.expanduser('~')
        full_path = os.path.join(file_path, tmp_file_name)
        try:
            with open(full_path, mode='w', encoding='utf-8') as temp:
                temp.write('')
                temp.seek(0)
        except Exception as e:
            print_line(f'Cant create temp file, get an exception: {e}.')
            return [None]
        cmd = "npm list --json > {0}".format(full_path)
        if os.name == 'nt':
            if not local:
                os.chdir(path)
            else:
                os.chdir("c:\\")
            try:
                proc = subprocess.Popen(
                    ["powershell", cmd],
                    stdout=subprocess.PIPE)
                output, error = proc.communicate()
                proc.kill()
                if error:
                    print_line(f'Powershell command throw {proc.returncode} code:')
                    print_line(f'and {error.strip()} error message.')
                    return [None]
                try:
                    enc = self.define_file_encoding(full_path)
                    if enc == 'undefined':
                        print_line('An error with encoding occured in temp file.')
                        return [None]
                    with open(full_path, encoding=enc) as cf:
                        data = json.load(cf)
                        walkdict(data)
                        return [True]
                except Exception as e:
                    print_line(f'File read exception: {e}')
                    return [None]
                finally:
                    if os.path.isfile(full_path):
                        os.remove(full_path)
            except OSError as os_error:
                print_line(f'Powershell command throw errno: {os_error.errno}, strerror: {os_error.strerror}')
                print_line(f'and filename: {os_error.filename}.')
                if os.path.isfile(full_path):
                    os.remove(full_path)
                return [None]
            finally:
                if os.path.isfile(full_path):
                    os.remove(full_path)
        if os.path.isfile(full_path):
            os.remove(full_path)
        return [None]

    def load_package_json_packages_from_path(self, filename: str) -> list:
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line(f'Undefined file {filename} encoding.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    packages = json.load(pf)
                    return [packages]
            except Exception as e:
                print_line(f'File {filename} read exception: {e}')
                return [None]
        print_line('File does not exist.')
        return [None]

    def load_npm_lock_packages_from_path(self, filename: str) -> list:
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line(f'Undefined file {filename} encoding.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    try:
                        packages = json.load(pf)
                        return [packages]
                    except json.JSONDecodeError as json_decode_error:
                        print_line(f'An exception occured with json decoder: {json_decode_error}.')
                        return [None]
            except Exception as e:
                print_line(f'File {filename} read exception: {e}')
                return [None]
        print_line('File does not exist.')
        return [None]

    def load_gem_packages_from_path(self, filename: str) -> list:
        if os.path.exists(filename):
            enc = self.define_file_encoding(filename)
            if enc == 'undefined':
                print_line(f'Undefined file {filename} encoding.')
                return [None]
            try:
                with open(filename, 'r', encoding=enc) as pf:
                    cont = pf.read().replace('default: ', '').replace(' ', '').replace(')', '')
                    cont = cont.split('\n')
                    return [cont]
            except Exception as e:
                print_line(f'File {filename} read exception: {e}')
                return [None]
        print_line('File does not exist.')
        return [None]

    # -------------------------------------------------------------------------
    # Parsers
    # -------------------------------------------------------------------------

    @staticmethod
    def parse_windows_10_packages(report: list) -> list:
        # TODO: Annotate type
        packages = []
        try:
            for report_element in report:
                if len(report_element) > 0:
                    splitted_report_element = report_element.split()
                    component_and_version = splitted_report_element[len(splitted_report_element) - 1]
                    element_array = component_and_version.split('_')
                    if len(element_array) >= 2:
                        common_component_name = element_array[0]
                        common_component_version = element_array[1]
                        component = {'name': common_component_name.split('.')}
                        if len(common_component_name.split('.')) >= 3 and component['name'][1] == 'NET':
                            component['name'] = 'net_framework'
                        else:
                            component['name'] = common_component_name.split('.')
                            component['name'] = component['name'][len(component['name']) - 1]
                        component['version'] = common_component_version.split('.')
                        component['version'] = component['version'][0] + '.' + component['version'][1]
                        packages.append(component)
            return packages
        except:
            print_line('Exception occured. Try run app with Administrator rights.')
            return [None]

    @staticmethod
    def parse_pip_packages_from_path(packages: list) -> list:
        components = []
        for ref in packages:
            if len(ref) > 0:
                if '==' in ref:
                    refs = ref.split('==')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '>' in ref:
                    refs = ref.split('>')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '<' in ref:
                    refs = ref.split('<')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '>=' in ref:
                    refs = ref.split('>=')
                    components.append({'name': refs[0], 'version': refs[1]})
                elif '<=' in ref:
                    refs = ref.split('<-')
                    components.append({'name': refs[0], 'version': refs[1]})
                else:
                    try:
                        mm = importlib.import_module(ref)
                        components.append({'name': ref, 'version': mm.__version__})
                    except ImportError as import_exception:
                        print_line(f'Get an exception {import_exception} when define component version.')
                        components.append({'name': ref, 'version': '*'})
                        continue
        return components

    @staticmethod
    def parse_npm_packages(comp: list) -> list:
        components2 = []
        for c in comp:
            if c["name"] == "from":
                if '@' in c['version']:
                    p = c["version"].split('@')
                    p[1] = p[1].replace('~', '')
                    components2.append({"name": p[0], "version": p[1]})
                else:
                    name = c["version"]
                    cmd = "npm view {0} version".format(name)
                    if os.name == 'nt':
                        try:
                            proc = subprocess.Popen(
                                ["powershell", cmd],
                                stdout=subprocess.PIPE)
                            version, error = proc.communicate()
                            version = version.decode("utf-8").replace('\n', '')
                            if error:
                                print_line(f'Powershell command throw {proc.returncode} code '
                                           f'and {error.strip()} error message.')
                        except OSError as os_error:
                            print_line(f'Powershell command throw errno: {os_error.errno}, strerror: {os_error.strerror}')
                            print_line(f'and filename: {os_error.filename}.')
                            continue
                        except:
                            continue
                    else:
                        # TODO: COMPLETE FOR ANOTHER PLATFORMS
                        version = '*'
                    components2.append({"name": name, "version": version})
        return components2

    @staticmethod
    def parse_npm_lock_packages(packages: dict) -> list:
        def already_in_components(components: list, key: str) -> bool:
            for component in components:
                if component['name'] == key:
                    return True
            return False

        dependencies = packages['dependencies']
        keys = dependencies.keys()
        components = []
        for key in keys:
            if not already_in_components(components=components, key=key):
                components.append({'name': key, "version": dependencies[key]['version']})
            if 'requires' in dependencies[key].keys():
                requires = dependencies[key]['requires']
                for rkey in requires.keys():
                    if not already_in_components(components=components, key=rkey):
                        components.append({'name': rkey, 'version': requires[rkey]})
            if 'dependencies' in dependencies[key].keys():
                deps = dependencies[key]['dependencies']
                for dkey in deps.keys():
                    if not already_in_components(components=components, key=dkey):
                        components.append({'name': dkey, 'version': deps[dkey]})
        return components

    @staticmethod
    def parse_package_json_packages_from_path(packages: dict) -> list:
        components = []
        dependencies = packages['dependencies']
        dev_dependencies = packages['devDependencies']
        if dev_dependencies != {}:
            for key in dev_dependencies.keys():
                components.append({'name': key, 'version': str(dev_dependencies[key]).replace('^', '')})
        if dependencies != {}:
            for key in dependencies.keys():
                components.append({'name': key, 'version': str(dependencies[key]).replace('^', '')})
        return components

    @staticmethod
    def parse_gem_packages_from_path(packages: list) -> list:
        components = []
        for c in packages:
            if len(c) > 0:
                cs = c.split('(')
                try:
                    components.append({'name': cs[0], 'version': cs[1]})
                except:
                    continue
        return components
    # -------------------------------------------------------------------------
    # Addition methods
    # -------------------------------------------------------------------------

    @staticmethod
    def define_file_encoding(filename: str) -> str:
        encodings = ['utf-16', 'utf-8', 'windows-1250', 'windows-1252', 'iso-8859-7', 'macgreek']
        for e in encodings:
            try:
                import codecs
                fh = codecs.open(filename, 'r', encoding=e)
                fh.readlines()
                fh.seek(0)
                return e
            except:
                continue
        return 'undefined'

    @staticmethod
    def get_platforms(api_data: dict) -> list:
        platforms = []
        if api_data['organization'] is None:
            return platforms
        if api_data['organization']['platforms'] is None:
            return platforms
        for platform in api_data['organization']['platforms']:
            platforms.append(platform['name'])
        return platforms

    def get_projects(self, api_data: dict) -> list:
        projects = []
        if api_data['organization'] is None:
            return projects
        if api_data['organization']['platforms'] is None:
            return projects
        platform_number = self.web_api.get_platform_number_from_name(api_data=api_data)
        if platform_number == -1:
            return projects
        for project in api_data['organization']['platforms'][platform_number]['projects']:
            projects.append(project['name'])
        return projects

    def get_current_set_name(self, api_data: dict) -> list:
        if api_data['organization'] is None:
            return [None]
        if api_data['organization']['platforms'] is None:
            return [None]
        platform_number = self.web_api.get_platform_number_from_name(api_data=api_data)
        if platform_number == -1:
            return [None]
        project_number = self.web_api.get_project_number_from_name(api_data=api_data)
        if project_number == -1:
            return ['0.0.1']
        return [api_data['organization']['platforms'][platform_number]['projects'][project_number]['current_component_set']['name']]

    def get_components(self, api_data: dict) -> list:
        if api_data['organization'] is None:
            return [None]
        if api_data['organization']['platforms'] is None:
            return [None]
        platform_number = self.web_api.get_platform_number_from_name(api_data=api_data)
        if platform_number == -1:
            return [None]
        project_number = self.web_api.get_project_number_from_name(api_data=api_data)
        if project_number == -1:
            return [None]
        return api_data['organization']['platforms'][platform_number]['projects'][project_number]['current_component_set']

    # -------------------------------------------------------------------------
    # Checkers
    # -------------------------------------------------------------------------

    @staticmethod
    def check_action_type(api_data: dict) -> bool:
        if 'action' not in api_data:
            return False
        if api_data['action'] != Actions.SAVE_CONFIG and \
                api_data['action'] != Actions.CREATE_PLATFORM and \
                api_data['action'] != Actions.CREATE_PROJECT and \
                api_data['action'] != Actions.CREATE_SET and \
                api_data['action'] != Actions.SHOW_PLATFORMS and \
                api_data['action'] != Actions.SHOW_PROJECTS and \
                api_data['action'] != Actions.SHOW_SET:
            return False
        return True

    # -------------------------------------------------------------------------
    # Config actions
    # -------------------------------------------------------------------------

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
            print_line(f'Create config file first with parameter --action=save_config.')
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
                api_data['password'] = config['password']
                return True
            except yaml.YAMLError as yaml_exception:
                print_line(f'Config file save in yaml format exception: {yaml_exception}.')
                return False
            finally:
                yaml_config_file.close()


class Actions(object):
    SAVE_CONFIG = 'save_config'
    CREATE_PLATFORM = 'create_platform'
    CREATE_PROJECT = 'create_project'
    CREATE_SET = 'create_set'
    SHOW_PLATFORMS = 'show_platforms'
    SHOW_PROJECTS = 'show_projects'
    SHOW_SET = 'show_set'


class Targets(object):
    OS = 'os'
    PIP = 'pip'
    REQ = 'req'
    REQUIREMENTS = 'requirements'
    NPM = 'npm'
    NPM_LOCAL = 'npm_local'
    PACKAGE_JSON = 'package_json'
    PACKAGE_LOCK_JSON = 'package_lock_json'
    GEM = 'gem'
    GEMFILE = 'gemfile'
    GEMFILE_LOCK = 'gemfile_lock'


class Methods(object):
    AUTO = 'auto'
    MANUAL = 'manual'


class Formats(object):
    SYSTEM = 'system'
    MANUAL = 'manual'


class OSs(object):
    WINDOWS = 'windows'
    UBUNTU = 'ubuntu'
    DEBIAN = 'debian'
    CENTOS = 'centos'
    FEDORA = 'fedora'
    OPENSUSE = 'opensuse'
    MACOS = 'macos'
