from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from scraper.models import UserProfileHtml, UserCookie
from scraper.Infrastructure import Linkedin
from scraper.models import UserCookie

from scraper.check_if_cookie import check_if_cookie


@login_required(login_url='/auth/signin')
def loading_bridge(request):
    to = request.GET.get('to')
    message = 'Loading, please wait...'

    if 'update_linkedin_access' in to:
        message = 'Verifying connection with LinkedIn...'

    if 'new_cv' in to:
        message = 'Ensuring connection and fetching data from LinkedIn. This process may take a moment...'

    return render(request, 'props/loading_fullscreen.html', {'to': to, 'message': message})


@login_required(login_url='/auth/signin')
def new_extraction(request):
    cookie = check_if_cookie(request.user)
    if cookie == None:
        return redirect('/')
    
    user = UserProfileHtml.objects.get(user=request.user)
    data = user.data
    return render(request, 'generate_cv/home.html', {'data': data})


@login_required(login_url='/auth/signin')
def md_linkedin(request):
    li_at = request.GET.get('li_at')
    validate = Linkedin.get_profile_data(
        li_at,
        request.user,
        True,
        True
    )

    if type(validate) == bool:
        if validate:
            try:
                user_cookie = UserCookie.objects.get(user=request.user)
                user_cookie.cookie = li_at
                user_cookie.save()
            except UserCookie.DoesNotExist:
                user_cookie = UserCookie(
                    user=request.user,
                    cookie=li_at
                )
                user_cookie.save()

    return redirect('/')


@login_required(login_url='/auth/signin')
def index(request):
    cv_exists = False
    cookie_exists = True
    try:
        UserCookie.objects.get(user=request.user)
    except UserCookie.DoesNotExist:
        cookie_exists = False
    return render(request, 'home/home.html', {'cv_exists': cv_exists, 'cookie_exists': cookie_exists})