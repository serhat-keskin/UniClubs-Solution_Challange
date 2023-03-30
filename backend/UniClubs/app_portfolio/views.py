from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q,Count #filtreleme opsiyonları için import ettik
from django.contrib import messages  #hata mesajlarını bu kütüphane ile yazdırıyoruz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm  # user için form aslında model formlarıyla aynı sayılır
from django.http import HttpResponse
from . import models as portfolio_models
# from .forms import MyUserCreationForm, UpdateUserForm
# from django.contrib.auth.models import User  #ESKİ DEFAULT USER MODEL
from app_base.models import User #yeni custom user model
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View
from django.core.files.base import ContentFile  #file handle
import requests, json, copy, datetime, traceback
from django.utils import timezone

def index(request):
    # data = portfolio_models.<your_model>.objects.filter(is_active=True)
    # context = {'data': data}
    # return render(request,'app_portfolio/sks/index.html', context)
    return render(request,'app_portfolio/index.html')




