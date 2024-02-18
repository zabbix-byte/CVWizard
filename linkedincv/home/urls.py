
from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('cv', new_extraction),
    path('', index),
    path('setup_linkedin_access', setup_linkedin_access),
]
