"""E_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
    path('login-page/' , views.Login.as_view() , name = "login-page"),
    path('login/' , views.LoginView , name = "login"),
    path('register/' , views.Register , name = "register"),
    path('create_account/' , views.CreateAccount.as_view() , name = "create-account-page"),
    path('check_username/', views.CheckUserName , name = "check-username"),
    path('check_email/', views.CheckEmail , name = "check-email"),
    path('logout/', views.LogoutView , name = 'logout-page'),
]