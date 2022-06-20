import json

import pymongo
import requests
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from datasets.generateDataset import generateDataset
from datasets.models import Dataset
from datasets.forms import DatasetForm

client = pymongo.MongoClient("mongodb://localhost:27017/")

def show(req: HttpRequest, id: str):
    return render(req, "show_datasets.html", {
        "object": get_object_or_404(Dataset, id=id)
    })

def list(req: HttpRequest):
    if req.method == "GET":
        return render(req, "list_datasets.html", {
            "objects": Dataset.objects.all(),
            "collections": client['timeseriesdbs']['dbs'].find({}),
            "form": DatasetForm()
        })
    else:
        payload = json.loads(req.body)
        dbdb = client['timeseriesdbs']
        collection = dbdb[payload['collection']]
        metric = payload['metric']
        window_size = payload['window_size']
        feature = payload['feature']
        train = payload['train']
        vali = payload['vali']
        ds_data, mean, std = generateDataset(collection, metric, feature, window_size=window_size, train=train, vali=vali)
        ds = Dataset(name=payload['feature'], content=ds_data, mean=mean, std=std)
        ds.save()
        return redirect(reverse("datasets:show", args=[ds.id]))


def delete(req: HttpRequest, id: str):
    if req.method == "POST":
        obj = get_object_or_404(Dataset, id=id)
        obj.delete()
        return redirect(reverse("datasets:list"))
