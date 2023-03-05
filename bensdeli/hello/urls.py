from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('people/', views.person_list, name='person_list'),
    path('people/create/', views.person_create, name='person_create'),
]
