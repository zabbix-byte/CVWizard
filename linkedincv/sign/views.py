import re

from django.shortcuts import render, redirect
from scraper.Infrastructure import Linkedin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from scraper.check_if_cookie import check_if_cookie


def get_perfil_data(request):
    if request.POST:
        username = request.POST['username']
        cookie = request.POST['cookie']
        authorized = Linkedin.get_profile_data(username, cookie)

        if type(authorized) == tuple:
            if not authorized[0]:
                return render(request, 'auth/login.html', {'Authorized': False, 'info': authorized[1]})

        return redirect(f'/home?cookie={cookie}&username={username}')

    return render(request, 'auth/login.html', {'Authorized': None})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            check_if_cookie(user, True, True)
            return redirect('/')
        else:
            return render(request, 'auth/login.html', {'Authorized': False, 'info': 'Mystical access denied'})

    return render(request, 'auth/login.html', {'Authorized': None})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_check = request.POST.get('password_check')

        email_r = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if len(password) < 8:
            return render(request, 'auth/register.html', {'Authorized': False, 'info': 'Password length minimum 8 characters.'})

        if (re.fullmatch(email_r, username)):
            return render(request, 'auth/register.html', {'Authorized': False, 'info': 'Username can\'t be an email.'})

        if password != password_check:
            return render(request, 'auth/register.html', {'Authorized': False, 'info': 'Passwords don\'t match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'Authorized': False, 'info': 'Username ensnared by digital wards.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {'Authorized': False, 'info': 'Email ensnared by digital wards.'})

        user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            check_if_cookie(user, True, True)
            return redirect('/')

    return render(request, 'auth/register.html', {'Authorized': None})


@login_required(login_url='/auth/signup/')
def logoutv(request):
    logout(request)
    return redirect('/auth/signin/')
