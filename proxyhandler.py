from itertools import cycle
import random

proxies_file = 'proxies.txt'

def read_proxies(file):
    with open(file) as txt_file:
        proxies = txt_file.read().splitlines()
    return proxies

def proxy_parse(proxy):
    proxy_parts = proxy.split(':')
    if len(proxy_parts) == 2:
        ip, port = proxy_parts
        formatted_proxy = {'http': f'https://{ip}:{port}/',}
    elif len(proxy_parts) == 4:
        ip, port, user, password = proxy_parts
        formatted_proxy = {'http': f'https://{user}:{password}@{ip}:{port}/',}
    formatted_proxy = formatted_proxy['http']
    return formatted_proxy

def proxy():
    proxies = read_proxies(proxies_file)
    proxy_rotation = random.choice(proxies)
    proxy = proxy_parse(proxy_rotation)
    return proxy

