# Generated by Django 2.2.7 on 2021-02-02 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDType', models.IntegerField(choices=[(1, '居民身份证'), (2, '居民户口簿'), (3, '护照'), (4, '军官证'), (5, '驾驶证'), (6, '港澳居民来往内地通行证'), (7, '台湾居民来往内地通行证'), (99, '其他法定有效证件')], default=1)),
                ('IDNumber', models.CharField(default=0, max_length=20)),
                ('name', models.CharField(default=1, max_length=23)),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女'), (0, '未知的性别'), (5, '女性改（变）为男性'), (6, '男性改（变）为女性'), (9, '未说明的性别')], default=1)),
                ('phone_number', models.CharField(default=1, max_length=13)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '患者',
                'verbose_name_plural': '患者',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentID', models.IntegerField(choices=[(3108, '妇科'), (3110, '儿科'), (3128, '综合一科'), (3148, '口腔科'), (3103, '内科'), (3141, '产科'), (3113, '五官科'), (3119, '中医科'), (3123, '皮肤科'), (3154, '外科'), (3114, '疼痛科'), (3161, '骨科')], default=0)),
                ('name', models.CharField(default=1, max_length=23)),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女'), (0, '未知的性别'), (5, '女性改（变）为男性'), (6, '男性改（变）为女性'), (9, '未说明的性别')], default=1)),
                ('dob', models.DateField(default=1898, null=True)),
                ('phone_number', models.CharField(default=1, max_length=13)),
                ('address', models.CharField(max_length=200)),
                ('user', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '医生',
                'verbose_name_plural': '医生',
            },
        ),
    ]
