from django.contrib import admin
from django.urls import path
from datasets import views

app_name = 'datasets'

urlpatterns = [
    path('<uuid:id>/delete', views.delete, name="delete"),
    path('<uuid:id>/', views.show, name="show"),
    path('', views.list, name="list"),
]