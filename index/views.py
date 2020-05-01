from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import UserForm, PatientForm
from .models import Patient, Appointment
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from . import forms
from . import models
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

def doc_signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                email=request.POST['username'],
                password=request.POST['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You've been logged in.")
                    return HttpResponseRedirect(reverse('index:doc_profile'))
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Email or password is incorrect."
                )
    return render(request, 'index/doc_login.html', {'form': form})

def doc_signup(request):
    form = forms.DocCreateForm()
    if request.method == 'POST':
        form = forms.DocCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('index:doc_profile'))
    return render(request, 'index/doc_register.html', {'form': form})

def doclogout(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return render(request, 'index/index.html')

def profile_view(request):
    user = request.doctor
    patient = get_object_or_404(Patient, pk=2)
    if request.method == "POST":
        form = PatientForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            patient=form.save(commit=False)
            patient.user = user
          
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
    patient = get_object_or_404(Patient, pk=2)
    return render(request, 'index/profile_update.html', {'patient': patient, 'user': user})       

def status_pat(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=2)
    return render(request, 'index/patient.html', {'patient': patient,"user":user})

def appointment_pat(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=2)
    return render(request, 'index/pat_appoint.html', {'patient': patient,"user":user})

def history_pat(request):
    user = request.user
    patient = get_object_or_404(Patient, pk=2)
    return render(request, 'index/pat_history.html', {'patient': patient, "user":user})


def doc_profile(request):
    """Display user profile information."""
    user = request.user
    return render(request, 'accounts/doc_profile.html', {'user': user})

def edit_doc_profile(request):
    """Edit user profile information."""
    user = request.doctor
    form1 = forms.DocUpdateForm(instance=user)
    form2 = forms.DocProfileUpdateForm(instance=user.docprofile)
    if request.method == 'POST':
        form1 = forms.DocUpdateForm(instance=user, data=request.POST)
        form2 = forms.DocProfileUpdateForm(
            instance=user.docprofile,
            data=request.POST,
            files=request.FILES
        )
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, "Your profile has been updated!")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'index:doc_edit.html',
        {'form1': form1, 'form2': form2})

def change_password(request):
    """Change a user's password."""
    form = forms.ValidatingPasswordChangeForm(
        user=request.doctor,
        request=request
    )
    if request.method == 'POST':
        form = forms.ValidatingPasswordChangeForm(
            user=request.doctor,
            data=request.POST,
            request=request
        )
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been updated!")
            return HttpResponseRedirect(reverse('index:doc_profile'))
    return render(request, 'index/change_password.html', {'form': form})