import asyncio
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from settings import SECRET_KEY
from handlers import handler


@asyncio.coroutine
def init(loop):
    app = web.Application(middlewares=[session_middleware(
        EncryptedCookieStorage(SECRET_KEY))])
    app.router.add_route('GET', '/', handler)
    srv = yield from loop.create_server(
        app.make_handler(), '0.0.0.0', 8080)
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
