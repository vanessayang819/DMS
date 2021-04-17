from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import Diagnosis
from datetime import datetime
from home.context_processors import hasGroup
from appointments.models import Appointment
from django.contrib import messages
from profiles.models import Patient, Doctor
from appointments.forms import TypeForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
# CREATE
@login_required
def generate(request, appointment_id):
    if hasGroup(request.user, 'doctor'):
        c = {}
        c['appointment'] = Appointment.objects.get(pk=appointment_id)
        c['forms'] = TypeForm(request.POST)
        c.update(csrf(request))
        return render(request, 'diagnosis/generate.html', c)
    messages.add_message(request, messages.WARNING, '失败')
    return HttpResponseRedirect('/home')

@login_required
def doGenerate(request):
    if hasGroup(request.user, 'doctor'):
        appointment = Appointment.objects.get(pk=request.POST.get('appointment_id', ''))
        description = request.POST.get('description', '')
        filed_time = request.POST.get('filed_date') + 'T' + request.POST.get('filed_time')
        filed_time = datetime(*[int(v) for v in filed_time.replace('T', '-').replace(':', '-').split('-')])
        #closed_date = datetime.now()
        closed_time = request.POST.get('closed_date') + 'T' + request.POST.get('closed_time')
        closed_time = datetime(*[int(v) for v in closed_time.replace('T', '-').replace(':', '-').split('-')])

        d_type = request.POST.get('d_type','')
        c = Diagnosis(appointment=appointment, description=description,
                      filed_time=filed_time ,closed_time=closed_time,
                      d_type=d_type)
        c.save()

        messages.add_message(request, messages.INFO, '成功创建')
        return HttpResponseRedirect('/diagnosis/')
    messages.add_message(request, messages.WARNING, '失败')
    return HttpResponseRedirect('/home')


# RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'doctor'):
        appt_list = [i for i in Appointment.objects.all() if i.doctor.user.id == user.id]
        c['diagnosis'] = []
        for appointment in appt_list:
            c['diagnosis'].extend(list(Diagnosis.objects.filter(appointment=appointment)))

        current_page = request.GET.get('p')
        paginator = Paginator(c['diagnosis'], 5)
        try:
            page_obj = paginator.page(current_page)
        except EmptyPage as e:
            page_obj = paginator.page(1)
        except PageNotAnInteger as e:
            page_obj = paginator.page(1)
    else:
        messages.add_message(request, messages.WARNING, '失败')
        return HttpResponseRedirect('/home')
    return render(request, 'diagnosis/view.html', {'page_obj': page_obj})


#UPDATE
@login_required
def changeDiagnosis(request, id):
    user = request.user
    if hasGroup(user, 'doctor'):
        c = {'diagnosis': Diagnosis.objects.get(pk=id)}
        c['doctors'] = Doctor.objects.all()
        c['forms'] = TypeForm(request.POST)
        c.update(csrf(request))
        return render(request, 'diagnosis/update.html', c)
    messages.add_message(request, messages.WARNING, '失败')
    return HttpResponseRedirect('/home')


@login_required
def doChange(request):
    user = request.user
    if hasGroup(user, 'doctor'):
        diagnosis = Diagnosis.objects.get(pk=int(request.POST.get('id')))
        description = request.POST.get('description')
        d_type = request.POST.get('d_type','')
        diagnosis.description = description
        diagnosis.d_type = d_type
        diagnosis.save()
    messages.add_message(request, messages.INFO, '修改成功')
    return HttpResponseRedirect('/diagnosis/')
