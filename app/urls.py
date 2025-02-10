from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_collection, name='collection'),
    path('artist/', views.get_artist, name='artist'),
    path('artitem/', views.get_artitem, name='artitem'),
    path('news/', views.get_news, name='news'),
]