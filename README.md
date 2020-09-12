# Shopify-Monitor-Py

### How to install and use
1. Make sure you install [Python3](https://www.python.org/getit/) and [pip](https://pip.pypa.io/en/stable/installing/) followed by running the following in the same directory as main.py
```bash
pip install -r requirements.txt
```
2. Run main.py for new items where you add site urls in sitelist.txt, main_restocks.py for restock links.
```bash
python3 main.py
```
```bash
python3 main_restocks.py
```
### How to configure
I have a format setup in webhook.json where you can add the site name and the webhook where you want it to go. For example, if you want just bodega links posted in a specific webhook:
```bash
    "bodega": {
        "webhook": [
            "https://discordapp.com/api/webhooks/579704202398269440/uJSY0Biqn3LSjoCthiqfLefp9-h7lYrgyLGHgEUb97QaSE22uVZ6eSf4-qTIC4QqHh3t"
        ]
    },
```
Make sure you maintain the json valid! use jsonlint.com to make sure it is or else monitor will error out!

For sites that you want new products, use sitelist.txt. For restock, add product links in shopify.txt.

Note: this does not have any kind of cache bypass for obvious reasons.
