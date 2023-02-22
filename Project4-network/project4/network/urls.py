
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("edit", views.edit, name="edit"),
    path("getpposts", views.getpposts, name="getpposts"),
    path("follow/<int:id>/<str:f>", views.follow, name="follow"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("like/<int:id>", views.like, name="like"),
    path("description/<int:id>", views.description, name="description"), 
    path("getpost/<int:id>", views.getpost, name="post"),

]
