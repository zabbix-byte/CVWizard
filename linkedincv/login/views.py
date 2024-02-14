from django.shortcuts import render, redirect
from scraper.Infrastructure import Linkedin
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def login(request):
    if request.POST:
        username = request.POST['username']
        cookie = request.POST['cookie']
        authorized = Linkedin.get_profile_data(username, cookie)

        if type(authorized) == tuple:
            if not authorized[0]:
                return render(request, 'auth/login.html', {'Authorized': False, 'info': authorized[1]})

        return redirect(f'/home?cookie={cookie}&username={username}')

    return render(request, 'auth/login.html', {'Authorized': None})
