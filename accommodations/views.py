from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accommodations.forms import (
    UserLogin,
    ApplicationForm, DormForm)
from accommodations.models import Dorm


@login_required
def index(request):
    form = ApplicationForm()
    context = {
        'app_form': form
    }
    return render(request, 'index.html', context)


@login_required
def camine(request):
    dorms = Dorm.objects.all()
    form = DormForm()
    context = {
        'dorm_form': form,
        'dorms': dorms,
    }
    return render(request, 'camine.html', context)


def login_view(request):
    if request.method == 'GET':
        login_form = UserLogin()
        context = {
            'form': login_form,
        }
        return render(request, 'login.html', context)
    if request.method == 'POST':
        login_form = UserLogin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': login_form,
                'message': 'Wrong user and/or password!',
            }
            return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))