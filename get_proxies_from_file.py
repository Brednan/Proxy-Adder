from proxy_server_api import Proxy


def get_proxies_from_file(file_path: str, proxy_type, auth_required=False) -> list:
    proxy_list = []

    with open(file_path, 'r') as f:
        raw_proxy_list = f.read().strip().split('\n')
        for raw_proxy in raw_proxy_list:
            proxy = raw_proxy.split(':')

            if auth_required:
                if len(proxy) < 4:
                    continue

                proxy_list.append(Proxy(proxy[0], proxy[1], proxy_type, None, proxy[2], proxy[3], True))
                continue

            if len(proxy) < 2:
                continue

            proxy_list.append(Proxy(proxy[0], proxy[1], proxy_type, None))

    return proxy_list
