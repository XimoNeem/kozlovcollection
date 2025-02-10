from django.shortcuts import render
from .models import Artist

def get_collection(request):
    data = Artist.objects.get()
    print(data)
    return render(request, 'collection/index.html', {'data': data})

def get_artist(request):
    data = Artist.objects.get()
    print(data)
    return render(request, 'artist/index.html', {'data': data})

def get_artitem(request):
    return render(request, 'temp/page-template.html')

def get_news(request):
    return render(request, 'temp/page-template.html')