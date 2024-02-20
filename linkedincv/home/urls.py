
from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('new_cv', new_extraction),
    path('', index),
    path('update_linkedin_access', md_linkedin),
    path('loading_bridge', loading_bridge)
]
