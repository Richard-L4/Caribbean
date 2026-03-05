from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'active_tab': 'index'})


def destinations(request):
    return render(request, 'destinations.html', {'active_tab': 'destinations'})


def destinations_details(request):
    return render(request,
                  'destinations-details.html',
                  {'active_tab': 'destinations_details'})


def login(request):
    return render(request, 'login.html', {'active_tab': 'login'})


def logout(request):
    return render(request, 'logout.html', {'active_tab': 'logout'})
