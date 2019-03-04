"""This module implements an async rest API"""
from aiohttp import web
import json
import asyncio


async def handle(request):
    response_obj = {'status' : 'success'}
    return web.Response(text=json.dumps(response_obj))

async def new_number(request):
    """Makes a post request for a countdown to begin."""
    try:
        number = request.query['number']
        print("Creating number: ", number)

        response_obj = {'status': 'success'}
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e) }
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_post('/countdown', new_number)

web.run_app(app, port=8081)

