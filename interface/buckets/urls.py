from django.contrib import admin
from django.urls import path
from buckets import views

app_name = 'buckets'

urlpatterns = [
    # path('<uuid:id>/', views.show, name="show"),
    path('<uuid:id>/delete', views.delete, name="delete"),
    path('', views.list, name="list"),
]