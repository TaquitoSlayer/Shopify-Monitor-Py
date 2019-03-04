import proxyhandler
import products
from multiprocessing import Process
import time


file = '/Users/OverpricedFruit/proxies_aug23_fixed.txt'
proxies = proxyhandler.read_proxies(file)
sites = products.generate_sitelist()
site = sites[0]

def main(proxy):
    proxy_formatted = proxyhandler.proxy_parse(proxy)
    try:
        products.List(site, proxy_formatted)
        with open('proxies_good.txt', 'a') as f:
            f.write(f'{proxy}\n')
        print(proxy, ' - GOOD PROXY')
    except:
        print(proxy, ' - BAD PROXY')

if __name__ == '__main__':
    for proxy in proxies:
        p = Process(target=main, args=(proxy,))
        p.start() # starting workers
    p.join()
time.sleep(3)
print(f'ALL PROXIES CHECKED')
