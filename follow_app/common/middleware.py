from django.http import HttpResponse
from django.conf import settings


class HealthcheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health/":
            return HttpResponse("ok")
        return self.get_response(request)


class VersionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/version/":
            return HttpResponse(settings.VERSION)
        return self.get_response(request)
