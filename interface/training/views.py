import base64
import json
import os

import humanize
from django.conf import settings
from django.contrib.sites import requests
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from buckets.models import Bucket
from training.forms import MLModelForm, MLModelDatasetForm, InputFeatureForm, OutputFeatureForm, MLModelVersionForm
from training.models import MLModel, MLModelDataset, InputFeatures, OutputFeatures, MLModelVersion


def list(req: HttpRequest):
    if req.method == "GET":
        return render(req, "list_training.html", {
            "objects": MLModel.objects.all(),
            "form": MLModelForm()
        })
    else:
        form = MLModelForm(req.POST)
        if form.is_valid():
            train = form.save()
            if not train.bucket:
                train.bucket = str(train.id)
                train.save()
            bucket = Bucket(name=train.bucket)
            bucket.save()
            return redirect(reverse("training:edit", args=[train.id]))
        else:
            return render(req, "list_training.html", {
                "form": MLModelForm()
            })


def edit(req: HttpRequest, id: str):
    if req.method == "GET":
        model = get_object_or_404(MLModel, id=id)
        form = MLModelDatasetForm(initial={'model': model.pk})
        form.fields['model'].queryset = MLModel.objects.filter(id=id)
        form.fields['dataset'].label_from_instance = lambda x: x.name
        trainform = MLModelVersionForm(initial={'model': model.pk})
        trainform.fields['dataset'].label_from_instance = lambda x: x.dataset.name
        return render(req, "edit_training.html", {
            "object": model,
            "objects": MLModelDataset.objects.filter(model=model),
            "datasetform": form,
            "inputform": InputFeatureForm(initial={'model': model.pk}),
            "outputform": OutputFeatureForm(initial={'model': model.pk}),
            "trainform": trainform
        })
    else:
        # TODO: theres a sec flaw here
        form = MLModelDatasetForm(req.POST)
        if form.is_valid():
            mldataset = form.save()
            return redirect(reverse("training:edit", args=[id]))


def inputFeature(req: HttpRequest, id: str):
    form = InputFeatureForm(req.POST)
    if form.is_valid():
        mldataset = form.save()
        return redirect(reverse("training:edit", args=[id]))


def deleteInputFeature(req: HttpRequest, id: str):
    if req.method == "POST":
        obj = get_object_or_404(InputFeatures, id=id)
        model_id = obj.model.id
        obj.delete()
        return redirect(reverse("training:edit", args=[model_id]))


def outputFeature(req: HttpRequest, id: str):
    form = OutputFeatureForm(req.POST)
    if form.is_valid():
        mldataset = form.save()
        return redirect(reverse("training:edit", args=[id]))

def deleteOutputFeature(req: HttpRequest, id: str):
    if req.method == "POST":
        obj = get_object_or_404(OutputFeatures, id=id)
        model_id = obj.model.id
        obj.delete()
        return redirect(reverse("training:edit", args=[model_id]))

def deleteVersionFeature(req: HttpRequest, id: str):
    if req.method == "POST":
        obj = get_object_or_404(MLModelVersion, id=id)
        model_id = obj.model.id
        obj.delete()
        return redirect(reverse("training:edit", args=[model_id]))

def train(req: HttpRequest, id: str):
    form = MLModelVersionForm(req.POST)
    if form.is_valid():
        mlversion = form.save()
        mlversion.train()
        return redirect(reverse("training:edit", args=[id]))


def delete(req: HttpRequest, id: str):
    if req.method == "POST":
        obj = get_object_or_404(MLModel, id=id)
        obj.delete()
        return redirect(reverse("training:list"))


def view_model(req: HttpRequest, id: str):
    obj = get_object_or_404(MLModelVersion, id=id)
    data = json.loads(obj.evaluation_result.replace("'", "\""));
    for key, _ in data.items():
        if key != "combined":
            model_bucket = os.path.join(settings.ROOT_BUCKET, obj.model.bucket or str(obj.model.id))
            model_version_path = os.path.join(model_bucket, str(obj.id))
            image_data = open(model_version_path + "/results/" + "learning_curves_" + key + "_loss.png", "rb").read()
            data[key]['loss_img'] = 'data:image/png;base64,{}'.format(base64.b64encode(image_data).decode('ascii'))
    return render(req, "view_model.html", {
        "object": obj,
        "evaluation_result": data,
        "duration": humanize.naturaldelta(obj.trained - obj.created)
    })
