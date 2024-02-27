from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from scraper.models import UserProfileHtml, UserCookie
from scraper.Infrastructure import Linkedin
from scraper.models import UserCookie

from scraper.check_if_cookie import check_if_cookie
from cv.models import ExportedCv


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
    existing_data = request.GET.get('existing_data')

    if existing_data == 'false':
        cookie = check_if_cookie(request.user)
        if cookie == None:
            return redirect('/')

    try:
        user = UserProfileHtml.objects.get(user=request.user)
    except UserProfileHtml.DoesNotExist:
        return redirect('/')

    data = user.data
    return render(request, 'generate_cv/home.html', {'data': data, 'export_date': datetime.now()})


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
    exists_profile = False
    last_modified = None
    try:
        UserCookie.objects.get(user=request.user)
    except UserCookie.DoesNotExist:
        cookie_exists = False

    profile_data = list(UserProfileHtml.objects.filter(user=request.user).values())

    if len(profile_data) == 1:
        last_modified = profile_data[0]['last_modified']
        exists_profile = True

    exported_cv = [{'name': i['name'], 'uuid': i['id'].hex}
                   for i in ExportedCv.objects.filter(user=request.user).values('id', 'name')]
    exported_cv_not_exists = True if len(exported_cv) == 0 else False

    return render(request, 'home/home.html', {'cv_exists': cv_exists,
                                              'cookie_exists': cookie_exists,
                                              'exists_profile': exists_profile,
                                              'last_modified': last_modified,
                                              'exported_cv': exported_cv,
                                              'exported_cv_not_exists': exported_cv_not_exists
                                              })
