from django.shortcuts import render, get_object_or_404, redirect
from .models import Artist, Artwork, Route, PressMention, FlowEvent, Employee, PostalLink, Exhibition, YearPeriod, VideoSet
from collections import defaultdict
from django.http import HttpRequest
import re



def get_main(request):
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/collection/collection.html', {'is_mobile': is_mobile})

def get_collection(request):
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/main.html', {'is_mobile': is_mobile})

from django.shortcuts import get_object_or_404
from django.shortcuts import render

def get_artist(request, artist_id):
    data = get_object_or_404(Artist, id=artist_id)
    
    # Определяем, является ли запрос мобильным
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    
    # Сортируем работы в зависимости от флага is_mobile
    if is_mobile:
        artworks = data.artworks.all().order_by('order_mobile')  # Сортировка для мобильных
    else:
        artworks = data.artworks.all().order_by('order_desktop')  # Сортировка для десктопов

    # Передаем отсортированные данные в шаблон
    return render(request, 'pages/artist.html', {'data': data, 'artworks': artworks, 'is_mobile': is_mobile})


def get_artwork(request, artwork_id):
    data = get_object_or_404(Artwork, id=artwork_id) 

    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']

    artworks_by_artist = list(
        Artwork.objects.filter(artist=data.artist).order_by('created_at')
    )

    # Находим индекс текущей работы в списке
    current_index = next((i for i, artwork in enumerate(artworks_by_artist) if artwork.id == data.id), None)

    previous_artwork = None
    next_artwork = None

    if current_index is not None:
        total = len(artworks_by_artist)
        previous_index = (current_index - 1) % total
        next_index = (current_index + 1) % total

        previous_artwork = artworks_by_artist[previous_index]
        next_artwork = artworks_by_artist[next_index]

    neighboring_artworks_ids = {
        'previous': previous_artwork.id if previous_artwork else None,
        'next': next_artwork.id if next_artwork else None
    }

    return render(request, 'pages/artwork.html', {
        'data': data,
        'is_mobile': is_mobile,
        'neighboring_artworks_ids': neighboring_artworks_ids
    })

def get_period(request, period_id):
    data = get_object_or_404(YearPeriod, id=period_id) 

    previous_route = YearPeriod.objects.filter(id__lt=period_id).order_by('-id').first()
    next_route = YearPeriod.objects.filter(id__gt=period_id).order_by('id').first()

    if not previous_route:
        previous_route = YearPeriod.objects.order_by('-id').first()  # Последний период, если нет предыдущего

    if not next_route:
        next_route = YearPeriod.objects.order_by('id').first()  # Первый период, если нет следующего

    def modify_title(route):
        if route:
            match = re.match(r'(M\.\d+)', route.title)
            route.title = match.group(1) if match else route.title
        return route

    header_data = {
        'current': data,
        'previous': modify_title(previous_route),
        'next': modify_title(next_route)
    }

    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    
    return render(request, 'pages/period.html', {
        'data': data,
        'is_mobile': is_mobile,
        'header_data': header_data
    })

def get_route(request, route_id):
    data = get_object_or_404(Route, id=route_id)

    previous_route = Route.objects.filter(id__lt=route_id).order_by('-id').first()
    next_route = Route.objects.filter(id__gt=route_id).order_by('id').first()

    if not previous_route:
        previous_route = Route.objects.order_by('-id').first()  # Последний маршрут, если нет предыдущего

    if not next_route:
        next_route = Route.objects.order_by('id').first()  # Первый маршрут, если нет следующего

    def modify_title(route):
        if route:
            match = re.match(r'(M\.\d+)', route.title)
            route.title = match.group(1) if match else route.title
        return route

    header_data = {
        'current': data,
        'previous': modify_title(previous_route),
        'next': modify_title(next_route)
    }

    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    
    return render(request, 'pages/route.html', {
        'data': data,
        'is_mobile': is_mobile,
        'header_data': header_data
    })

def get_exhibition(request, exhibition_id):
    data = get_object_or_404(Exhibition, id=exhibition_id) 
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/exhibition.html', {'data': data, 'is_mobile': is_mobile})

def get_article(request, article_id):
    data = get_object_or_404(Route, id=article_id) 
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/article.html', {'data': data, 'is_mobile': is_mobile})

def get_news(request):
    data = PressMention.objects.all().order_by('name')
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/press.html')

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

def get_routes(request):
    data = Route.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/routes.html', {'data': data, 'is_mobile': is_mobile})


def get_collection_by_period(request):
    data = Route.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'routes/index.html', {'data': data, 'is_mobile': is_mobile})

def get_collection_by_years(request):
    data = YearPeriod.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/collection/years.html', {'data': data, 'is_mobile': is_mobile})

def get_videos(request):
    data = VideoSet.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/videos.html', {'data': data, 'is_mobile': is_mobile})

def get_team(request):
    data = Employee.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/team.html', {'data': data, 'is_mobile': is_mobile})

def get_exhibition_participation(request):
    data = Exhibition.objects.filter(is_own=False, is_visible=True)
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/exhibitions.html', {'data': data, 'is_mobile': is_mobile, 'is_own': False,})

def get_exhibitions_list(request):
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/exhibition_switch.html', {'is_mobile': is_mobile})

def get_own_exhibitions(request):
    data = Exhibition.objects.filter(is_own=True, is_visible=True)
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/exhibitions.html', {'data': data, 'is_mobile': is_mobile, 'is_own': True,})

def get_publications(request):
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/publications.html', {'is_mobile': is_mobile})

def get_cooperation(request):
    data = PostalLink.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/cooperation.html', {'data': data, 'is_mobile': is_mobile})

def get_press(request):
    data = PressMention.objects.filter(is_visible=True)
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/press.html', {'data': data, 'is_mobile': is_mobile})

def get_flow(request):
    data = FlowEvent.objects.all()
    is_mobile = request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META['HTTP_USER_AGENT']
    return render(request, 'pages/flow.html', {'data': data, 'is_mobile': is_mobile})

def custom_404_view(request):
    return render(request, "pages/404.html", status=404)

def get_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "exhibition" and password == "2425":
            request.session['authenticated'] = True
            return redirect('/')

    return render(request, "pages/login.html")