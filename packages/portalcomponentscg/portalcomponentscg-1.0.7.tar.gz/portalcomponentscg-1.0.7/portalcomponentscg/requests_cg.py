import json
from typing import AnyStr

import requests
from itertools import count


class Requests(object):
    def __init__(self, url_login: str = None, username: str = None,
                 password: AnyStr = None,
                 url_request: AnyStr = None, json_request: AnyStr = None, path: AnyStr = None):

        self.url_login = url_login
        self.username = username
        self.password = password
        self.url_request = url_request
        self.json_request = json_request
        self.path = path

    def get_intranet(self):

        """
        :param url: Url do GET - Deve ser informada no .env
        :return: Informacoes do Intranet
        """

        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}

        return_inform = requests.get(url=self.url_request, headers=headers, verify=True)
        return_inform_format = json.loads(return_inform.text)

        return return_inform_format

    def get_cg(self):

        """
        :param url: Url do GET - Deve ser informada no .env
        :return: Informacoes solicitadas
        """

        params = {
            'username': self.username,
            'password': self.password
        }
        key = requests.post(self.url_login, data=params)
        key_headers = json.loads(key.text)

        headers = {'Authorization': 'Token ' + key_headers['key']}
        return_inform = requests.get(url=self.url_request, headers=headers, verify=True)
        return_inform_format = json.loads(return_inform.text)

        return return_inform_format

    def post_cg(self):
        """
        :param url: Url do Post - Deve ser informada no .env
        :return: Registra informacoes no Portal
        """

        params = {
            'username': self.username,
            'password': self.password
        }
        key = requests.post(self.url_login, data=params)
        key_headers = json.loads(key.text)
        headers = {'Authorization': 'Token ' + key_headers['key'],
                   'Content-type': 'application/json',
                   'Accept': 'application/json'}
        try:
            x = requests.post(url=self.url_request, data=json.dumps(self.json_request),
                                 headers=headers, verify=True)
        except:
            pass

    def patch_cg(self):
        """
        :param url: Url do Post - Deve ser informada no .env
        :return: Registra informacoes no Portal
        """

        params = {
            'username': self.username,
            'password': self.password
        }
        key = requests.post(self.url_login, data=params)
        key_headers = json.loads(key.text)
        headers = {'Authorization': 'Token ' + key_headers['key'],
                   'Content-type': 'application/json',
                   'Accept': 'application/json'}
        try:

            x = requests.patch(url=self.url_request, data=json.dumps(self.json_request),
                               headers=headers, verify=True)
        except:
            pass

    def patch_file_cg(self):
        """
        :param url: Url do Post - Deve ser informada no .env
        :return: Registra informacoes no Portal
        """

        params = {
            'username': self.username,
            'password': self.password
        }
        key = requests.post(self.url_login, data=params)
        key_headers = json.loads(key.text)
        headers = {'Authorization': 'Token ' + key_headers['key']}

        file_ob = {'arquivo': open(self.path, 'rb')}

        try:
            r = requests.patch(self.url_request, headers=headers, files=file_ob)
            print(r.raise_for_status())
        except:
            pass

    def delete_cg_generic(self, id, dict_inform, other_url):
        """
        :param url: Url do Delet - Deve ser informada no .env
        :return: Status code
        """

        params = {
            'username': self.username,
            'password': self.password
        }
        key = requests.post(self.url_login, data=params)
        key_headers = json.loads(key.text)

        headers = {'Authorization': 'Token ' + key_headers['key'],
                   'Content-type': 'application/json',
                   'Accept': 'application/json'
                   }

        return_inform = requests.get(url=f'{self.url_request}{id}/', headers=headers, verify=True)
        return_inform_format = json.loads(return_inform.text)

        n = count(0)

        for i_return_portal in return_inform_format['colaborador']:
            num = next(n)
            if str(dict_inform['id']) == str(i_return_portal['id']):
                return_inform_format['colaborador'].pop(num)

        try:
            x = requests.patch(url=f'{other_url}{return_inform_format["id"]}/',
                               data=json.dumps(return_inform_format),
                               headers=headers, verify=True)
        except:
            pass
