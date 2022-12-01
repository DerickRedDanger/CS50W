from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/comment/<int:id>", views.comment, name="comment"),
    path("listing/follow/<int:id>", views.follow, name="follow"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("new/", views.new,name="new"),
    path("category/", views.categories,name="categories"),
    path("category/<int:id>", views.Category,name="Category"),
    path("close/<int:id>", views.close,name="close"),
    path("watchlist/", views.watchlist,name="watchlist"),
]
