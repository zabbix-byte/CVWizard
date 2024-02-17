
from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('cv', home),
    path('', index),
]
