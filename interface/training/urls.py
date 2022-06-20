from django.contrib import admin
from django.urls import path
from training import views

app_name = 'training'

urlpatterns = [
    path('<uuid:id>/delete', views.delete, name="delete"),
    path('<uuid:id>/', views.edit, name="edit"),
    path('<uuid:id>/input', views.inputFeature, name="input"),
    path('<uuid:id>/output', views.outputFeature, name="output"),
    path('input/<uuid:id>', views.deleteInputFeature, name="inputFeature"),
    path('output/<uuid:id>', views.deleteOutputFeature, name="outputFeature"),
    path('<uuid:id>/models', views.deleteVersionFeature, name="deleteVersionFeature"),
    path('<uuid:id>/train', views.train, name="train"),
    path('model/<uuid:id>', views.view_model, name="model"),
    path('', views.list, name="list"),
]