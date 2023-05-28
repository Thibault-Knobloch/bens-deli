from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("product/<int:pk>", views.product_view, name="product_view"),
    path("internal/", views.internal_view, name="internal_view"),
    path("internal/login", views.login_view, name="login_view"),
    path("internal/create", views.internal_create, name="internal_create"),
    path("internal/edit/<int:pk>", views.internal_edit, name="internal_edit"),
    path('internal/create-size-option/', views.internal_create_size_option, name='internal_create_size_option'),
    path('internal/delete-size-option/', views.internal_delete_size_option, name='internal_delete_size_option'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('delete-review/', views.delete_review, name='delete_review'),
]
