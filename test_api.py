import pytest
from aiohttp import web
from server import healthcheck, hash_string

@pytest.fixture
async def cli(aiohttp_client):
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', hash_string)
    return await aiohttp_client(app)

async def test_healthcheck(cli):
    resp = await cli.get('/healthcheck')
    assert resp.status == 200
    text = await resp.text()
    assert text == '{}'

async def test_hash_string(cli):
    data = {'string': 'test'}
    resp = await cli.post('/hash', json=data)
    assert resp.status == 200
    result = await resp.json()
    assert 'hash_string' in result
