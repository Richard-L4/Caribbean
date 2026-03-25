from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, RegisterForm, CommentForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CardText, Places, Comment


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


def destinations(request, pk):
    card = get_object_or_404(CardText, pk=pk)

    prev_card = CardText.objects.filter(pk__lt=pk,
                                        pk__gte=2).order_by('-pk').first()
    next_card = CardText.objects.filter(pk__gt=pk).order_by('pk').first()

    return render(request,
                  'destinations.html',
                  {'active_tab': 'destinations',
                   'card': card,
                   'prev_card': prev_card,
                   'next_card': next_card})


def destinations_details(request, pk):
    card = get_object_or_404(CardText, id=pk)
    places = Places.objects.filter(card=card)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        place = get_object_or_404(Places, id=place_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.places = place
            comment.save()
            return redirect('destinations-details', pk=card.pk)

    comments = Comment.objects.filter(places__card=card).order_by('created_at')
    return render(request,
                  'destinations-details.html',
                  {'active_tab': 'destinations_details',
                   'card': card,
                   'places': places,
                   'comments': comments,
                   'form': form})


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('destinations-details', pk=comment.places.card.pk)
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('destinations-details', pk=comment.places.card.pk)
    return render(request, 'edit-comment.html',
                  {'active_tab': 'edit-comment',
                   'form': form,
                   'comment': comment})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('destinations-details', pk=comment.places.card.pk)

    if request.method == 'POST':
        card_pk = comment.places.card.pk
        comment.delete()
        return redirect('destinations-details', card_pk)

    return render(request,
                  'delete-comment.html', {'active_tab': 'delete-comment',
                                          'comment': comment})


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
