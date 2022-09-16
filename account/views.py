import json

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, CreateView, TemplateView
from django.conf import settings


class Login(CreateView):
    template_name = 'account/login.html'
    model = User
    fields = ['username' , 'password']



class CreateAccount(TemplateView):
    template_name = 'account/create_account.html'

def Register(request):
    data = json.loads(request.body)
    email = data['email']
    username = data['username']
    password = data['password']
    user = User(email=email , username=username)
    user.set_password(password)
    user.save()
    return JsonResponse({'status' : 'success'})

def CheckUserName(request):
    print("OMAD")
    username = request.GET.get('username')
    check_user = User.objects.filter(username=username).exists()
    if check_user:
        return JsonResponse({'status' : 'invalid'})
    else:
        return JsonResponse({'status': 'valid'})


def CheckEmail(request):
    data = json.loads(request.body)
    email = data['email']
    print(email)
    check_email = User.objects.filter(email=email).exists()
    print(check_email)
    if check_email:
        return JsonResponse({'status': 'invalid'})
    else:
        return JsonResponse({'status': 'valid'})


def LoginView(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = User.objects.filter(username=username).first()
    if user is not None:
        check_password = user.check_password(password)
        if check_password:
            login(request , user)
            return JsonResponse({'status' : 'successful'})
        return JsonResponse({'status': "unsuccessful"})
    else:
        return JsonResponse({'status' : "unsuccessful"})

def LogoutView(request):
    logout(request)
    return redirect(reverse("login-page"))