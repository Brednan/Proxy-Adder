from proxy_server_api import ProxyServerAPI


PORT = 65433
with open('./proxy_server_ip', 'r') as f:
    PROXY_SERVER_API = f.read()

api = ProxyServerAPI(PROXY_SERVER_API, PORT, True)
print(api.get_proxies())
