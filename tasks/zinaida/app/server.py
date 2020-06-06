#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import base64
import hmac
import json
import io
import os
import pickle
import random
import re
import sys
import time
import Crypto.Cipher.AES, Crypto.Random, Crypto.Util.Padding
import barcode
import barcode.writer

from jinja2 import FileSystemLoader

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, 'static')

PREFIX = "ugra_must_be_funny_in_a_rich_man_s_world_"
SECRET2 = b"liver-float-practice-list-inhabitant"
SALT2_SIZE = 12
SECRET3 = b'?g7P\x02\xc6\x82n\xa3fMhnb?\xa6'


GOODS = {b: v for b, v in pickle.load(open("goods.pkl", "rb")).items() if barcode.EAN13(b).ean == b}
# {"4607046123647": ('САХАР "ХОРОШИЙ/РУССКИЙ" РАФИНАД 1 КГ.', 6999, 'https://grozd.ru/content/images/thumbs/5ea139b8fb678c28bba4d0d9_sahar-horoijrusskij-rafinad-1-kg.jpeg')}


def encrypt(s):
    iv = Crypto.Random.get_random_bytes(Crypto.Cipher.AES.block_size)
    cipher = Crypto.Cipher.AES.new(SECRET3, Crypto.Cipher.AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(Crypto.Util.Padding.pad(json.dumps(s).encode(),
                                                                        Crypto.Cipher.AES.block_size)))

def decrypt(s):
    data = base64.b64decode(s)
    cipher = Crypto.Cipher.AES.new(SECRET3, Crypto.Cipher.AES.MODE_CBC, data[:Crypto.Cipher.AES.block_size])
    return json.loads(Crypto.Util.Padding.unpad(cipher.decrypt(data[Crypto.Cipher.AES.block_size:]),
                                                                    Crypto.Cipher.AES.block_size))

def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()

    @routes.get('/{token}/')
    async def root(request):
        token = request.match_info["token"]
        return jinja2.render_template('index.html', request, {})

    @routes.post('/{token}/next')
    async def next(request):
        token = request.match_info["token"]
        form = await request.post()
        try:
            cookie = decrypt(request.cookies.get("wstate", ""))
        except:
            cookie = {"token": token, "sum": 0}

        if cookie["token"] != token:
            return web.Response(text="HTTP/1.1 400 Это всё обман", status=400)

        this_barcode = form.get("barcode", "")
        if this_barcode:
            if this_barcode != cookie.get("next_barcode"):
                return web.Response(text="HTTP/1.1 422 Всё не так", status=422) 
            else:
                cookie["sum"] += GOODS[this_barcode][1]

        if this_barcode or "next_barcode" not in cookie:
            next_barcode = random.choice(list(GOODS.keys()))
            cookie["next_barcode"] = next_barcode
        else:
            next_barcode = cookie.get("next_barcode")

        barcode_io = io.BytesIO()
        barcode.EAN13(next_barcode, writer=barcode.writer.ImageWriter()).write(barcode_io)

        resp = web.StreamResponse()
        resp.headers["Content-type"] = "application/json"
        resp.set_cookie("wstate", encrypt(cookie).decode())
        await resp.prepare(request)
        await resp.write(json.dumps({"sum": cookie["sum"],
                                     "last": get_flag(token) if cookie["sum"] >= 100000000 else
                                             (GOODS[this_barcode][0] if this_barcode else None),
                                     "last_price": GOODS[this_barcode][1] if this_barcode else None,
                                     "next_pic": GOODS[next_barcode][2],
                                     "next_barcode": base64.b64encode(barcode_io.getvalue()).decode()}).encode())
        return resp

    routes.static('/static', STATIC_DIR)

    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))
    return app


def start():
    app = build_app()

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        web.run_app(app, path=os.path.join(sys.argv[1], 'zinaida.sock'))


if __name__ == '__main__':
    start()
