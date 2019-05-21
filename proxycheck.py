import proxyhandler
import products
from multiprocessing import Process
import time


file = './proxies_check.txt'
proxies = proxyhandler.read_proxies(file)
sites = products.generate_sitelist()
site = sites[0]

def main(proxy):
    proxy_formatted = proxyhandler.proxy_parse(proxy)
    try:
        start = time.time()
        products.List(site, proxy_formatted)
        end = time.time()
        time_elapsed = end - start
        time_elapsed = time_elapsed * 1000
        if time_elapsed < 5000:
            with open('proxies_good_mar7.txt', 'a') as f:
                f.write(f'{proxy}\n')
            print(proxy, ' - GOOD PROXY')
        else:
            print(proxy, ' - SLOW PROXY - ', time_elapsed)
    except:
        print(proxy, ' - BAD PROXY')

if __name__ == '__main__':
    for proxy in proxies:
        p = Process(target=main, args=(proxy,))
        p.start() # starting workers
    p.join()
time.sleep(3)
print(f'ALL PROXIES CHECKED')
