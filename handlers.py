import asyncio

import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web
from uuid import uuid4
from urllib.parse import parse_qs
unique_pool = set()


@asyncio.coroutine
@aiohttp_jinja2.template('base.jinja2')
def base_handler(request):
    session = yield from get_session(request)
    name = session.get('name')
    if session.new or not name:
        session['name'] = 'None'

    return {'name': name}


@asyncio.coroutine
def set_name_handler(request):
    session = yield from get_session(request)
    data = yield from request.json()
    name = data.get('name')
    # TODO unique names for players
    session['name'] = name
    return web.HTTPOk()


@asyncio.coroutine
def start_new_game_handler(request):
    slug = uuid4()
    if slug in unique_pool:
        yield from start_new_game_handler(request)
    unique_pool.add(str(slug))
    return web.HTTPFound('/game/{}'.format(slug))


@asyncio.coroutine
def game_handler(request):
    game_id = request.match_info['game_id']
    if game_id not in unique_pool:
        return web.HTTPBadRequest()

    qs = parse_qs(request.query_string)
    game_mode = qs.get('type')

    if game_mode is not None:
        if game_mode[0] == 'join':
            yield from join_game(request)
        elif game_mode[0] == 'watch':
            yield from watch_game(request)
    else:
        yield from start_new_game(request)


@asyncio.coroutine
def join_game(request):
    raise NotImplementedError


@asyncio.coroutine
def watch_game(request):
    raise NotImplementedError


@asyncio.coroutine
def start_new_game(request):
    raise NotImplementedError


@asyncio.coroutine
def websocket_handler(request):
    ws = web.WebSocketResponse()
    yield from ws.prepare(request)
    session = yield from get_session(request)
    try:
        while True:
            msg_ws = yield from ws.receive()
            if msg_ws:
                # TODO process game and live chat data.
                ws.send_str('response data')
    except:
        # Error happened
        pass
    finally:
        pass
        # Connection closed
    return ws


@asyncio.coroutine
@aiohttp_jinja2.template('test.jinja2')
def test_handler(request):
    # test websocket connection template
    # TODO refactor as game controller
    pass

__all__ = ["base_handler",
           "set_name_handler",
           "start_new_game_handler",
           "game_handler",
           "test_handler",
           "websocket_handler"]

# TODO email restore session
