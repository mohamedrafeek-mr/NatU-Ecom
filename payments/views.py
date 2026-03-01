from django.http import HttpResponse


def callback(request):
    # payment gateway will POST here; verify signature etc.
    return HttpResponse('OK')
