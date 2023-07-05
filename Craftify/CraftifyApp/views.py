from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime

# Create your views here.


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def signin(request):
    return render(request, "COMMON/login.html")


def userRegister(request):
    return render(request, "COMMON/userRegister.html")


def artistRegister(request):
    if request.POST:
        skill = request.POST.getlist("skills")
        print(skill)
        
        skills = request.POST.get('skills', '')  # Retrieve the submitted skills value
        skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]  # Split the skills string into a list
        print(skills_list)
    return render(request, "COMMON/artistRegister.html")
