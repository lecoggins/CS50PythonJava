from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create"),
    path("category_listings", views.category_listings, name="category_listings"),
    path("watchlist_category_listings", views.watchlist_category_listings, name="watchlistCategory_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="addWatchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="removeWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]
