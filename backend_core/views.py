from django.http import HttpResponse


def ping(request):
    return HttpResponse('pong', content_type='text/plain')


def favicon(request):
    return HttpResponse(status=204)
