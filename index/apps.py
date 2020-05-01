from django.apps import AppConfig
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import forms

class IndexConfig(AppConfig):
    name = 'index'

