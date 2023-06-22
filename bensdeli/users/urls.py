from django.urls import path
from . import views
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView


urlpatterns = [
    path("login/", views.user_login_view, name="user_login_view"),
    path("register/", views.register_view, name="register_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("profile/", views.profile_view, name="profile_view"),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]