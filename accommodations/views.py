from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accommodations.forms import (
    UserLogin,
    ApplicationForm, DormForm)
from accommodations.models import Dorm


@login_required
def admin_panel(request):
    dorms = Dorm.objects.all()
    if request.method == 'GET':
        camin_form = DormForm()
    elif request.method == 'POST':
        camin_form = DormForm(request.POST)
        if camin_form.is_valid():
            camin_form.save()
            return redirect('index')
    context = {
        'posts': dorms,
        'camin_form': camin_form,
    }
    return render(request, 'admin_panel.html', context)


@login_required
def index(request):
    form = ApplicationForm()
    context = {
        'app_form': form,
        'camin_form': DormForm
    }
    return render(request, 'index.html', context)


@login_required
def camine(request):
    dorms = Dorm.objects.all()
    form = DormForm()
    context = {
        'form': form,
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