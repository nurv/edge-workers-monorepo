import json

import pymongo
import requests
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from buckets.models import Bucket
from function.models import Function

# Create your views here.

client = pymongo.MongoClient("mongodb://localhost:27017/")

def list(req: HttpRequest):
        res = requests.get("http://localhost:5001/master")

        return render(req, "list_workers.html", {
            "objects": res.json()['workers']
        })

def apilist(req: HttpRequest):
    res = requests.get("http://localhost:5001/master")
    a = res.json()
    return JsonResponse(a)

def deploy(req: HttpRequest):
    print("Deploy")
    dbdb = client['timeseriesdbs']
    collection = dbdb['dbs']
    dbs = []
    for db in collection.find({}):
        dbs += [{ "id": str(db['_id']), "name": db['name'] }]
    buckets = []
    for bucket in Bucket.objects.all():
        buckets += [{ "id": str(bucket.id), "name": bucket.name }]
    payload = json.loads(req.body)
    fn = Function.objects.get(id=payload['function'])

    with open(settings.ROOT_BUCKET + "/" + str(fn.id) + ".js", "w") as f:
        f.write(fn.code)

    res = requests.post("http://localhost:5001/master", json={
        "type": "deploy",
        "worker": payload['worker'],
        "dbs": dbs,
        "buckets": buckets,
        "function": payload['function']
    })


    return JsonResponse({"result":"ok"})