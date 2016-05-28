import asyncio

from jinja2 import FileSystemLoader
from aiohttp.web import Application
from aiohttp_jinja2 import setup as setup_jinja
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from settings import SECRET_KEY, TEMPLATE_DIR
from routes import routes


@asyncio.coroutine
def init(loop):
    app = Application(middlewares=[session_middleware(
        EncryptedCookieStorage(SECRET_KEY))])
    setup_jinja(app, loader=FileSystemLoader(TEMPLATE_DIR))
    for route in routes:
        app.router.add_route(route['method'], route['url'], route['handler'], **route['kwargs_'])
    srv = yield from loop.create_server(
        app.make_handler(), '0.0.0.0', 8080)
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
