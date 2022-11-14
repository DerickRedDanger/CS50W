from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name="search"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("random", views.Random, name="random"),
    path("editEntry/<str:title>", views.editEntry, name="editEntry"),
    path("<str:title>", views.page,name="page"),
    
    
]
