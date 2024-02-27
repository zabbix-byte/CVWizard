import json

from django.shortcuts import redirect
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
    return JsonResponse({'error': True})
