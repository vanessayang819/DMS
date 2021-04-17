from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
sex_CHOICES = ((1, "男"), (2, "女"), (0, '未知的性别'),
               (5, '女性改（变）为男性'), (6, '男性改（变）为女性'),
               (9, '未说明的性别')
               )
IDType_CHOICES = ((1, '居民身份证'), (2, '居民户口簿'),
                  (3, '护照'), (4, '军官证'),
                  (5, '驾驶证'), (6, '港澳居民来往内地通行证'),
                  (7, '台湾居民来往内地通行证'), (99, '其他法定有效证件'),)

department_CHOICES = ((3108, '妇科'), (3110, '儿科'),
                      (3128, '综合一科'), (3148, '口腔科'),
                      (3103, '内科'), (3141, '产科'),
                      (3113, '五官科'), (3119, '中医科'),
                      (3123, '皮肤科'), (3154, '外科'),
                      (3114, '疼痛科'), (3161, '骨科'),
                      )


class Patient(models.Model):
    IDType = models.IntegerField(choices=IDType_CHOICES, default=1)
    IDNumber = models.CharField(default=000000, max_length=20)
    name = models.CharField(default=1, max_length=23)
    sex = models.IntegerField(choices=sex_CHOICES, default=1)
    phone_number = models.CharField(default=1, max_length=13)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"患者"
        verbose_name_plural = u"患者"


class Doctor(models.Model):
    user = models.OneToOneField(User, default=000000, on_delete=models.CASCADE)
    departmentID = models.IntegerField(choices=department_CHOICES, default=0000)
    name = models.CharField(default=1, max_length=23)
    sex = models.IntegerField(choices=sex_CHOICES, default=1)
    dob = models.DateField(default=1900-1-1, null=True)
    phone_number = models.CharField(default=1, max_length=13)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"医生"
        verbose_name_plural = u"医生"
