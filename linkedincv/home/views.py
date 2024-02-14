from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from scraper.models import UserProfileHtml


def home(request):
    cookie = request.GET.get('cookie')
    username = request.GET.get('username')

    if not username and not cookie:
        return redirect('/auth/login')

    try:
        user = UserProfileHtml.objects.get(cookie=cookie, user=username)
    except UserProfileHtml.DoesNotExist:
        return redirect('/auth/login')

    return render(request, 'home/home.html', {'data': user.data})


def index(request):
    return redirect('/home')
