from django.shortcuts import render

def set_route(request):
    return render(request, 'set_route.html')
