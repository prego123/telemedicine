from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.db import models


class Patient(models.Model):
    user = models.ForeignKey(User, default=1)
    first_name = models.CharField(max_length=250)
    last_name= models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.first_name + ' - ' + self.last_name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_username = models.CharField(max_length=250)
    date = models.CharField(max_length=250)

    def __str__(self):
        return self.doctor_username

class Doctor(models.Model):
    user = models.ForeignKey(User, default=1)
    first_name = models.CharField(max_length=250)
    last_name= models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    degree= models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    
    def __str__(self):
        return self.first_name + ' - ' + self.last_name

class Appointmentdoc(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_username = models.CharField(max_length=250)
    date = models.CharField(max_length=250)

    def __str__(self):
        return self.patient_username