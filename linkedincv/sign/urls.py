
from django.contrib import admin
from django.urls import path
from sign.views import *

urlpatterns = [
    path('signin/', signin),
    path('signup/', signup),
    path('logout/', logoutv)
]
