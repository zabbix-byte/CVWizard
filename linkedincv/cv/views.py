import json

from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cv.models import ExportedCv
# Create your views here.


@login_required(login_url='/auth/signin')
def export(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        basic_information = data.get('basic_information')
        education = data.get('education')
        experiences = data.get('experiences')
        licenses = data.get('licenses')
        projects = data.get('projects')
        hide_basic_information_items = data.get('hide_basic_information_items')
        name = data['name'].strip()

        if len(name) == 0:
            return JsonResponse({'error': 'Enter a name for your export'})

        if len(name) > 79:
            return JsonResponse({'error': 'The maximum length for the name is 80 characters'})

        try:
            ExportedCv.objects.get(name=name, user=request.user)
            return JsonResponse({'error': 'Already have this name configured for export'})

        except ExportedCv.DoesNotExist:
            export = ExportedCv(
                name=name,
                user=request.user,
                basic_information=basic_information,
                education=education,
                experiences=experiences,
                licenses=licenses,
                projects=projects,
                hide_basic_information_items=hide_basic_information_items
            )

            export.save()

            return JsonResponse({'uuid': export.id})

    return JsonResponse({'okk': True})
