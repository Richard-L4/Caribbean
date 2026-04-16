from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, RegisterForm, CommentForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CardText, Places, Comment, CommentReaction, Translation, \
      Rating
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg


def index(request):
    return render(request, 'index.html', {'active_tab': 'index'})


def info(request):
    form = ContactForm(request.POST or None)
    # -- use of None so else not
    # -- needed in request before retrun direct
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted")
            return redirect('info')

    return render(request, 'info.html', {'active_tab': 'info', 'form': form})


def destinations(request, pk):
    card = get_object_or_404(CardText, pk=pk)
    language = request.GET.get('lang', 'en')

    # try to get a translation, fall back to original card if none exists
    translation = Translation.objects.filter(
        card=card, language=language).first()
    prev_card = CardText.objects.filter(pk__lt=pk,
                                        pk__gte=2).order_by('-pk').first()
    next_card = CardText.objects.filter(pk__gt=pk).order_by('pk').first()

    return render(request,
                  'destinations.html',
                  {'active_tab': 'destinations',
                   'card': card,
                   'translation': translation,
                   'prev_card': prev_card,
                   'next_card': next_card})


def destinations_details(request, pk):
    card = get_object_or_404(CardText, id=pk)
    places = Places.objects.filter(card=card)
    language = request.GET.get('lang', 'en')

    # get translations for all places on this card
    place_translations = Translation.objects.filter(
        place__in=places,
        language=language
    )
    # turn into a dict so template can look up by place id
    # { place.id: translation }
    translations_by_place = {t.place_id: t for t in place_translations}

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

    ratings_by_place = {}
    for p in places:

        avg = p.ratings.aggregate(avg=Avg('rating'))['avg']
        count = p.ratings.count()
        user_rating = None

        if request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                place=p, user=request.user
            ).first()
        ratings_by_place[p.id] = {
            'average_rating': avg,
            'rating_count': count,
            'user_rating': user_rating
        }
    return render(request,
                  'destinations-details.html',
                  {'active_tab': 'destinations_details',
                   'card': card,
                   'places': places,
                   'comments': comments,
                   'form': form,
                   'translations_by_place': translations_by_place,
                   'language': language,
                   'ratings_by_place': ratings_by_place})


@login_required
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


@login_required
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


# ==============================
# Comment Reactions (Like/Dislike)
# ==============================
@login_required
def toggle_reaction(request, comment_id, reaction_type):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    comment = get_object_or_404(Comment, id=comment_id)
    with transaction.atomic():
        existing = CommentReaction.objects.filter(user=request.user,
                                                  comment=comment).first()
        if existing:
            if existing.reaction != reaction_type:
                existing.reaction = reaction_type
                existing.save()
                status = 'changed'
            else:
                status = 'unchanged'
        else:
            CommentReaction.objects.create(user=request.user, comment=comment,
                                           reaction=reaction_type)
            status = 'added'

        likes_count = comment.reactions.filter(reaction='like').count()
        dislikes_count = comment.reactions.filter(reaction='dislike').count()

    return JsonResponse({'status': status, 'likes': likes_count,
                         'dislikes': dislikes_count})


@login_required
def rating(request, pk):
    if request.method == 'POST':
        place = get_object_or_404(Places, pk=pk)
        rating_value = int(request.POST.get('rating', 0))
        if rating_value < 1 or rating_value > 5:
            return redirect('destination-details', pk=place.card.pk)

        # Create / update rating
        Rating.objects.update_or_create(
            place=place,
            user=request.user,
            defaults={'rating': rating_value}
        )
        return redirect('destinations-details', pk=place.card.pk)
    return redirect('index')
