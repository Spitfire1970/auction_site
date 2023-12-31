from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.add_listing, name="add_listing"),
    path("listings/<int:listing_num>", views.show_listing, name = "listing"),
    path("categories", views.categories, name = "categories"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("categories/<str:categoryy>", views.category, name = "category")
]
