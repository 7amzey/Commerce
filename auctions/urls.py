from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:auction_id>", views.listing_page, name="listing_page"),
    path("<int:auction_id>/bidding", views.bidding, name="bidding"),
    path("<int:auction_id>/closing", views.closing, name="closing"),
    path("<int:auction_id>/confirm_closing", views.confirm_closing, name="confirm_closing"),
    path("<int:auction_id>/comment", views.comments, name="comment"),
    path("categories", views.category, name="category"),
    path("categories/<str:name>", views.auction_by_category, name="auction_by_category"),
    path("<int:auction_id>/", views.watchlists, name="watchlists"),
    path("watchlist", views.watchlist_page, name="watchlist_page"),
    path("search", views.search_bar, name="search_bar"),
    path("closed_auctions", views.closed_auctions, name="closed"),
    path("<str:username>/auctions", views.my_auctions, name="myauctions")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
