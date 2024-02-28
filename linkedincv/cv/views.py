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

        editor = True if data.get('editor') and data.get('editor').lower() == 'true' else False
        uuid = data.get('uuid')

        if len(name) == 0:
            return JsonResponse({'error': 'Enter a name for your export'})

        if len(name) > 79:
            return JsonResponse({'error': 'The maximum length for the name is 80 characters'})

        if not editor:
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

            return JsonResponse({'uuid': export.id.hex})

        data_to_edit = ExportedCv.objects.get(user=request.user, id=uuid)
        data_to_edit.name = name
        data_to_edit.basic_information = basic_information
        data_to_edit.education = education
        data_to_edit.experiences = experiences
        data_to_edit.licenses = licenses
        data_to_edit.projects = projects
        data_to_edit.hide_basic_information_items = hide_basic_information_items
        data_to_edit.save()
        return JsonResponse({'uuid': data_to_edit.id.hex})

    return JsonResponse({'okk': True})
