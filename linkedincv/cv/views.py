import json

from django.shortcuts import redirect, render
from django.http import JsonResponse
# Create your views here.


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
            return JsonResponse({'error': 'The maximum length for the name is 255 characters'})

    return JsonResponse({'okk': True})
