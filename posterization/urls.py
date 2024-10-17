# Define a URL make_poster/ que chama a view create_posters do app posterization.

from django.urls import path
from . import views

urlpatterns = [
    path('make_poster/', views.create_posters, name='create_poster'),  # View web
    path('api/make_poster/', views.CreatePostersView.as_view(), name='create_poster_api'),  # View API
]