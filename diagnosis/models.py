from django.db import models
from django.contrib.auth.models import User
from appointments.models import Appointment

# Create your models here.
diag_type_CHOICES = ((1, '优先门诊法'),
                     (2, '先到先看病'),
                     (3, '间隔一定数量'),
                      (4, '无'),
                     )


class Diagnosis(models.Model):
    appointment = models.OneToOneField(Appointment, default=None, on_delete=models.CASCADE,
                                       related_name='diagnosis_appointment')
    # patient = models.ForeignKey(Patient, default=None,on_delete=models.CASCADE, related_name='case_patient')
    description = models.CharField(max_length=500, default=None)
    filed_time = models.DateTimeField(default=None, null=True)
    closed_time = models.DateTimeField(default=None, null=True)
    d_type = models.IntegerField(
        choices=diag_type_CHOICES,
        default=1,
    )

    def __str__(self):
        return self.description
