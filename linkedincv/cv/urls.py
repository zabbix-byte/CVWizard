from django.urls import path
from cv.views import *

urlpatterns = [
    path('export', export)
]
