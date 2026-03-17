from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CardText


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
    card_texts = CardText.objects.all().order_by('id')
    for card in card_texts:
        card.content = card.content or 'Content coming soon'
    return render(request,
                  'destinations.html',
                  {'active_tab': 'destinations',
                   'card_texts': card_texts})


def destinations_details(request, pk):
    card = get_object_or_404(CardText, id=pk)
    return render(request,
                  'destinations-details.html',
                  {'active_tab': 'destinations_details', 'card': card})


# ==============================
# User Authentication
# ==============================
def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()  # ← Use this instead of authenticate()
        login(request, user)
        messages.success(request, f"You are logged in as {user.username}")
        return redirect('index')
    return render(request, 'login.html', {'active_tab': 'login', 'form': form})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    else:
        """
             the else: as an example that although not needed show the end of
             the def function shows the pattern, check the if and if not the
             if go to return render
        """
        return render(request, 'logout.html', {'active_tab': 'logout'})


def confirm_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request,
                  'confirm-logout.html', {'active_tab': 'confirm_logout'})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(
            request, f"Account created for {user.username}! You can log in."
        )
        return redirect('login')
    return render(request, 'register.html',
                  {'active_tab': 'register', 'form': form})
