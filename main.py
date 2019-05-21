import requests
import logging
import products
import proxyhandler
from threading import Thread
import time
import json
from dhooks import Webhook, Embed
from urllib.parse import urlparse
import re

urls = []
logging.basicConfig(level=logging.INFO, format = '%(asctime)s: %(message)s')
logging.basicConfig(filename='debug.log',level=logging.DEBUG, format = '%(asctime)s: %(message)s')

# get sitelist as list
sites = products.generate_sitelist()

def config():
    with open('config.json') as json_file:
        config = json.load(json_file)
        tasks = 1
        delay = config['delay']
    return tasks, delay

# executing now to prevent confusion
tasks, delay = config()
print(f'SHOPIFY MONITOR BY @TAQUITOSLAYER - {tasks} TASKS PER SITE WITH A DELAY OF {delay} SECONDS PER PROXY BAN')

def check_if_posted(url):
    if url in urls:
        logging.info('PRODUCT ALREADY POSTED, IGNORING...')
    # might actually make duplicates rofl
    else:
        logging.info('NEW PRODUCT BEING ADDED TO LIST TO PREVENT DUPLICATES....')
        urls.append(url)
        post_to_discord(url)
    

def post_to_discord(product_url):
    fucked = False
    while not fucked:
        try:
            proxy_picked = proxyhandler.proxy()
            title, image, _stock, price, product_url, variants = products.get_info(product_url, proxy_picked)
            fucked = True
        except:
            pass
    parsed_uri = urlparse(product_url)
    result = '{uri.netloc}'.format(uri=parsed_uri)
    eve_qt = 'http://remote.eve-backend.net/api/quick_task?link=' + product_url
    cyber_qt = 'https://cybersole.io/dashboard/quicktask?url=' + product_url
    pd_qt = 'https://api.destroyerbots.io/quicktask?url=' + product_url
    tks_qt = 'https://thekickstationapi.com/quick-task.php?link=' + product_url
    sb_qt = 'https://scottbotv1.com/quicktask?' + product_url
    swft_qt = 'http://swftaio.com/pages/quicktask?Input=' + product_url
    with open('webhook.json') as json_file:
        json_dump = json.load(json_file)
        for site_name in json_dump:
            if site_name in result:
                webhookz = json_dump[site_name]['webhook']
                embed = Embed()
                for webhook in webhookz:
                    client = Webhook(webhook)
                    embed.color = 0x00FF00
                    embed.description = f'[{title}]({product_url})'
                    price = int(price/100)
                    embed.add_field(name='Price',value=f'${price}')
                    links = []
                    for vid, titlez in variants.items():
                        links.append(f'[{titlez}](http://{result}/cart/{vid}:1)\n')
                    links = ''.join(links)
                    embed.add_field(name='Sizes Available', value=links,inline='false')
                    embed.add_field(name='Quick Tasks', value=f'[EVE]({eve_qt}) - [CYBER]({cyber_qt}) - [PD]({pd_qt}) - [TKS]({tks_qt}) - [SB]({sb_qt}) - [SWFT]({swft_qt})',inline='false')
                    embed.set_thumbnail(image)
                    embed.set_footer(text=f'Shopify Monitor by @TaquitoSlayer | {result}')
                    client.send(embeds=[embed])
                    embed.fields.clear()

def channel_fill():
    fucked = False
    while not fucked:
        try:
            proxy_picked = proxyhandler.proxy()
            for site in sites:
                print(site)
                initial_product_list = products.List(site, proxy_picked)
                for product in initial_product_list:
                    post_to_discord(product)
                    fucked = True
        except Exception as e:
            logging.info(f'SOMETHING WRONG, PROBABLY PROXY BAN - {proxy_picked} - SLEEPING FOR {delay} SECONDS: {e}')
            print(e)
            time.sleep(float(delay))
            pass
    

def monitor(url, proxy, task_num):
    try:
        initial_product_list = products.List(url, proxy)
    except requests.exceptions.RequestException as err:
        logging.info(f'{url.upper()} - {task_num} - {task_num}: ERROR: ' + err)
        pass
    while True:
        try:
            new_product_list = products.List(url, proxy)
        except requests.exceptions.RequestException as err:
            logging.info(f'{url.upper()} - {task_num} - {task_num}: ERROR: ' + err)
            pass

        diff = list(set(new_product_list) - set(initial_product_list))
        if bool(diff) == True:
            logging.info(f'{url.upper()} - {task_num}: NEW PRODUCT FOUND!')
            diff = set(diff)
            for product in diff:
                check_if_posted(product)
                initial_product_list = new_product_list
        elif bool(diff) == False:
            logging.info(f'{url.upper()} - {task_num}: NO CHANGES FOUND')
            pass
        else:
            pass

def main(task_num, url, delay):
    fucked = False
    while not fucked:
        proxy_picked = proxyhandler.proxy()
        try:
            monitor(url, proxy_picked, task_num)
            fucked = True
        # simplejson.errors.JSONDecodeError
        except Exception as e:
            logging.info(f'{url.upper()} SOMETHING WRONG, PROBABLY PROXY BAN - {task_num}: {proxy_picked} - SLEEPING FOR {delay} SECONDS')
            logging.info(f'{e}')
            time.sleep(float(delay))
            pass


if __name__ == '__main__':
    for site in sites:
        for i in range(int(tasks)):
            print(site)
            p = Thread(target=main, args=(i+1, site, delay))
            p.start() # starting workers