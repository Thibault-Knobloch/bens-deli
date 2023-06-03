from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login_view, name="user_login_view"),
    path("register/", views.register_view, name="register_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("profile/", views.profile_view, name="profile_view"),
]