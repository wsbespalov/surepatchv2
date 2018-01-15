# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
import importlib
import subprocess

from core.interface import print_line
from core.webapi import WebAPI

try:
    import pip
    from pip.utils import get_installed_distributions
except ImportError as import_exception:
    print_line(f"Can't import pip get_installed_distributions. Get an exception: {import_exception}.")
    sys.exit(0)


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

    def create_project_os_auto_system_none(self, api_data: dict) -> bool:
        components = []
        if api_data['os_type'] == OSs.WINDOWS:
            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                os_packages = self.load_windows_10_packages_from_powershell()[0]
                if os_packages is None:
                    print_line('Failed to load OS components.')
                    return False
                report = os_packages.decode('utf-8').replace('\r', '').split('\n')[9:]
                components = self.parse_windows_10_packages(report)
                if components[0] is None:
                    print_line('Failed parse OS components.')
                    return False
            if api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)

    def create_project_os_auto_system_path(self, api_data: dict) -> bool:
        components = []
        if api_data['os_type'] == OSs.WINDOWS:
            if api_data['os_version'] == '10' or api_data['os_version'] == '8':
                report = self.load_windows_10_packages_from_powershell_unloaded_file(api_data['file'])[0]
                if report is None:
                    return False
                components = self.parse_windows_10_packages(report=report)[0]
                if components is None:
                    return False
            if api_data['os_version'] == '7':
                print_line('Windows 7 does not support yet.')
                return False
        api_data['components'] = components
        return self.web_api.create_new_project(api_data=api_data)


    # -------------------------------------------------------------------------
    # SET
    # -------------------------------------------------------------------------

    def action_create_set(self, api_data: dict) -> bool:
        pass

    # -------------------------------------------------------------------------
    # Show
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Menu
    # -------------------------------------------------------------------------

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
                api_data['action'] != Actions.CREATE_SET:
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
                api_data['password'] = config['password']
                return True
            except yaml.YAMLError as yaml_exception:
                print_line(f'Config file save in yaml format exception: {yaml_exception}')
                return False
            finally:
                yaml_config_file.close()

class Actions(object):
    SAVE_CONFIG = 'save_config'
    CREATE_PLATFORM = 'create_platform'
    CREATE_PROJECT = 'create_project'
    CREATE_SET = 'create_set'


class Targets(object):
    OS = 'os'
    PIP = 'pip'
    REQ = 'req'
    REQUIREMENTS = 'requirements'
    NPM = 'npm'
    PACKAGE_JSON = 'package_json'
    GEM = 'gem'
    GEMLIST = 'gemlist'
    GEMFILE = 'gemfile'


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
