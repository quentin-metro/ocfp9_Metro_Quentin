from . import forms
from .models import UserFollows, Ticket, Review
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from itertools import chain


def logout_user(request):
    logout(request)
    return redirect('login')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'accounts/signup.html', context={'form': form})


@login_required
def flux(request):
    return render(request, 'accounts/flux.html')


@login_required
def ticket_create(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.username
            form.save(user)
    return render(request, 'accounts/ticket.html', context={'form': form})


@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    user_posts = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)
    for post in user_posts:
        if hasattr(post, 'ticket'):
            post.type = 'review'
        else:
            post.type = 'ticket'
    return render(request, 'accounts/posts.html', context={'posts': user_posts})


@login_required
def alter_post(request, post_type, post_id):
    return redirect('posts')


@login_required
def delete_post(request, post_type, post_id):
    if post_type == "review":
        Review.objects.filter(id=post_id).delete()
    else:
        Ticket.objects.filter(id=post_id).delete()
    return redirect('posts')


@login_required
def abonnements(request):
    # Affichage Follows
    user = request.user.username
    followed = UserFollows.objects.filter(user=request.user)
    follower = UserFollows.objects.filter(followed_user=request.user)
    # Handling form
    form = forms.FollowForm()
    if request.method == 'POST':
        form = forms.FollowForm(request.POST)
        if form.is_valid():
            form.save(user)
            # raise relation already exist error
    context = {'form': form,
               'followed': followed,
               'follower': follower
               }
    return render(request, 'accounts/abonnements.html', context=context)


@login_required
def unfollow(request, follow_id):
    user_follow = UserFollows.objects.get(id=follow_id)
    user_follow.delete()
    return abonnements(request)
