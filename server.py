import asyncio

import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from settings import SECRET_KEY, TEMPLATE_DIR
from handlers import *


@asyncio.coroutine
def init(loop):
    app = web.Application(middlewares=[session_middleware(
        EncryptedCookieStorage(SECRET_KEY))])
    aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

    app.router.add_route('GET', '/', base_handler)
    app.router.add_route('POST', '/setname', set_name_handler, expect_handler=web.Request.json)
    app.router.add_route('GET', '/start_new_game', start_new_game_handler)
    game = app.router.add_resource(r'/game/{game_id}')
    game.add_route('GET', game_handler)

    srv = yield from loop.create_server(
        app.make_handler(), '0.0.0.0', 8080)
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
