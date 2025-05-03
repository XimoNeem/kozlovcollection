from django.shortcuts import redirect
from django.conf import settings

class SimpleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = ['/login/']  # Страница логина без защиты

        if request.path not in allowed_paths and 'authenticated' not in request.session:
            return redirect('/login/')

        return self.get_response(request)