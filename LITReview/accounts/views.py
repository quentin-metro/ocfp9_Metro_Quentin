from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    return render(request, 'accounts/accueil.html')
