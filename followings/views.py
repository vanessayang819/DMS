from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import Following
from datetime import datetime
from django.utils import timezone
from home.context_processors import hasGroup
from profiles.models import Patient, Doctor
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import timedelta
from appointments.forms import TypeForm
# Create your views here.


#CREATE
@login_required
def book(request):
    user = request.user
    if hasGroup(user, 'doctor'):
        c = {}
        c.update(csrf(request))
        c['patients'] = Patient.objects.all()
        c['doctors'] = Doctor.objects.filter(user_id=user.id)
        c['forms'] = TypeForm(request.POST)

        return render(request, 'followings/book_followings.html', c)
    messages.add_message(request, messages.WARNING, '失败')
    return HttpResponseRedirect('/home')

@login_required
def doBook(request):
    user = request.user
    if  hasGroup(user, 'doctor'):
        patient = Patient.objects.get(name=request.POST.get('patient', ''))
        doctor = Doctor.objects.get(name=request.POST.get('doctor', ''))
        following_type = request.POST.get('following_type')
        following_time = request.POST.get('following_date')+'T'+request.POST.get('following_time')
        following_time = datetime(*[int(v) for v in following_time.replace('T', '-').replace(':', '-').split('-')])
        description = request.POST.get('description', '')
        following = Following(patient=patient, doctor=doctor,following_type=following_type,
                                  following_time=following_time,description=description)
        following.save()
        messages.add_message(request, messages.INFO, '成功添加随访')
    else:
        messages.add_message(request, messages.WARNING, '添加随访失败')
    return HttpResponseRedirect('/followings/')


#RETRIEVE
@login_required
def view(request):
    user = request.user
    if hasGroup(user, 'doctor'):
        following_list= [i for i in Following.objects.all() if i.doctor.user.id == user.id]
        current_page = request.GET.get('p')
        paginator = Paginator(following_list, 5)
        try:
            page_obj = paginator.page(current_page)
        except EmptyPage as e:
            page_obj = paginator.page(1)
        except PageNotAnInteger as e:
            page_obj = paginator.page(1)
    else:
        messages.add_message(request, messages.WARNING, '访问失败')
        return HttpResponseRedirect('/home')
    return render(request, 'followings/view_followings.html', {'page_obj': page_obj})


#UPDATE
@login_required
def changeFollowing(request, id):
    user = request.user
    if hasGroup(user, 'doctor'):
        c = {'following': Following.objects.get(pk=id)}
        c['doctors'] = Doctor.objects.all()
        c['forms'] = TypeForm(request.POST)
        c.update(csrf(request))
        return render(request, 'followings/change.html', c)
    messages.add_message(request, messages.WARNING, '修改失败')
    return HttpResponseRedirect('/home')


@login_required
def doChange(request):
    user = request.user
    if hasGroup(user, 'doctor'):
        following = Following.objects.get(pk=int(request.POST.get('id')))
        following_time = request.POST.get('following_date')+'T'+request.POST.get('following_time')
        following_time = datetime(*[int(v) for v in following_time.replace('T', '-').replace(':', '-').split('-')])
        description = request.POST.get('description')
        following_type = request.POST.get('following_type')
        following.following_time = following_time
        following.description = description
        following.following_type = following_type
        following.save()
    messages.add_message(request, messages.INFO, '修改随访成功')
    return HttpResponseRedirect('/followings/')



#DELETE
def delete(request, id):
    user = request.user
    if hasGroup(user, 'doctor'):
        Following.objects.get(id=id).delete()
        messages.add_message(request, messages.INFO, '成功删除随访')
    else:
        messages.add_message(request, messages.WARNING, '删除随访失败')
    return HttpResponseRedirect('/followings/')


