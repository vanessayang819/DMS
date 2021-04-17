from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib import messages


# Create your views here.
def chooserole(request):
	return render(request, 'loginmodule/choose_role.html')

def login(request):
	if request.user.is_authenticated:
		messages.add_message(request, messages.INFO, '登录成功')
		return HttpResponseRedirect('/home')
	else:
		c = {}
		c.update(csrf(request))
		return render(request, 'loginmodule/login.html', c)


def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		# messages.add_message(request, messages.INFO, '已经登录')
		return HttpResponseRedirect('/home')
	else:
		messages.add_message(request, messages.WARNING, '用户名不存在或密码错误')
		return HttpResponseRedirect('/login')


def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	messages.add_message(request, messages.INFO, '成功登出')
	return HttpResponseRedirect('/chooserole')
