from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_collection, name='collection'),
    path('artist/<int:artist_id>/', views.get_artist, name='artist_detail'), 
    path('artwork/<int:artwork_id>/', views.get_artwork, name='artwork'), 
    path('period/<int:period_id>/', views.get_period, name='period'), 

    path('news/', views.get_news, name='news'), 
    path('artistlist/', views.get_artist_list, name='collection_a_z'),  # A - Я (список художников)

    # path('m1-m10/', views.get_collection_by_period, name='collection_m1_m10'),  # M.1 — M.10
    path('1957-2057/', views.get_collection_by_years, name='collection_by_years'),  # 1957 — 2057
    
    path('home-anton/', views.get_videos, name='home_anton'),  # ПОКА ВСЕ ДОМА У АНТОНА
    path('team/', views.get_team, name='team'),  # КОМАНДА

    # Подразделы выставок
    path('exhibitions_participation/', views.get_exhibition_participation, name='exhibitions_participation'),  # УЧАСТИЕ В ПРОЕКТАХ
    path('own_exhibitions/', views.get_own_exhibitions, name='own_exhibitions'),  # СОБСТВЕННАЯ ВЫСТАВОЧНАЯ ПРОГРАММА

    path('publications/', views.get_publications, name='publications'),  # ИЗДАНИЯ
    path('cooperation/', views.get_cooperation, name='cooperation'),  # СОТРУДНИЧЕСТВО
    path('press/', views.get_press, name='press'),  # ПРЕССА
    path('flow/', views.get_flow, name='flow'),  # ПРЕССА

    path("routes/", views.get_routes, name="routes"),
]