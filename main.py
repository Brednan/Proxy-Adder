from get_proxies_from_file import *
from proxy_server_api import ProxyServerAPI


if __name__ == '__main__':
    PORT = 65433
    with open('./proxy_server_ip', 'r') as f:
        PROXY_SERVER_API = f.read()

    while True:
        proxy_path = input('Enter the location of the proxies: ')
        if proxy_path:
            break

    while True:
        proxy_type = input('Enter the type of proxies: ')
        if proxy_type:
            break

    while True:
        auth_required = input('Is authentication required: ').lower()
        if auth_required:
            if auth_required in ('y', 'n'):
                break

    try:
        server_api = ProxyServerAPI(PROXY_SERVER_API, PORT, True)

        if auth_required == 'y':
            proxy_list = get_proxies_from_file(proxy_path, proxy_type, True)
            res = server_api.add_proxies(proxy_list, True)
        else:
            proxy_list = get_proxies_from_file(proxy_path, proxy_type)
            res = server_api.add_proxies(proxy_list)

        if res:
            print('Successfully added proxies!')
        else:
            print('Failed to add proxies!')

    except ConnectionRefusedError:
        print('Error: Unable to connect to the proxy server!')
