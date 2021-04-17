# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")
# import os
#
# if __name__ == '__main__':
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")
#     import django
#
#     django.setup()
#
#     from test1.appointments.models import Appointment
#     from django.utils import timezone
#     from datetime import timedelta
#

from diagnosis.models import Diagnosis
from django.db.models import Func,ExpressionWrapper, F, fields,Avg


SomeModel.objects.annotate(
    duration = Func(F('end_date'), F('start_date'), function='age')
)

from datetime import timedelta


#duration = ExpressionWrapper(F('closed_at') - F('opened_at'), output_field=fields.DurationField())
dur=Diagnosis.objects.annotate(duration=ExpressionWrapper(F('closed_time') - F('filed_time'),output_field=fields.DurationField()))

dur.values('duration')
dur.aggregate(Avg('duration'))


Diagnosis.objects.values('duration')
my_diag = Diagnosis.objects.filter(appointment__doctor__user_id=2).values()
my_diag1 = my_diag.filter(d_type=1)

dur1=my_diag1.annotate(duration=ExpressionWrapper( F('filed_time')-F('appointment__appointment_time'),output_field=fields.DurationField()))

from profiles.models import Patient, Doctor
from datetime import date
def age(date_of_birth):
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
age=age(birth_of_date)







