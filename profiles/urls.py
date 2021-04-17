from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', myProfile),
    path('patient_view/', viewPatient),
    url(r'change_profile/(?P<id>\d+)/', changeProfile),
    path('do_change/', doChange),

]
