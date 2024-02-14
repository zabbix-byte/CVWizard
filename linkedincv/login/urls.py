
from django.contrib import admin
from django.urls import path
from login.views import *

urlpatterns = [
    path('', login)    
]
