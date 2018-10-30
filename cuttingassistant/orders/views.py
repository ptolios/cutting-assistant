from django.http import HttpResponse


def orders(request):
    return HttpResponse('This is the orders page...')
