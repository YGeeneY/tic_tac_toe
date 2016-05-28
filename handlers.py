import time
import asyncio
from aiohttp_session import get_session
from aiohttp import web


@asyncio.coroutine
def handler(request):
    session = yield from get_session(request)
    session['last_visit'] = time.time()
    print(session)
    if session.new:
        return web.Response(body=b'Hello newby')
    return web.Response(body=b'I\'ve seen you before')