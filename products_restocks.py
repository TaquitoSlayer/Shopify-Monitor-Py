import requests
import re
import json

r = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}


def get_info(url, proxy):
    variants = {}
    resp = r.get(url, headers = headers, proxies={"http": proxy, "https": proxy})
    # resp = r.get(url, headers = headers)
    fucked = False
    while not fucked:
        try:
            stock = re.findall(r'''"inventory_quantity":(\d*),''', resp.text)
            stock = stock[0]
        except:
            stock = 'N/A'
            pass
        try:
            jsonurl = url + '.js'
            resp_json = r.get(jsonurl, headers = headers)
            resp_json = json.loads(resp_json.text)
        except:
            print('ERROR LOADING PRODUCT JSON')
            pass

        try:
            image = resp_json['images'][0]
            image = f'https:{image}'
        except:
            image = 'https://i.imgur.com/PheG08Z.jpg'
            pass
        
        try:
            title = resp_json['title']
        except:
            title = 'NO NAME FOUND'
            pass
        try:
            prices = resp_json['variants']
            for price in prices:
                price = price['price']
        except Exception as e:
            print(e)
            price = 'N/A'
            pass
        try:
            variantz = resp_json['variants']             
            for variant in variantz:
                if variant['available'] == True:
                    vid = variant['id']
                    name = variant['title']
                    variants[vid] = name
                else:
                    pass
            fucked = True
        except Exception as e:
            print(f'ERROR: {e}')
    
    return title, image, stock, price, url, variants