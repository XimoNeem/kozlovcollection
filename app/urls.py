from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_collection, name='collection'),  # КОЛЛЕКЦИЯ
    path('artist/<int:artist_id>/', views.get_artist, name='artist_detail'),  # Детали художника
    path('artitem/', views.get_artitem, name='artitem'),  # Отдельный объект искусства
    path('news/', views.get_news, name='news'),  # Новости (если они были)
    path('artistlist/', views.get_artist_list, name='collection_a_z'),  # A - Я (список художников)

    # Новые маршруты на основе меню
    path('collection/m1-m10/', views.get_collection_by_period, name='collection_m1_m10'),  # M.1 — M.10
    path('collection/a-z/', views.get_artist_list, name='collection_a_z'),  # Дублируется A — Я
    path('collection/1957-2057/', views.get_collection_by_years, name='collection_by_years'),  # 1957 — 2057
    
    path('home-anton/', views.get_home_anton, name='home_anton'),  # ПОКА ВСЕ ДОМА У АНТОНА
    path('team/', views.get_team, name='team'),  # КОМАНДА
    path('exhibitions/', views.get_exhibitions, name='exhibitions'),  # ВЫСТАВКИ

    # Подразделы выставок
    path('exhibitions/participation/', views.get_exhibition_participation, name='exhibition_participation'),  # УЧАСТИЕ В ПРОЕКТАХ
    path('exhibitions/own/', views.get_own_exhibitions, name='own_exhibitions'),  # СОБСТВЕННАЯ ВЫСТАВОЧНАЯ ПРОГРАММА

    path('publications/', views.get_publications, name='publications'),  # ИЗДАНИЯ
    path('cooperation/', views.get_cooperation, name='cooperation'),  # СОТРУДНИЧЕСТВО
    path('press/', views.get_press, name='press'),  # ПРЕССА
]