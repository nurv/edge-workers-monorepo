from bson import ObjectId
from django.http import HttpRequest
from django.shortcuts import render, redirect

import pymongo
from django.urls import reverse

from timeseries.forms import TSDBForm

client = pymongo.MongoClient("mongodb://localhost:27017/")


def list(req: HttpRequest):
    dbdb = client['timeseriesdbs']
    collection = dbdb['dbs']
    if req.method == "GET":
        return render(req, "list_timeseries.html", {
            "objects": collection.find({}),
            "form": TSDBForm()
        })
    else:
        form = TSDBForm(req.POST)
        if form.is_valid():
            object = collection.insert_one({
                "name": form.cleaned_data['name']
            })
            dbdb.create_collection(form.cleaned_data['name'], timeseries={
                "timeField": "timestamp",
                "metaField": "metadata",
                "granularity": "hours"
            })
            return redirect(reverse("timeseries:view", args=[object.inserted_id]))
        else:
            return render(req, "list_training.html", {
                "form": TSDBForm()
            })


def view(req, id):
    dbdb = client['timeseriesdbs']
    collection = dbdb['dbs']
    object = collection.find_one({
        "_id": ObjectId(id)
    })
    return render(req, "view_timeseries.html", {
        "object": object,
        "count": dbdb[object['name']].count_documents({}),
        "objects": dbdb[object['name']].find({})
    })

def delete(req, id):
    dbdb = client['timeseriesdbs']
    collection = dbdb['dbs']
    if req.method == "POST":
        object = collection.find_one({
            "_id": ObjectId(id)
        })
        collection.delete_one({"_id": ObjectId(id)})
        dbdb.drop_collection(object['name'])
        return redirect(reverse("timeseries:list"))
