from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("product/<int:pk>", views.product_view, name="product_view"),
    path("internal/", views.internal_view, name="internal_view"),
    path("internal/login", views.login_view, name="login_view"),
    path("internal/create", views.internal_create, name="internal_create"),
    path("internal/edit/<int:pk>", views.internal_edit, name="internal_edit"),
]
