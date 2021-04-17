from django import forms
from .models import appt_access_CHOICES
from diagnosis.models import diag_type_CHOICES
from followings.models import following_type_CHOICES
from appointments.models import is_pass_CHOICE
from django.forms import fields,widgets


class TypeForm(forms.Form):
    following_type = forms.IntegerField(
        widget=forms.Select(choices=following_type_CHOICES))
    d_type = forms.IntegerField(
        widget=forms.Select(choices=diag_type_CHOICES))
    appt_access = forms.IntegerField(
        widget=forms.Select(choices=appt_access_CHOICES))
    is_pass = forms.IntegerField(
        widget=forms.Select(choices=is_pass_CHOICE))




