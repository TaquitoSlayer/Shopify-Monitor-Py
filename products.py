import requests
import re
import json

r = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}

def generate_sitelist():
    with open('sitelist.txt') as urls:
        sitelist = urls.read().splitlines()
    return sitelist

def List(url, proxy):
    product_urls = []
    json_url = 'https://' + url + '/products.json?from=135297231&to=2035543867467'
    dump = r.get(json_url, headers = headers, proxies={"http": proxy, "https": proxy})
    json_dump = dump.json()
    products = json_dump['products']
    for product in products:
        placeholder = product['handle']
        product_url = 'https://' + url + '/products/' + placeholder
        product_urls.append(product_url)
    return product_urls


def get_info(url, proxy):
    variants = {}
    resp = r.get(url, headers = headers, proxies={"http": proxy, "https": proxy})
    stock = 'N/A'
    image = 'https://i.imgur.com/PheG08Z.jpg'
    title = 'NO NAME FOUND'
    price = 'N/A'
    
    try:
        stock = re.findall(r'''"inventory_quantity":(\d*),''', resp.text)
        stock = stock[0]
    except:
        pass
    try:
        jsonurl = url + '.json'
        resp_json = r.get(jsonurl, headers = headers)
        resp_json = json.loads(resp_json.text)
    except:
        print('ERROR LOADING PRODUCT JSON')
        pass

    try:
        images = resp_json['product']['images']
        images = images[0]
        image = images['src']
    except:
        pass
    
    try:
        title = resp_json['product']['title']
    except:
        pass
    try:
        prices = resp_json['product']['variants']
        for price in prices:
            price = price['price']
    except Exception as e:
        print(e)
        pass
    try:
        variantz = resp_json['product']['variants']             
        for variant in variantz:
            vid = variant['id']
            name = variant['title']
            variants[vid] = name
    except Exception as e:
        print(f'ERROR: {e}')
        variants = {"NO ATC LINK FOUND" : "YOU-PLAYED-YOURSELF"}
    return title, image, stock, price, url, variants