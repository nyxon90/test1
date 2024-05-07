# server.py

import asyncio
import aiohttp
from aiohttp import web
import hashlib
import click


async def healthcheck(request):
    return web.json_response({})


async def hash_string(request):
    try:
        data = await request.json()
        if 'string' not in data:
            return web.json_response({'validation_errors': 'Missing required field'}, status=400)

        string_to_hash = data['string']
        hashed_string = hashlib.sha256(string_to_hash.encode()).hexdigest()

        return web.json_response({'hash_string': hashed_string})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)


@click.command()
@click.option('--host', default='localhost', help='Host of the server')
@click.option('--port', default=8080, help='Port of the server')
def run_server(host, port):
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', hash_string)
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
