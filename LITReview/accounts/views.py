from . import forms
from .models import UserFollows, Ticket, Review
from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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
def ticket_create(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.username
            form.save(user)
            return redirect('posts')
    return render(request, 'accounts/ticket.html', context={'form': form})


@login_required
def ticket_edit(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    data = {'title': ticket.title, 'description': ticket.description, 'image': ticket.image}
    form = forms.TicketForm(initial=data)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.edit(ticket)
            return redirect('posts')
    return render(request, 'accounts/ticket.html', context={'form': form})


@login_required
def review_create(request, ticket_id):
    # Create a review for an existing ticket
    # Display and setup Form
    form = forms.ReviewForm()
    ticket = Ticket.objects.get(id=ticket_id)
    # Post request
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        form.set_ticket(ticket)
        if form.is_valid():
            user = request.user.username
            form.save(user)
            return redirect('posts')
    return render(request, 'accounts/review.html', context={'form': form, 'ticket': ticket})


@login_required
def review_ticket_create(request):
    # create a review and an associated ticket
    form = forms.ReviewTicketForm()
    if request.method == 'POST':
        form = forms.ReviewTicketForm(request.POST)
        if form.is_valid():
            user = request.user.username
            form.save(user)
            return redirect('posts')
    return render(request, 'accounts/review.html', context={'form': form})


@login_required
def review_edit(request, review_id):
    review = Review.objects.get(id=review_id)
    data = {'headline': review.headline, 'rating': review.rating, 'body': review.body}
    form = forms.ReviewForm(initial=data)
    ticket = Ticket.objects.get(id=review.ticket.id)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        form.set_ticket(ticket)
        if form.is_valid():
            form.edit(review)
            return redirect('posts')
    return render(request, 'accounts/review.html', {'form': form, 'ticket': ticket})


@login_required
def flux(request):
    # Get follow_user posts
    list_follows = []
    followeds = UserFollows.objects.filter(user=request.user)
    for follow in followeds:
        list_follows.append(follow.followed_user.id)
    follow_tickets = Ticket.objects.filter(user__in=list_follows)
    follow_reviews = Review.objects.filter(user__in=list_follows)

    # Get user posts
    my_tickets = Ticket.objects.filter(user=request.user)
    my_reviews = Review.objects.filter(user=request.user)
    reviewed = []
    for review in my_reviews:
        reviewed.append(review.ticket)

    # Get review to your ticket from non-followed
    reviews_to_my_tickets = Review.objects.filter(ticket__in=my_tickets)
    non_follow_reviews = reviews_to_my_tickets.exclude(user__in=list_follows).exclude(user=request.user)

    # sort and organize
    my_flux = sorted(chain(my_tickets, my_reviews, follow_tickets, follow_reviews, non_follow_reviews),
                     key=lambda x: x.time_created, reverse=True)
    for post in my_flux:
        if hasattr(post, 'ticket'):
            post.type = 'review'
        else:
            post.type = 'ticket'
    return render(request, 'accounts/flux.html', context={'flux': my_flux, 'reviewed': reviewed})


@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    # sort and organize
    user_posts = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)
    for post in user_posts:
        if hasattr(post, 'ticket'):
            post.type = 'review'
        else:
            post.type = 'ticket'
    return render(request, 'accounts/posts.html', context={'posts': user_posts})


@login_required
def post_edit(request, post_type, post_id):
    if post_type == "review":
        return redirect('review_edit', review_id=post_id)
    else:
        return redirect('ticket_edit', ticket_id=post_id)


@login_required
def post_delete(request, post_type, post_id):
    if post_type == "review":
        Review.objects.filter(id=post_id).delete()
    else:
        Ticket.objects.filter(id=post_id).delete()
    return redirect('posts')


@login_required
def follows(request):
    # Affichage Follows
    user = User.objects.get(username=request.user.username)
    followed = UserFollows.objects.filter(user=user)
    follower = UserFollows.objects.filter(followed_user=user)

    # Handling form
    form = forms.FollowForm()
    if request.method == 'POST':
        form = forms.FollowForm(request.POST)
        if form.is_valid():
            form.check_valid(user)
            form.save(user)
    context = {'form': form,
               'followed': followed,
               'follower': follower
               }
    return render(request, 'accounts/follows.html', context=context)


@login_required
def unfollow(request, follow_id):
    user_follow = UserFollows.objects.get(id=follow_id)
    user_follow.delete()
    return redirect('follows')
