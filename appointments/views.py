from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from .models import Appointment
from datetime import datetime
from django.utils import timezone
from home.context_processors import hasGroup
from profiles.models import Patient, Doctor
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import timedelta
from .forms import TypeForm
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
        c['appointments'] = Appointment.objects.all()
        c['forms'] = TypeForm(request.POST)
        return render(request, 'appointments/book_appointment.html', c)
    return HttpResponseRedirect('/home')

@login_required
def doBook(request):
    user = request.user
    if hasGroup(user, 'doctor'):
        patient = Patient.objects.get(name=request.POST.get('patient', ''))
        doctor = Doctor.objects.get(name=request.POST.get('doctor', ''))
        appt_access = request.POST.get('appt_access')
        appointment_time = request.POST.get('appointment_date')+'T'+request.POST.get('appointment_time')
        appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        appointment = Appointment(patient=patient, doctor=doctor,
                                  appointment_time=appointment_time, appt_access=appt_access)
        appointment.save()
        messages.add_message(request, messages.INFO, '成功')
    else:
        messages.add_message(request, messages.WARNING, '失败')
    return HttpResponseRedirect('/appointments/')


#
@login_required
def view(request):
    user = request.user
    if hasGroup(user, 'doctor'):
        appt_list= [i for i in Appointment.objects.all() if i.doctor.user.id == user.id]
        current_page = request.GET.get('p')
        paginator = Paginator(appt_list, 7)
        try:
            page_obj = paginator.page(current_page)
        except EmptyPage as e:
            page_obj = paginator.page(1)
        except PageNotAnInteger as e:
            page_obj = paginator.page(1)
    else:
        messages.add_message(request, messages.WARNING, '访问失败')
        return HttpResponseRedirect('/home')
    return render(request, 'appointments/view_all.html', {'page_obj': page_obj})



@login_required
def myview(request):
    user = request.user
    start = timezone.now() - timedelta(hours=12, minutes=0, seconds=0)
    endtime = timezone.now() + timedelta(hours=8, minutes=0, seconds=0)
    sortType = request.GET.get('sort','')
    appt = Appointment.objects.filter(doctor__user__id =user.id)

    if sortType == '1':
        appt = appt.filter(appointment_time__range=(start,endtime)).order_by('appt_access')
    elif sortType == '2':
        appt = appt.filter(appointment_time__range=(start, endtime)).order_by('appointment_time')

    elif sortType == '3':
        appt1 = list(appt.filter(appointment_time__range=(start, endtime)).filter(appt_access=1))
        appt2 = list(appt.filter(appointment_time__range=(start, endtime)).filter(appt_access=2))

        n = len(appt1) + len(appt2)
        appt=[]
        i = 0
        j = 0
        k = 0
        while i < n:
            while j < len(appt1):
                appt.append(appt1[j])
                j = j + 1
                i = i + 1
                break
            while j < len(appt1):
                appt.append(appt1[j])
                j = j + 1
                i = i + 1
                break
            while k < len(appt2):
                appt.append(appt2[k])
                k = k + 1
                i = i + 1
                break
    else:
        appt = appt.filter(appointment_time__range=(start, endtime))

    c = {}
    c['appt'] = appt

    return render(request, 'appointments/my_schedule.html', c)

