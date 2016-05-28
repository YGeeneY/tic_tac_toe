import asyncio
import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web
from uuid import uuid4

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
    if game_id in unique_pool:
        return web.Response(
            text="Game_id, {}".format(game_id))
    return web.HTTPBadRequest()


__all__ = ["base_handler",
           "set_name_handler",
           "start_new_game_handler",
           "game_handler"]