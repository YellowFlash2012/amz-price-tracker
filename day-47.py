import requests
from bs4 import BeautifulSoup
from twilio.rest import *
from config import *
from lxml import html

client = Client(account_sid, auth_token)

url = 'https://www.amazon.com/gp/product/B0000Z6JIW/ref=ox_sc_saved_title_8?smid=ATVPDKIKX0DER&psc=1'

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "X-Forwarded-For": "156.0.213.5",
    "X-Http-Proto": "HTTP/1.1"
}

res = requests.get(url=url, headers=headers)
res.raise_for_status()

# tree = html.fromstring(res.content)
# print(res.status_code)
res_data = res.text
soup = BeautifulSoup(res_data, 'lxml')
priceEl= soup.find(name="td", id="priceblock_ourprice_lbl")
price = soup.find(name="span", id="priceblock_ourprice").getText().strip()

deal_price = price.split("$", 1)[1]

msg= 'Got good news for you. You can get the presto pressure cooker for less than $200 right now. Hurry up, it might not last'

if float(deal_price) < 200:
    message = client.messages \
        .create(
            body=msg,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )

    print(message.status)
