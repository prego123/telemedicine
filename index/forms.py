from django.contrib.auth.models import User
from django import forms
from .models import Patient, Doctor, Appointmentdoc

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username', 'email', 'password']
    
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'address', 'profile_pic']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'address', 'degree', 'profile_pic']
