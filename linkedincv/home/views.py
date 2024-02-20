import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from scraper.models import UserProfileHtml, UserCookie
from scraper.Infrastructure import Linkedin
from scraper.models import UserCookie
from django.http import JsonResponse


@login_required(login_url='/auth/signin')
def loading_bridge(request):
    to = request.GET.get('to')
    message = 'Loading, please wait...'

    if 'update_linkedin_access' in to:
        message = 'Verifying connection with LinkedIn...'
    
    if 'new_cv' in to:
        message = 'Verifying connection and retrieving data from LinkedIn...'

    return render(request, 'props/loading_fullscreen.html', {'to': to, 'message': message})


@login_required(login_url='/auth/signin')
def new_extraction(request):
    cookie = UserCookie.objects.get(user=request.user)
    validate = Linkedin.get_profile_data(cookie.default_username, cookie.cookie, request.user, False)

    if type(validate) == tuple:
        if not validate[0]:
            UserCookie.objects.filter(user=request.user).delete()
            return redirect('/')

    user = UserProfileHtml.objects.get(user=request.user, target=cookie.default_username)
    data = user.data
    return render(request, 'generate_cv/home.html', {'data': data})


@login_required(login_url='/auth/signin')
def md_linkedin(request):
    li_at = request.GET.get('li_at')
    validate = Linkedin.get_profile_data(
        None,
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
                    cookie=li_at,
                    default_username='default'
                )
                user_cookie.save()

            return redirect('/')
    else:
        return redirect('https://www.linkedin.com/login')


@login_required(login_url='/auth/signin')
def index(request):
    cv_exists = False
    cookie_exists = True
    try:
        UserCookie.objects.get(user=request.user)
    except UserCookie.DoesNotExist:
        cookie_exists = False
    return render(request, 'home/home.html', {'cv_exists': cv_exists, 'cookie_exists': cookie_exists})


@login_required(login_url='/auth/signin')
def setup_linkedin_access(request):
    if request.body:
        body = json.loads(request.body)
        username = body['username']
        li_token = body['li_token']

        validate = Linkedin.get_profile_data(username, li_token, request.user, True)

        if type(validate) == bool:
            if validate:
                try:
                    user_cookie = UserCookie.objects.get(user=request.user)
                    user_cookie.cookie = li_token
                    user_cookie.default_username = username
                    user_cookie.save()
                except UserCookie.DoesNotExist:
                    user_cookie = UserCookie(
                        user=request.user,
                        cookie=li_token,
                        default_username=username
                    )
                    user_cookie.save()

                return JsonResponse({'ok': True})
        elif type(validate) == tuple:
            if not validate[0]:
                return JsonResponse({'error': validate[1]})

    return JsonResponse({'error': 'Only POST'})
