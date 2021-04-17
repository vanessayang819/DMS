from django.db import models
from profiles.models import Patient, Doctor


# Create your models here.
following_type_CHOICES = ((1, '门诊随访'),
                     (2, '慢性病随访'),
                     (3, '出院随访'),
                     (4, '其他'),
                     )

class Following(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='following_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='following_doctor')
    description = models.CharField(max_length=500, default=None)
    following_time = models.DateTimeField()
    following_type = models.IntegerField(
        choices=following_type_CHOICES,
        default=1,
    )

    def __str__(self):
        return self.patient.name + ' 与 ' + self.doctor.name
