from django import forms
from django.contrib import admin
from .models import Patient, Appointment, Doctor, Appointmentdoc
from . import models

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Appointmentdoc)
# Register your models here.