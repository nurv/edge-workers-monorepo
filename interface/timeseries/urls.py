from django.contrib import admin
from django.urls import path, re_path
from timeseries import views

app_name = 'timeseries'

urlpatterns = [
    re_path('(?P<id>([a-f\d]{24}))/delete', views.delete, name="delete"),
    re_path('(?P<id>([a-f\d]{24}))', views.view, name="view"),
    path('', views.list, name="list"),
]