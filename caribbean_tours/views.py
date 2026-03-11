from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html', {'active_tab': 'index'})


def info(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted")
            return redirect('info')
    else:
        form = ContactForm()
    return render(request, 'info.html', {'active_tab': 'info', 'form': form})


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


def confirm_logout(request):
    return render(request,
                  'confirm-logout.html', {'active_tab': 'confirm_logout'})


def register(request):
    return render(request, 'register.html', {'active_tab': 'register'})
