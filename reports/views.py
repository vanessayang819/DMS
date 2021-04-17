from django.shortcuts import render
from profiles.models import Patient, Doctor
from appointments.models import Appointment
from diagnosis.models import Diagnosis
from datetime import datetime
from django.db.models import Func,ExpressionWrapper, F, Q, fields, Avg, Count


def countPatient(request):
    user = request.user
    counts = {}
    d = Doctor.objects.get(user_id=user.id)
    my_appt1 = d.appointment_doctor.filter(appt_access=1)
    my_appt2 = d.appointment_doctor.filter(appt_access=2)
    counts['male1'] = my_appt1.filter(patient__sex=1).count()
    counts['male2'] = my_appt2.filter(patient__sex=1).count()
    counts['female1'] = my_appt1.filter(patient__sex=2).count()
    counts['female2'] = my_appt2.filter(patient__sex=2).count()
    counts['appt1'] = my_appt1.count()
    counts['appt2'] = my_appt2.count()
    # counts['1below25'] = my_appt1.filter(patient__age__lt=35).count()
    # counts['2below25'] = my_appt2.filter(patient__sex=2).count()


    # mypid = []
    # for i in d.appointment_doctor.all():
    #     mypid.append(i.patient.id)
    # mypatientid = list(set(mypid))
    # my_patient = Patient.objects.filter(pk__in=mypatientid)



    my_diag = Diagnosis.objects.filter(appointment__doctor__user_id=user.id).values()
    counts["type1"] = my_diag.filter(d_type=1).count()
    counts["type2"] = my_diag.filter(d_type=2).count()
    counts["type3"] = my_diag.filter(d_type=3).count()

    my_diag = my_diag.annotate(duration=ExpressionWrapper(F('filed_time') - F('appointment__appointment_time'),
                                                        output_field=fields.DurationField()))

    my_diag1 = my_diag.filter(Q(d_type=1)& Q(appointment__appt_access=1))
    my_diag2 = my_diag.filter(Q(d_type=2)& Q(appointment__appt_access=1))
    my_diag3 = my_diag.filter(Q(d_type=3)& Q(appointment__appt_access=1))
    my_diag4 = my_diag.filter(Q(d_type=1)& Q(appointment__appt_access=2))
    my_diag5 = my_diag.filter(Q(d_type=2)& Q(appointment__appt_access=2))
    my_diag6 = my_diag.filter(Q(d_type=3)& Q(appointment__appt_access=2))

    if my_diag1:
        counts['w1'] = int(my_diag1.aggregate(Avg('duration'))['duration__avg'].total_seconds())/60
    else:
        counts['w1'] = 0
    if my_diag2:
        counts['w2'] = int(my_diag2.aggregate(Avg('duration'))['duration__avg'].total_seconds())/60
    else:
        counts['w2'] =0
    if my_diag3:
        counts['w3'] = int(my_diag3.aggregate(Avg('duration'))['duration__avg'].total_seconds())/60
    else:
        counts['w3'] =0
    if my_diag4:
        counts['w4'] = int(my_diag4.aggregate(Avg('duration'))['duration__avg'].total_seconds())/60
    else:
        counts['w4'] =0
    if my_diag5:
        counts['w5'] = int(my_diag5.aggregate(Avg('duration'))['duration__avg'].total_seconds())/60
    else:
        counts['w5'] =0
    if my_diag6:
        counts['w6'] = int(my_diag6.aggregate(Avg('duration'))['duration__avg'].total_seconds())/60
    else:
        counts['w6'] =0

    counts['s1'] = counts['w1']+counts['w4']
    counts['s2'] = counts['w2']+counts['w5']
    counts['s3'] = counts['w3']+counts['w6']

    if     counts['type1']==0:
        counts['a1']=0
    else:
        counts['a1'] = counts['s1'] /counts['type1']

    if counts['type2'] == 0:
        counts['a2'] = 0
    else:
        counts['a2'] = counts['s2'] /counts['type2']

    if     counts['type3']==0:
        counts['a3']=0
    else:
        counts['a3'] = counts['s3'] /counts['type3']

    return render(request, 'reports/data_analysis.html', counts)

