from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listingPage/<int:id>", views.listingPage, name="listingPage"),
    path("watchListRemove/<int:id>", views.watchListRemove, name="watchListRemove"),
    path("watchListAdd/<int:id>", views.watchListAdd, name="watchListAdd"),
    path("watchListPage", views.watchListPage, name="watchListPage"),
    path("commentSection/<int:id>", views.commentSection, name="commentSection"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("auctionClosed/<int:id>", views.auctionClosed, name="auctionClosed"),
]
