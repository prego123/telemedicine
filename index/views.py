from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import UserForm, PatientForm, DoctorForm
from .models import Patient, Appointment, Doctor, Appointmentdoc
# Create your views here.

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def first(request):
    return render(request, 'index/index.html')

def usersign(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index/patient.html')
    context = {
        "form": form,
    }
    return render(request, 'index/user_register.html', context)

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index/patient.html')
            else:
                return render(request, 'index/user_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'index/user_login.html', {'error_message': 'Invalid login'})
    return render(request, 'index/user_login.html')

def userlogout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'index/index.html', context)

def profile_view(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=1)
    if request.method == "POST":
        form = PatientForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            patient=form.save(commit=False)
            patient.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                patient.profile_pic = request.FILES['profile_pic']
            patient.save()
            return render(request, 'index/profile_update.html', {'patient': patient})
        context = {
        "form": form,
        'patitent':patient
        }
        return render(request, 'index/profile_user.html', context)
    return render(request, 'index/profile_user.html', {"user":user, 'patient':patient})
    
def profile_update(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=1)
    return render(request, 'index/profile_update.html', {'patient': patient, 'user': user})       

def status_pat(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=1)
    return render(request, 'index/patient.html', {'patient': patient,"user":user})

def appointment_pat(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=1)
    return render(request, 'index/pat_appoint.html', {'patient': patient,"user":user})

def history_pat(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=1)
    return render(request, 'index/pat_history.html', {'patient': patient, "user":user})



def docsign(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index/doctor.html')
    context = {
        "form": form,
    }
    return render(request, 'index/doc_register.html', context)

def doclogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index/doctor.html')
            else:
                return render(request, 'index/doc_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'index/doc_login.html', {'error_message': 'Invalid login'})
    return render(request, 'index/doc_login.html')

def doclogout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'index/index.html', context)

def profile_view_doc(request):
    user = request.user
    doctor = get_object_or_404(Doctor, pk=1)
    return render(request, 'index/profile_doc.html', {"user":user, 'doctor':doctor})
    
def profile_update_doc(request):
    user = request.user
    doctor = get_object_or_404(Doctor, pk=1)
    if request.method == "POST":
        form = DoctorForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            doctor=form.save(commit=False)
            doctor.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                doctor.profile_pic = request.FILES['profile_pic']
            doctor.save()
            return render(request, 'index/profile_doc.html', {'doctor': doctor})
        context = {
        "form": form,
        'doctor':doctor
        }
        return render(request, 'index/doc_profile_update.html', context)
    return render(request, 'index/doc_profile_update.html', {'user': user, 'doctor':doctor})       

def status_doc(request):
    user = request.user
    doctor = get_object_or_404(Doctor, pk=1)
    return render(request, 'index/doctor.html', {"user":user, 'doctor':doctor})

def appointment_doc(request):
    user = request.user
    doctor = get_object_or_404(Doctor, pk=1)
    return render(request, 'index/doc_appoint.html', {"user":user, 'doctor':doctor})

def history_doc(request):
    user = request.user
    doctor = get_object_or_404(Doctor, pk=1)
    return render(request, 'index/doc_history.html', {"user":user, 'doctor':doctor})

