from django.shortcuts import render

def index(request):
    return render(request, 'homepage/index.html', {})

def artist_page(request):
    return render(request, 'artist/index.html')