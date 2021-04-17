from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', view),
    url(r'generate/(?P<appointment_id>\d+)/', generate),
    path('do_generate/', doGenerate),

    url(r'change_diagnosis/(?P<id>\d+)/', changeDiagnosis),
    path('do_change/', doChange),
]
