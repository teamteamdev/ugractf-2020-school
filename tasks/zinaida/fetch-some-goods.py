#!/usr/bin/env python3

# GOODS = {"4607004890154": ('БЗМЖ СЫР ПЛАВЛЕНЫЙ "HOCHLAND" СЛИВОЧНЫЙ 400ГР', 20990, 'https://grozd.ru/content/images/thumbs/5ea130d9fb678c28bba34033_bzm-syr-plavlenyj-hochland-slivonyj-400gr.jpeg'),

import pickle
import bs4
import requests
import tqdm
import random

random.seed(0)

hrefs = []
for page in tqdm.tqdm([1, 2, 3, 4, 5]):
    soup = bs4.BeautifulSoup(requests.get("https://grozd.ru/produkty?pagesize=72&pagenumber=%d" % page).content)
    for pic in list(soup.find_all(class_="picture"))[1:]:
        hrefs.append(pic["href"])

goods = {}
for href in tqdm.tqdm(hrefs):
    soup = bs4.BeautifulSoup(requests.get("https://grozd.ru" + href).content)
    
    ean13 = soup.find(class_="gtin").find(class_="value").text.strip()
    name = soup.find(class_="generalTitle").text.strip().upper()
    price = int(soup.find(class_="actual-price").text.strip().replace(",", "").replace(" ₽", "")) + random.randint(-1000, 1000)
    pic = soup.find_all(class_="img-fluid")[-1]["src"]

    if len(ean13) == 13:
        goods[ean13] = (name, price, pic)

pickle.dump(goods, open("goods.pkl", "wb"))
