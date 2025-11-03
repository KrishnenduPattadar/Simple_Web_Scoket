from django.urls import path
from market.views import market_live_view

urlpatterns = [
    path("market/live/", market_live_view, name="market_live"),
]