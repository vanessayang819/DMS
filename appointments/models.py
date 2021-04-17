from django.db import models
from django.contrib.auth.models import User
from profiles.models import Patient, Doctor


# Create your models here.

appt_access_CHOICES = ((2, '线上'), (1, '线下'),)
is_pass_CHOICE = ((0,'未诊断'),(1,'已诊断'),(2,'过号'))
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,related_name='appointment_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment_doctor')
    appointment_time = models.DateTimeField()
    is_pass = models.IntegerField(
        choices = is_pass_CHOICE,
        default=0,
    )
    appt_access = models.IntegerField(choices=appt_access_CHOICES,default=1)

    def __str__(self):
        return self.patient.name + ' 与 ' + self.doctor.name


    class Meta:
        verbose_name = u"预约"
        verbose_name_plural = u"预约"
