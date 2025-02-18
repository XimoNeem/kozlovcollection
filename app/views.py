from django.shortcuts import render
from .models import Artist, Artwork, Route, PressMention, FlowEvent, Employee, PostalLink, Exhibition
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.http import HttpRequest

def get_collection(request):
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/collection/collection.html', {'is_mobile': is_mobile})

def get_artist(request, artist_id):
    data = get_object_or_404(Artist, id=artist_id)  
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/artist.html', {'data': data, 'is_mobile': is_mobile})

def get_artwork(request, artwork_id):
    data = get_object_or_404(Artwork, id=artwork_id) 
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/artwork.html', {'data': data, 'is_mobile': is_mobile})

def get_news(request):
    data = PressMention.objects.all().order_by('name')
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/news.html')

def get_artist_list(request):
    artists = Artist.objects.all().order_by('name')
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    data = defaultdict(list)
    for artist in artists:
        first_letter = artist.name[0].upper()
        data[first_letter].append(artist)

    # Преобразуем defaultdict в обычный словарь
    data = dict(data)

    return render(request, 'pages/artist_list.html', {'data': data, 'is_mobile': is_mobile})

# Новые представления

def get_collection_by_period(request):
    data = Route.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'routes/index.html', {'data': data, 'is_mobile': is_mobile})

def get_collection_by_years(request):
    return render(request, 'collection/years.html')

def get_home_anton(request):
    return render(request, 'home_anton/index.html')

def get_team(request):
    data = Employee.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/team.html', {'data': data, 'is_mobile': is_mobile})

def get_exhibition_participation(request):
    data = Exhibition.objects.filter(is_own=False, is_visible=True)
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/exhibitions.html', {'data': data, 'is_mobile': is_mobile})

def get_own_exhibitions(request):
    data = Exhibition.objects.filter(is_own=True, is_visible=True)
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/exhibitions.html', {'data': data, 'is_mobile': is_mobile})

def get_publications(request):
    return render(request, 'publications/index.html')

def get_cooperation(request):
    data = PostalLink.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/cooperation.html', {'data': data, 'is_mobile': is_mobile})

def get_press(request):
    return render(request, 'press/index.html')

def get_flow(request):
    data = FlowEvent.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/flow.html', {'data': data, 'is_mobile': is_mobile})