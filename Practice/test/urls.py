from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("section/<int:num>", views.section, name="Section"),
    path("re", views.reindex, name="reindex"),
    path("posts", views.posts, name="posts")
]