import json
from typing import AnyStr

import requests
from itertools import count


class Requests(object):
    def __init__(self, url_login: str = None, username: str = None,
                 password: AnyStr = None, json_request: AnyStr = None, id_request: int = None):

        self.url_login = url_login
        self.username = username
        self.password = password
        self.json_request = json_request
        self.id_request = id_request

    def get_intranet(self, url):

        """
        :param url: Url do GET - Deve ser informada no .env
        :return: Informacoes do Intranet
        """

        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}
        if self.id_request is None:
            return_inform = requests.get(url=f'{url}{self.id_request}', headers=headers, verify=True)
            return_inform_format = json.loads(return_inform.text)

            return return_inform_format
        else:
            return_inform = requests.get(url=url, headers=headers, verify=True)
            return_inform_format = json.loads(return_inform.text)

            return return_inform_format

    def get_cg(self, url):

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

        if self.id_request is None:
            headers = {'Authorization': 'Token ' + key_headers['key']}
            return_inform = requests.get(url=f'{url}{self.id_request}', headers=headers, verify=True)
            return_inform_format = json.loads(return_inform.text)

            return return_inform_format
        else:
            headers = {'Authorization': 'Token ' + key_headers['key']}
            return_inform = requests.get(url=url, headers=headers, verify=True)
            return_inform_format = json.loads(return_inform.text)

            return return_inform_format

    def post_cg(self, url):
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
            x = requests.post(url=url, data=json.dumps(self.json_request),
                              headers=headers, verify=True)
        except:
            pass

    def patch_cg(self, url):
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

        if self.id_request is None:
            requests.patch(url=f'{url}{self.id_request}', data=json.dumps(self.json_request),
                           headers=headers, verify=True)
        else:
            print('Não é possivel realizar um patch sem passar o Indice')

    def patch_file_cg(self, url, path):
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

        file_ob = {'arquivo': open(path, 'rb')}

        if self.id_request is None:
            requests.patch(f'{url}{self.id_request}', headers=headers, files=file_ob)
        else:
            print('Não é possivel realizar um patch sem passar o Indice')

    def delete_cg_generic(self, url, id, dict_inform, other_url):
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

        return_inform = requests.get(url=f'{url}{id}/', headers=headers, verify=True)
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
