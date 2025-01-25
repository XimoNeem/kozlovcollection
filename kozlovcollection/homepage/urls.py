from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # главная страница
    path('artist/', views.artist_page, name='artist'),  # страница /artist
]