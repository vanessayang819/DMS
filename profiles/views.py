from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from home.context_processors import hasGroup
from django.contrib import messages
from profiles.models import Patient, Doctor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def myProfile(request):
    if hasGroup(request.user, 'doctor'):
      return render(request, 'profiles/my_profile.html')


# UPDATE
@login_required
def changeProfile(request, id):
    user = request.user
    if hasGroup(user, 'doctor'):
        c = {'doctor': Doctor.objects.get(pk=id)}
        c['doctors'] = Doctor.objects.all()
        c.update(csrf(request))
        return render(request, 'profiles/change_profile.html', c)
    return HttpResponseRedirect('/home')


@login_required
def doChange(request):
    user = request.user
    if hasGroup(user, 'doctor'):
        doctor = Doctor.objects.get(pk=int(request.POST.get('id')))
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        doctor.phone_number = phone_number
        doctor.address = address
        doctor.save()
    messages.add_message(request, messages.INFO, '修改成功')
    return HttpResponseRedirect('/profile/')


@login_required
def viewPatient(request):
    user = request.user
    if hasGroup(request.user, 'doctor'):
        c = {}
        c.update(csrf(request))
        d = Doctor.objects.get(user_id=user.id)
        c = {'myappt': d.appointment_doctor.all()}
        mypid = []
        for i in d.appointment_doctor.all():
            mypid.append(i.patient.id)
        mypatientid = list(set(mypid))
        mypatient = Patient.objects.filter(pk__in=mypatientid).order_by('id')
        current_page = request.GET.get('p')
        paginator = Paginator(mypatient, 8)
        try:
            page_obj = paginator.page(current_page)
        except EmptyPage as e:
            page_obj = paginator.page(1)
        except PageNotAnInteger as e:
            page_obj = paginator.page(1)
        c['page_obj'] = page_obj
        return render(request, 'profiles/patient_view.html', c)
    else:
        return HttpResponseRedirect('/home')
