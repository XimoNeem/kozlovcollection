from django.shortcuts import render

def index(request):
    return render(request, 'collection/index.html', {})

def artist_page(request):
    return render(request, 'temp/page-template.html')