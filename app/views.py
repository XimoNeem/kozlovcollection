from django.shortcuts import render
from .models import Artist, Artwork, Route
from collections import defaultdict
from django.shortcuts import get_object_or_404

def get_collection(request):
    return render(request, 'collection/index.html')

def get_artist(request, artist_id):
    data = get_object_or_404(Artist, id=artist_id)  
    return render(request, 'artist/index.html', {'data': data})

def get_artitem(request):
    data = Artwork.objects.get()
    print(data)
    return render(request, 'artitem/index.html', {'data': data})

def get_news(request):
    return render(request, 'temp/page-template.html')

def get_artist_list(request):
    artists = Artist.objects.all().order_by('name')
    
    data = defaultdict(list)
    for artist in artists:
        first_letter = artist.name[0].upper()
        data[first_letter].append(artist)

    # Преобразуем defaultdict в обычный словарь
    data = dict(data)

    return render(request, 'artist_list/index.html', {'data': data})

# Новые представления

def get_collection_by_period(request):
    data = Route.objects.all()
    return render(request, 'routes/index.html', {'data': data})

def get_collection_by_years(request):
    return render(request, 'collection/years.html')

def get_home_anton(request):
    return render(request, 'home_anton/index.html')

def get_team(request):
    return render(request, 'team/index.html')

def get_exhibitions(request):
    return render(request, 'exhibitions/index.html')

def get_exhibition_participation(request):
    return render(request, 'exhibitions/participation.html')

def get_own_exhibitions(request):
    return render(request, 'exhibitions/own.html')

def get_publications(request):
    return render(request, 'publications/index.html')

def get_cooperation(request):
    return render(request, 'cooperation/index.html')

def get_press(request):
    return render(request, 'press/index.html')