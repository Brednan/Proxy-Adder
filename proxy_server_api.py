from cryptography.fernet import Fernet
import json
import socket
from proxy import Proxy


class ProxyServerAPI(Fernet, socket.socket):
    def __init__(self, host, port, v6=False):
        self.host = host
        self.port = port

        if v6:
            socket.socket.__init__(self, socket.AF_INET6, socket.SOCK_STREAM)
        else:
            socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)

        self.__auth_token__ = self.__get_auth_token__()
        Fernet.__init__(self, self.__get_cryptography_key__())

    @staticmethod
    def __get_cryptography_key__():
        with open('./fernet_key.txt', 'rb') as f:
            return f.read()

    @staticmethod
    def __get_auth_token__():
        with open('./auth_token.txt', 'r') as f:
            return f.read()

    def __encrypt_message__(self, msg: str) -> bytes:
        return self.encrypt(msg.encode())

    def __decrypt_message__(self, msg: bytes) -> str:
        return self.decrypt(msg).decode()

    def __parse_content__(self, msg: bytes) -> dict:
        try:
            msg = self.__decrypt_message__(msg)
            return json.loads(msg)
        except json.JSONDecodeError:
            return {}

    def __encode_request__(self, content: dict) -> bytes:
        content_bytes = json.dumps(content).encode()
        return self.encrypt(content_bytes)

    def __send_request__(self, content: dict) -> dict:
        self.connect((self.host, self.port))
        content_bytes = self.__encode_request__(content)
        self.send(content_bytes + b'/END')

        res = b''
        buffer = self.recv(2048)
        while buffer:
            res += buffer
            buffer = self.recv(2048)

        if not res:
            return {}

        return self.__parse_content__(res)

    # Take list of proxies in a dictionary, and make them a list of Proxy objects
    @staticmethod
    def __create_proxy_list__(proxy_dicts):
        proxy_list = []
        for proxy in proxy_dicts:
            proxy_list.append(Proxy(proxy.get('ip'), proxy.get('port'), proxy.get('protocol'),
                                    proxy.get('anonymity_level'), proxy.get('username'), proxy.get('password'),
                                    proxy.get('auth_required')))

        return proxy_list

    def get_proxies(self, proxy_type='All', anonymity_level='All'):
        res = self.__send_request__({
            'command': 'get_proxies',
            'auth_token': self.__auth_token__,
            'proxy_type': proxy_type,
            'anonymity_level': anonymity_level
        })

        print(res)

        if not res.get('success') or not res.get('proxies'):
            return []

        return self.__create_proxy_list__(res.get('proxies'))

    def add_proxies(self, proxy_list: list, auth_required=False) -> bool:
        proxy_dict_list = []
        for proxy in proxy_list:
            if not auth_required:
                proxy_dict_list.append({
                    'ip': proxy.ip,
                    'port': proxy.port,
                    'proxy_type': proxy.protocol,
                    'anonymity_level': proxy.anonymity_level
                })
                continue

            proxy_dict_list.append({
                'ip': proxy.ip,
                'port': proxy.port,
                'proxy_type': proxy.protocol,
                'anonymity_level': proxy.anonymity_level,
                'username': proxy.username,
                'password': proxy.password,
                'auth_required': True
            })

        res = self.__send_request__({
            'auth_token': self.__auth_token__,
            'command': 'add_proxies',
            'proxy_list': proxy_dict_list,
            'auth_required': auth_required
        })

        return res.get('success') is True
