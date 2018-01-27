# -*- coding: utf-8 -*-

import json
import requests
import datetime

from core.interface import print_line


class WebAPI(object):
    """
    Web API for Surepatch CLI Application.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) \
        Gecko/20100101 Firefox/45.0',
        'token': ''}
    base_url = "https://beta.surepatch.net"
    login_url = base_url + "/api/auth/login"
    organization_url = base_url + "/api/organization"
    platform_url = base_url + "/api/platforms"
    project_url = base_url + "/api/projects"
    issues_url = base_url + "/api/projects/partial"
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
    issues_payload = dict(

    )

    def send_login_request(self, api_data: dict) -> bool:
        """
        Send login request to Surepatch server.
        :param api_data: api data set
        :return: result
        """
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
                    login_response_text = json.loads(response.text)
                    api_data['token'] = login_response_text['token']
                    api_data['user_id'] = login_response_text['userID']
                    api_data['org_id'] = login_response_text['orgID']
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

    def send_get_organization_parameters_request(self, api_data: dict) -> bool:
        """
        Send special request to Surepatch server to get Organization information.
        :param api_data: api data set
        :return: result
        """
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

    def send_create_new_platform_request(self, api_data: dict) -> bool:
        """
        Send request to Surepatch server to create new Platform.
        :param api_data: api data set
        :return: result
        """
        self.headers['token'] = api_data['token']
        self.platform_payload['name'] = api_data['platform']
        self.platform_payload['description'] = api_data['description']
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

    def send_create_new_project_request(self, api_data: dict) -> bool:
        """
        Send request to Surepatch server to create new Project.
        :param api_data: api data set
        :return: result
        """
        self.headers['token'] = api_data['token']
        self.project_payload['name'] = api_data['project']
        self.project_payload['platform_id'] = self.get_platform_id_by_name(api_data=api_data)
        self.project_payload['components'] = api_data['components']
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

    def send_create_new_component_set_request(self, api_data: dict) -> bool:
        """
        Send request to Surepatch server to create new Component Set.
        :param api_data: api data set
        :return:
        """
        platform = api_data['platform']
        project = api_data['project']
        components = api_data['components']
        name = api_data['set']
        platform_number = self.get_platform_number_by_name(api_data=api_data)
        if platform_number == -1:
            print_line(f'No such platform: {platform}')
            return False
        project_number = self.get_project_number_by_name(api_data=api_data)
        if project_number == -1:
            print_line(f'No such project: {project}')
            return False
        project_url = api_data['organization']['platforms'][platform_number]['projects'][project_number]['url']
        self.headers['token'] = api_data['token']
        self.components_payload['set_name'] = name
        self.components_payload['components'] = components
        self.components_payload['project_url'] = project_url
        try:
            response = requests.post(
                url=self.components_url,
                headers=self.headers,
                json=self.components_payload)
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

    def send_delete_platform_request(self, api_data: dict) -> bool:
        """
        Send request to delete Platform.
        :param api_data: api data set
        :return: result
        """
        platform_id = self.get_platform_id_by_name(api_data=api_data)
        if platform_id == -1:
            print_line(f"Platform {api_data['platform']} does not exist.")
            return False

        self.headers['token'] = api_data['token']

        try:
            response = requests.delete(
                url=self.platform_url + '/' + str(platform_id),
                headers=self.headers,
                json=self.platform_payload)
            if response.status_code == 200:
                return True
            print_line(f'Delete Platform failed. Status code: {response.status_code}')
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

    def send_delete_project_request(self, api_data: dict) -> bool:
        """
        Send request to delete Project.
        :param api_data: api data set
        :return: result
        """
        platform_number = self.get_platform_number_by_name(api_data=api_data)
        if platform_number == -1:
            print_line(f"Platform {api_data['platform']} does not exist.")
            return False

        project_number = self.get_project_number_by_name(api_data=api_data)
        if project_number == -1:
            print_line(f"Project {api_data['project']} does not exist.")
            return False

        project_id = api_data['organization']['platforms'][platform_number]['projects'][project_number]['id']

        self.headers['token'] = api_data['token']

        try:
            response = requests.delete(
                url=self.project_url + '/' + str(project_id),
                headers=self.headers,
                json=self.project_payload)
            if response.status_code == 200:
                return True
            print_line(f'Delete Project failed. Status code: {response.status_code}')
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

    def send_archive_platform_request(self, api_data: dict) -> bool:
        """
        Send request to archive Platform.
        :param api_data: api data set
        :return: result
        """
        platform_id = self.get_platform_id_by_name(api_data=api_data)
        if platform_id == -1:
            print_line(f"Platform {api_data['platform']} does not exist.")
            return False

        self.headers['token'] = api_data['token']
        self.platform_payload['id'] = platform_id
        self.platform_payload['options'] = dict(
            state='archive',
            archivedBy=api_data['user']
        )
        try:
            response = requests.put(
                url=self.platform_url,
                headers=self.headers,
                json=self.platform_payload)
            if response.status_code == 200:
                return True
            print_line(f'Archive Platform failed. Status code: {response.status_code}')
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

    def send_archive_project_request(self, api_data: dict) -> bool:
        """
        Send request to archive Project.
        :param api_data: api data set
        :return: result
        """
        platform_number = self.get_platform_number_by_name(api_data=api_data)
        if platform_number == -1:
            print_line(f"Platform {api_data['platform']} does not exist.")
            return False

        project_number = self.get_project_number_by_name(api_data=api_data)
        if project_number == -1:
            print_line(f"Project {api_data['project']} does not exist.")
            return False

        project_id = api_data['platforms'][platform_number]['projects'][project_number]['id']

        self.headers['token'] = api_data['token']
        self.project_payload['id'] = project_id
        self.project_payload['options'] = dict(
            state='archive',
            archivedBy=api_data['user']
        )
        try:
            response = requests.put(
                url=self.project_url,
                headers=self.headers,
                json=self.project_payload)
            if response.status_code == 200:
                return True
            print_line(f'Archive Project failed. Status code: {response.status_code}')
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

    def send_restore_platform_request(self, api_data: dict) -> bool:
        """
        Send request to restore defined Platform from archive.
        :param api_data:
        :return:
        """
        if api_data['platform'] is None or api_data['platform'] == '':
            print_line('Empty platform name.')
            return False

        if not self.send_get_archived_platforms_request(api_data=api_data):
            print_line('There were errors in obtaining archived platforms.')
            return False

        platform_id = None
        platform_url = None

        for archive_platform in api_data['archive_platforms']:
            if api_data['platform'] == archive_platform['name']:
                platform_id = archive_platform['_id']
                platform_url = archive_platform['url']
                break

        if platform_id is None:
            print_line(f"Not such platform {api_data['platform']} in archive.")
            return False

        self.headers['token'] = api_data['token']
        self.platform_payload = dict(
            newPlatform=dict(
                id=platform_id,
                url=platform_url,
                options=dict(
                    updated=datetime.datetime.now().isoformat() + 'Z',
                    state='open',
                    archived=None
                )
            )
        )
        try:
            response = requests.put(
                url=self.platform_url,
                headers=self.headers,
                json=self.platform_payload)
            if response.status_code == 200:
                return True
            print_line(f'Archive Platform failed. Status code: {response.status_code}')
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

    def send_restore_project_request(self, api_data: dict) -> bool:
        """
        Send request to restore defined Project from archive.
        :param api_data: api data set
        :return: result
        """
        if api_data['platform'] is None or api_data['platform'] == '':
            print_line('Empty platform name.')
            return False

        if api_data['project'] is None or api_data['project'] == '':
            print_line('Empty project name.')
            return False

        if not self.send_get_archived_projects_request(api_data=api_data):
            print_line('There were errors in obtaining archived projects.')
            return False

        project_id = None
        project_url = None
        my_archived_project = dict()

        for archive_project in api_data['archive_projects']:
            if api_data['project'] == archive_project['name']:
                project_id = archive_project['_id']
                project_url = archive_project['url']
                my_archived_project = archive_project
                break

        if project_id is None:
            print_line(f"Not such project {api_data['project']} in archive.")
            return False

        if my_archived_project['platform_id']['name'] != api_data['platform']:
            print_line(f"Defined project {api_data['project']} not in defined platform {api_data['platform']}.")
            return False

        self.headers['token'] = api_data['token']
        self.project_payload = dict(
            newProject=dict(
                id=project_id,
                url=project_url,
                options=dict(
                    updated=datetime.datetime.now().isoformat() + 'Z',
                    state='open',
                    archived=None
                )
            )
        )
        try:
            response = requests.put(
                url=self.project_url,
                headers=self.headers,
                json=self.project_payload)
            if response.status_code == 200:
                return True
            print_line(f'Archive Platform failed. Status code: {response.status_code}')
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

    def send_get_archived_platforms_request(self, api_data: dict) -> bool:
        """
        Send request to get all archived platforms.
        :param api_data: api data set
        :return: result
        """
        self.headers['token'] = api_data['token']
        try:
            response = requests.get(
                url=self.platform_url + '/archive/' + api_data['organization']['id'],
                headers=self.headers,
                json=self.platform_payload)
            api_data['archive_platforms'] = None
            if response.status_code == 200:
                try:
                    api_data['archive_platforms'] = json.loads(response.text)
                except json.JSONDecodeError as json_decode_error:
                    print_line(f'An exception occured with json decoder: {json_decode_error}.')
                    return False
                return True
            print_line(f'Archive Platform get information failed. Status code: {response.status_code}')
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

    def send_get_archived_projects_request(self, api_data: dict) -> bool:
        """
        Send request to get all archived projects.
        :param api_data: api data set
        :return: result, modify api_data
        """
        self.headers['token'] = api_data['token']
        try:
            response = requests.get(
                url=self.project_url + '/archive/' + api_data['organization']['id'],
                headers=self.headers,
                json=self.project_payload)
            api_data['archive_projects'] = None
            if response.status_code == 200:
                try:
                    api_data['archive_projects'] = json.loads(response.text)
                except json.JSONDecodeError as json_decode_error:
                    print_line(f'An exception occured with json decoder: {json_decode_error}.')
                    return False
                return True
            print_line(f'Archive Project get information failed. Status code: {response.status_code}')
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

    def send_get_issues_request(self, api_data: dict) -> bool:
        self.headers['token'] = api_data['token']
        platform_number = self.get_platform_number_by_name(api_data=api_data)
        project_number = self.get_project_number_by_name(api_data=api_data)
        project_url = api_data['organization']['platforms'][platform_number]['projects'][project_number]['url']
        try:
            response = requests.post(
                url=self.issues_url + '/' + project_url,
                headers=self.headers,
                json=self.issues_payload)
            api_data['archive_projects'] = None
            if response.status_code == 200:
                try:
                    api_data['issues'] = json.loads(response.content)['project']['issues']
                    return True
                except json.JSONDecodeError as json_decode_error:
                    print_line(f'An exception occured with json decoder: {json_decode_error}.')
                    return False
            print_line(f'Archive Project get information failed. Status code: {response.status_code}')
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
    def get_platform_id_by_name(api_data: dict) -> int:
        """
        Get platform ID by its name.
        :param api_data: api data set
        :return: result
        """
        platform_name = api_data['platform']
        for platform in api_data['organization']['platforms']:
            if platform['name'] == platform_name:
                return platform['id']
        return -1

    @staticmethod
    def get_platform_number_by_name(api_data: dict)-> int:
        """
        Get Platform number in list by its name.
        :param api_data: api data set
        :return:result
        """

        platform_name = api_data['platform']
        for index, platform in enumerate(api_data['organization']['platforms']):
            if platform['name'] == platform_name:
                return index
        return -1

    def get_project_number_by_name(self, api_data: dict) -> int:
        """
        Get project number (index) by its name.
        :param api_data: api data set
        :return: result
        """

        project_name = api_data['project']
        platform_number = self.get_platform_number_by_name(api_data=api_data)
        for index, project in enumerate(api_data['organization']['platforms'][platform_number]['projects']):
            if project['name'] == project_name:
                return index
        return -1
