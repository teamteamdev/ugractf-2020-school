#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp.web as web
import aiohttp_jinja2 as jinja2
import hmac
import json
import os
import pickle
import random
import sys

from jinja2 import FileSystemLoader

BASE_DIR = os.path.dirname(__file__)

PREFIX = "ugra_art_is_so_jvneovpakwnvjtoalqing_great_"
SECRET2 = b"loan-mortgage-destiny-grave-estate"
SALT2_SIZE = 12


def process_path(p):
    result = []
    commands = p.split()
    mode = None
    x, y = None, None
    x0, y0 = None, None
    for c in commands:
        if len(c) == 1 and c not in "0123456789":
            mode = c
            continue
        
        if "," in c:
            fs = c.split(",")
            nx, ny = float(fs[0]), float(fs[1])
        else:
            f = float(c)
            if mode == "H":
                nx, ny = f, y
            else:
                nx, ny = x, f

        if (x, y) == (None, None):
            dx, dy = 0, 0
            x0, y0 = nx, ny
        else:
            dx, dy = nx - x, ny - y
            result.append((dx, dy))
        x, y = nx, ny

    result.append((-sum(i[0] for i in result), -sum(i[1] for i in result)))
    return result

PATHS = dict(zip("abcdefghijklmnopqrstuvwxyz0123456789_", open("paths.txt").read().strip().split("\n")))
PATHS = {k: process_path(p) for k, p in PATHS.items()}


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), 'sha256').hexdigest()[:SALT2_SIZE]


def build_app():
    app = web.Application()
    routes = web.RouteTableDef()

    @routes.get('/{token}/')
    async def root(request):
        token = request.match_info["token"]
        flag = get_flag(token)
        data = sum([(PATHS[c] + [(20, 0)]) for c in flag], [])
        data = [(x/1.5, y/1.5) for x, y in data]
        return jinja2.render_template('index.html', request, {"data": json.dumps([list(i) for i in data])})

    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))
    return app


def start():
    app = build_app()

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        web.run_app(app, path=os.path.join(sys.argv[1], 'artist.sock'))


if __name__ == '__main__':
    start()
