from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accommodations.forms import (
    UserLogin,
    ApplicationForm, DormForm, StudentForm)
from accommodations.models import Dorm, Student, Application
from django.db import models


# @login_required
#def attach_files(request, name):
#    if request.method == 'GET':
#        form = models.FileField(upload_to='uploads')
#    elif request.method == 'POST':
#        form = models.FileField(upload_to='uploads')
#        if form.is_valid():
#            cleaned_data = form.cleaned_data
#            comment = UserPostComment(text=cleaned_data['text'],
#                                      post=post,
#                                      author=request.user)
#            comment.save()
#
#    comments = UserPostComment.objects.filter(post=post)
#
#    context = {
#        'post': post,
#        'comments': comments,
#        'form': form,
#    }
#
#    return render(request, 'post_details.html', context)

@login_required
def create_dorm(request):
    if request.method == 'GET':
        camin_form = DormForm()
    elif request.method == 'POST':
        camin_form = DormForm(request.POST)
        if camin_form.is_valid():
            camin_form.save()
            return redirect('index')
    context = {
        'camin_form': camin_form,
    }
    return render(request, 'create_dorm.html', context)

@login_required
def create_student(request):
    if request.method == 'GET':
        student_form = StudentForm()
    elif request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()
            return redirect('index')
    context = {
        'student_form': student_form,
    }
    return render(request, 'create_student.html', context)

@login_required
def admin_panel(request):
    app = Application.objects.all()

    context = {
        'applications': app,
    }
    return render(request, 'admin_panel.html', context)


@login_required
def index(request):
    form = ApplicationForm()
    app = Application.objects.filter(pk=request.user.pk).first

    context = {
        'app': app,
        'app_form': form,
    }
    return render(request, 'index.html', context)


@login_required
def camine(request, nume):
    dorm = Dorm.objects.get(name=nume)
    form = DormForm()
    context = {
        'form': form,
        'dorm': dorm,
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