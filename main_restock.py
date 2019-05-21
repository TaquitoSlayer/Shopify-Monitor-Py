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
def config():
    with open('config.json') as json_file:
        config = json.load(json_file)
        tasks = 1
        delay = config['delay']
    return tasks, delay

# executing now to prevent confusion
tasks, delay = config()
print(f'SHOPIFY RESTOCK MONITOR BY @TAQUITOSLAYER - {tasks} TASKS PER SITE WITH A DELAY OF {delay} SECONDS PER PROXY BAN')
    
def post_to_discord(title, image, _stock, price, product_url, variants):
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
                    embed.set_thumbnail(image)
                    embed.color = 0x00FF00
                    embed.description = f'[{title} has been restocked!]({product_url})'
                    price = int(price/100)
                    embed.add_field(name='Price',value=f'${str(price)}')
                    links = []
                    for vid, titlez in variants.items():
                        links.append(f'[{titlez}](http://{result}/cart/{vid}:1)\n')
                    links = ''.join(links)
                    embed.add_field(name='Sizes Available', value=links,inline='false')
                    embed.add_field(name='Quick Tasks', value=f'[EVE]({eve_qt}) - [CYBER]({cyber_qt}) - [PD]({pd_qt}) - [TKS]({tks_qt}) - [SB]({sb_qt}) - [SWFT]({swft_qt})',inline='false')
                    embed.set_footer(text=f'Shopify Monitor by @TaquitoSlayer | {result}')
                    client.send(embeds=[embed])
                    embed.fields.clear()
def monitor(url, proxy, task_num):
    try:
        title, image, stock, price, url, initial_stock_list = products.get_info(url, proxy)
    except requests.exceptions.RequestException as err:
        logging.info(f'{url.upper()} - {task_num} - {task_num}: ERROR: ' + err)
        pass
    while True:
        try:
            title, image, stock, price, url, new_stock_list = products.get_info(url, proxy)
        except requests.exceptions.RequestException as err:
            logging.info(f'{url.upper()} - {task_num} - {task_num}: ERROR: ' + err)
            pass

        diff = new_stock_list.items()- initial_stock_list.items()
        if bool(diff) == True:
            logging.info(f'{url.upper()} - {task_num}: NEW PRODUCT FOUND!')
            post_to_discord(title, image, stock, price, url, diff)
            initial_stock_list = new_stock_list
            time.sleep(2)


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


def generate_skulist(textfile):
    with open(textfile) as placeholders:
        skus = placeholders.read().splitlines()
    skus = list(set(skus))
    return skus

skus_m=[]
while True:
    skus = generate_skulist('shopify.txt')
    for sku in skus:
        if sku in skus_m:
            pass
        else:
            for i in range(int(tasks)):
                p = Thread(target=main, args=(i+1, sku, delay))
                p.start() # starting workers
