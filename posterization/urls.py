# Define a URL make_poster/ que chama a view create_posters do app posterization.

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('make_poster/', views.create_posters, name='create_poster'),
    path('api/make_poster/', views.CreatePostersView.as_view(), name='create_poster_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
