import datetime
import io
import csv
import json
import uuid

import aiohttp
import pymongo
from bson import ObjectId
from aiohttp import web, WSCloseCode
import asyncio
from os.path import exists
CONNECTIONS = {}


client = pymongo.MongoClient("mongodb://localhost:27017/")

class Worker(object):
    def __init__(self, ws):
        self.id = uuid.uuid4()
        self.name = "unidentified"
        self.ws = ws

async def http_handler(request):
    global CONNECTIONS
    if request.method == "GET":
        return web.json_response({
            'workers': [{"id": str(w.id), "name": w.name} for w in CONNECTIONS.values()]
        })
    elif request.method == "POST":
        r = await request.json()
        await CONNECTIONS[r['worker']].ws.send_str(json.dumps({
            "type": "deploy",
            "dbs": r['dbs'],
            "buckets": r['buckets'],
            "id": r['function']
        }))
        return web.json_response({})


async def database(request):
    dbdb = client['timeseriesdbs']
    collection = dbdb['dbs']
    if request.method == "POST":
        r = await request.json()
        object = collection.find_one({
            "_id": ObjectId(r['db'])
        })
        dbdb[object['name']].insert_one({
            "metadata": r['metadata'],
            "metrics": r['metrics'],
            "timestamp": datetime.datetime.now()
        })
        return web.json_response({})


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    wrk = Worker(ws)
    CONNECTIONS[str(wrk.id)] = wrk

    while True:
        try:
            msg = await ws.receive()
            print(msg)
            if msg.type == aiohttp.WSMsgType.TEXT:
                content = json.loads(msg.data)
                if content['type'] == "auth":
                    wrk.name = content['name']
            elif msg.type == aiohttp.WSMsgType.CLOSE or msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
        except:
            print("ERROR")

    del CONNECTIONS[str(wrk.id)]
    return ws


def create_runner():
    app = web.Application()
    app.add_routes([
        web.view('/master',   http_handler),
        web.view('/database', database),
        web.get('/ws/worker', websocket_handler),
    ])
    return app

if __name__ == '__main__':
    web.run_app(create_runner(), port=5001)
