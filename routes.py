from handlers import *
from aiohttp.web import Request


def route(method, url, handler, **kwargs):
    return dict(
        method=method,
        url=url,
        handler=handler,
        kwargs_=kwargs
    )

routes = [
    route('POST', '/setname', set_name_handler, name='set_name', expect_handler=Request.json),
    route('GET', '/', base_handler, name='base_handler'),
    route('GET', '/start_new_game', start_new_game_handler, name='new_game'),
    route('GET', '/game/{game_id}', game_handler, name='game'),
    route('GET', '/ws', websocket_handler, name='websocket'),
    route('GET', '/test', test_handler)
]
