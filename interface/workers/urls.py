from django.contrib import admin
from django.urls import path
from workers import views

app_name = 'workers'

urlpatterns = [
    path('', views.list, name="list"),
    path('api', views.apilist, name="api-list"),
    path('deploy', views.deploy, name="deploy"),
]