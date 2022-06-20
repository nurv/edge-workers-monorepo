from django.contrib import admin
from django.urls import path
from function import views

app_name = 'function'

urlpatterns = [
    path('<uuid:id>/delete', views.delete, name="delete"),
    path('<uuid:id>/submit', views.submit_code, name="submit"),
    path('<uuid:id>/', views.edit, name="edit"),
    path('', views.list, name="list"),
]