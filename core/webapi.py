# -*- coding: utf-8 -*-

import json
import requests

from core.interface import print_line


class WebAPI(object):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
        'token': ''}
    # a = "http://192.168.1.134:3000/"
    # b = "http://192.168.1.134:5555/api"
    # login_url = b + "/auth/login"
    # organization_url = b + "/organization"
    # platform_url = b + "/platforms"
    # project_url = b + "/projects"
    # components_url = b + "/components"
    base_url = "https://beta.surepatch.net"
    login_url = base_url + "/api/auth/login"
    organization_url = base_url + "/api/organization"
    platform_url = base_url + "/api/platforms"
    project_url = base_url + "/api/projects"
    components_url = base_url + "/api/components"
    login_payload = dict(
        username=None,
        password=None,
        referalToken=None,
        organization=None)
    platform_payload = dict(
        name='',
        description='')
    project_payload = dict(
        platform_id='',
        parent=None,
        project_url=None,
        project_id=None,
        required_right='manage_projects',
        name='',
        denied_if_unpaid=True,
        logo=None,
        components=[])
    components_payload = dict(
        set_name='0.0.0',
        components=[],
        project_url=None)

    def login(self, api_data: dict) -> bool:
        self.login_payload['username'] = api_data['user']
        self.login_payload['password'] = api_data['password']
        self.login_payload['referalToken'] = None
        self.login_payload['organization'] = api_data['team']
        try:
            response = requests.post(
                url=self.login_url,
                headers=self.headers,
                json=self.login_payload)
            if response.status_code == 200:
                try:
                    login_response = json.loads(response.text)
                    api_data['token'] = login_response['token']
                    api_data['user_id'] = login_response['userID']
                    api_data['org_id'] = login_response['orgID']
                    api_data['organization'] = None
                    print_line('Login success.')
                    return True
                except ValueError as json_value_exception:
                    print_line(f'Response JSON parsing exception: {json_value_exception}')
                    return False
            print_line(f'Login failed. Status code: {response.status_code}')
            return False
        except requests.exceptions.HTTPError as http_exception:
            print_line(f'HTTP Error: {http_exception}')
            return False
        except requests.exceptions.ConnectionError as connection_exception:
            print_line(f'Connection error: {connection_exception}')
            return False
        except requests.exceptions.Timeout as timeout_exception:
            print_line(f'Connection timeout: {timeout_exception}')
            return False
        except requests.exceptions.RequestException as request_exception:
            print_line(f'Request exception: {request_exception}')
            return False

    def get_organization_parameters(self, api_data: dict) -> bool:
        self.headers['token'] = api_data['token']
        try:
            response = requests.get(
                url=self.organization_url,
                headers=self.headers)
            if response.status_code == 200:
                try:
                    organization_data = json.loads(response.text)[0]
                    api_data['organization'] = dict(
                        id=organization_data['_id'],
                        name=organization_data['name'],
                        token=organization_data['token'],
                        ownerID=organization_data['owner_id']['_id'],
                        username=organization_data['owner_id']['username'],
                        first_name=organization_data['owner_id']['firstname'],
                        last_name=organization_data['owner_id']['lastname'],
                        token_expires=organization_data['owner_id']['tokenExpires'],
                        password_expires=organization_data['owner_id']['passwordExpires'],
                        first_sign_in=organization_data['owner_id']['firstSignin'],
                        private_key=organization_data['owner_id']['privateKey'],
                        connection_id=organization_data['owner_id']['connectionID'],
                        version=organization_data['owner_id']['__v'],
                        password=organization_data['owner_id']['password'],
                        github=organization_data['owner_id']['github'],
                        notifications=organization_data['owner_id']['notifications'],
                        TFA=organization_data['owner_id']['TFA'],
                        open_key=organization_data['owner_id']['openKey'],
                        blocked_till=organization_data['owner_id']['blockedTill'],
                        failed_attempts=organization_data['owner_id']['failedAttempts'],
                        updated=organization_data['owner_id']['updated'],
                        super=organization_data['owner_id']['super'],
                        last_passwords=organization_data['owner_id']['lastPasswords'],
                        url=organization_data['url'],
                        stripe_id=organization_data['stripe_id'],
                        team_plan_id=organization_data['team_plan_id'],
                        all_projects=organization_data['allProjects'],
                        platforms=[])
                    for platform_data in organization_data['platforms']:
                        platform = dict(
                            id=platform_data['_id'],
                            name=platform_data['name'],
                            description=platform_data['description'],
                            url=platform_data['url'],
                            version=platform_data['__v'],
                            projects=[])
                        for project_data in platform_data['projects']:
                            project = dict(
                                id=project_data['_id'],
                                name=project_data['name'],
                                logo=project_data['logo'],
                                organization_id=project_data['organization_id'],
                                platform_id=project_data['platform_id'],
                                current_component_set=project_data['current_component_set'],
                                token=project_data['token'], url=project_data['url'],
                                version=project_data['__v'], updated=project_data['updated'],
                                created=project_data['created'], issues=project_data['issues'],
                                component_set_history=project_data['component_set_history'],
                                child_projects=project_data['child_projects'],
                                parent_projects=project_data['parent_projects'])
                            platform['projects'].append(project)
                        api_data['organization']['platforms'].append(platform)
                    return True
                except ValueError as json_value_exception:
                    print_line(f'Response JSON parsing exception: {json_value_exception}')
                    return False
            print_line(f'Get organization parameters failed. Status code: {response.status_code}')
            return False
        except requests.exceptions.HTTPError as http_exception:
            print_line(f'HTTP Error: {http_exception}')
            return False
        except requests.exceptions.ConnectionError as connection_exception:
            print_line(f'Connection error: {connection_exception}')
            return False
        except requests.exceptions.Timeout as timeout_exception:
            print_line(f'Connection timeout: {timeout_exception}')
            return False
        except requests.exceptions.RequestException as request_exception:
            print_line(f'Request exception: {request_exception}')
            return False

    def create_new_platform(self, api_data: dict) -> bool:
        platform = api_data['platform']
        description = api_data['description']
        self.headers['token'] = api_data['token']
        self.platform_payload['name'] = platform
        self.platform_payload['description'] = description
        try:
            response = requests.post(
                url=self.platform_url,
                headers=self.headers,
                json=self.platform_payload)
            if response.status_code == 200:
                return True
            print_line(f'Create platform failed. Status code: {response.status_code}')
            return False
        except requests.exceptions.HTTPError as http_exception:
            print_line(f'HTTP Error: {http_exception}')
            return False
        except requests.exceptions.ConnectionError as connection_exception:
            print_line(f'Connection error: {connection_exception}')
            return False
        except requests.exceptions.Timeout as timeout_exception:
            print_line(f'Connection timeout: {timeout_exception}')
            return False
        except requests.exceptions.RequestException as request_exception:
            print_line(f'Request exception: {request_exception}')
            return False

    def create_new_project(self, api_data: dict) -> bool:
        project = api_data['project']
        components = api_data['components']
        platform_id = self.get_platform_id_from_name(api_data=api_data)
        self.headers['token'] = api_data['token']
        self.project_payload['name'] = project
        self.project_payload['platform_id'] = platform_id
        self.project_payload['components'] = components
        try:
            response = requests.post(
                url=self.project_url,
                headers=self.headers,
                json=self.project_payload)
            if response.status_code == 200:
                return True
            print_line(f'Create project failed. Status code: {response.status_code}')
            return False
        except requests.exceptions.HTTPError as http_exception:
            print_line(f'HTTP Error: {http_exception}')
            return False
        except requests.exceptions.ConnectionError as connection_exception:
            print_line(f'Connection error: {connection_exception}')
            return False
        except requests.exceptions.Timeout as timeout_exception:
            print_line(f'Connection timeout: {timeout_exception}')
            return False
        except requests.exceptions.RequestException as request_exception:
            print_line(f'Request exception: {request_exception}')
            return False

    def create_new_component_set(self, api_data: dict) -> bool:
        platform = api_data['platform']
        project = api_data['project']
        components = api_data['components']
        name = api_data['set']
        platform_number = self.get_platform_number_from_name(api_data=api_data)
        if platform_number == -1:
            print_line(f'No such platform: {platform}')
            return False
        project_number = self.get_project_number_from_name(api_data=api_data)
        if project_number == -1:
            print_line(f'No such project: {project}')
            return False
        self.headers['token'] = api_data['token']
        self.components_payload['set_name'] = name
        self.components_payload['components'] = components
        try:
            response = requests.post(
                url=self.project_url,
                headers=self.headers,
                json=self.project_payload)
            if response.status_code == 200:
                return True
            print_line(f'Create component set failed. Status code: {response.status_code}')
            return False
        except requests.exceptions.HTTPError as http_exception:
            print_line(f'HTTP Error: {http_exception}')
            return False
        except requests.exceptions.ConnectionError as connection_exception:
            print_line(f'Connection error: {connection_exception}')
            return False
        except requests.exceptions.Timeout as timeout_exception:
            print_line(f'Connection timeout: {timeout_exception}')
            return False
        except requests.exceptions.RequestException as request_exception:
            print_line(f'Request exception: {request_exception}')
            return False

    @staticmethod
    def get_platform_id_from_name(api_data: dict) -> int:
        platform_name = api_data['platform']
        for platform in api_data['organization']['platforms']:
            if platform['name'] == platform_name:
                return platform['id']
        return -1

    @staticmethod
    def get_platform_number_from_name(api_data: dict)-> int:
        platform_name = api_data['platform']
        for index, platform in enumerate(api_data['organization']['platforms']):
            if platform['name'] == platform_name:
                return index
        return -1

    def get_project_number_from_name(self, api_data: dict) -> int:
        project_name = api_data['project']
        platform_number = self.get_platform_number_from_name(api_data=api_data)
        for index, project in api_data['organization']['platforms'][platform_number].projects:
            if project['name'] == project_name:
                return index
        return -1
