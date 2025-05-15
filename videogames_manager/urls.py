from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_view, name="logout"),
    path("accounts/", include("allauth.urls")),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("get_games_data/", views.get_games_data, name="get_games_data"),
    path("game/<int:game_id>", views.game_detail, name="game_detail"),
    path("follow_game/<int:game_id>", views.follow_game, name="follow_game"),
    path("search_games/", views.search_games, name="search_games"),
    path('accounts/confirm-email/<uidb64>/<token>/', views.confirm_email, name='account_confirm_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)