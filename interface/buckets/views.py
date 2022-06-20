from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from buckets.forms import BucketForm
from buckets.models import Bucket


def list(req: HttpRequest):
    if req.method == "GET":
        return render(req, "list_buckets.html", {
            "objects": Bucket.objects.all(),
            "form": BucketForm()
        })
    else:
        form = BucketForm(req.POST)
        if form.is_valid():
            ds = form.save()
            return redirect(reverse("buckets:list")) # , args=[ds.id]))
        else:
            return render(req, "list_buckets.html", {
                "form": BucketForm()
            })

def delete(req: HttpRequest, id: str):
    if req.method == "POST":
        bucket = get_object_or_404(Bucket, id=id)
        bucket.delete()
        return redirect(reverse("buckets:list"))