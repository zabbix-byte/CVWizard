from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from scraper.models import UserProfileHtml, UserCookie


@login_required(login_url='/auth/signin')
def home(request):
    try:
        # user = UserProfileHtml.objects.get(cookie=cookie, user=username)
        # data = user.data
        ...
    except UserProfileHtml.DoesNotExist:
        return redirect('/auth/login')

    return render(request, 'generate_cv/home.html', {'data': ''})


@login_required(login_url='/auth/signin')
def index(request):
    cv_exists = False

    try:
        UserCookie.objects.get(user=request.user)
        cookie_exists = True
    except UserCookie.DoesNotExist:
        cookie_exists = False

    return render(request, 'home/home.html', {'cv_exists': cv_exists, 'cookie_exists': cookie_exists})
