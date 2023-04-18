from . import forms
from .models import UserFollows
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required


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
    return render(request, 'accounts/flux.html')\



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
