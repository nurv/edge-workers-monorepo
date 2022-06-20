import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from function.models import Function
from function.forms import FunctionNameForm


def edit(req: HttpRequest, id: str):
    if req.method == "GET":
        return render(req, "edit_function.html", {
            "object": get_object_or_404(Function, id=id)
        })
    else:
        fn = get_object_or_404(Function, id=id)
        payload = json.loads(req.body)
        fn.code = payload['code']
        fn.save()
        return JsonResponse({'result': 'ok'})


def list(req: HttpRequest):
    if req.method == "GET":
        return render(req, "list_function.html", {
            "objects": Function.objects.all(),
            "form": FunctionNameForm()
        })
    else:
        form = FunctionNameForm(req.POST)
        if form.is_valid():
            ds = form.save()
            return redirect(reverse("function:edit", args=[ds.id]))
        else:
            return render(req, "list_function.html", {
                "form": FunctionNameForm()
            })


@csrf_exempt
def submit_code(req: HttpRequest, id: str):
    fn = get_object_or_404(Function, id=id)
    payload = json.loads(req.body)
    fn.code = payload['code']
    fn.save()
    return JsonResponse({'result': 'ok'})


def delete(req: HttpRequest, id: str):
    if req.method == "POST":
        obj = get_object_or_404(Function, id=id)
        obj.delete()
        return redirect(reverse("function:list"))
