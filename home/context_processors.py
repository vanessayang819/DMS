from django.contrib.auth.models import Group

def hasGroup(user, groupName):
    try:
        group = Group.objects.get(name=groupName)
        return True if group in user.groups.all() else False
    except:
        return False


def menu_processor(request):
    menu = {'患者管理': '/profile/patient_view', '预约管理': '/appointments', '我的日程': '/appointments/my_schedule',
            '诊断管理': '/diagnosis', '随访管理': '/followings', '报表管理': '/reports'}
    return {'menu': menu}
