from django.shortcuts import render
from django.contrib import messages
from .models import Staff
from django.contrib.auth.models import User
# Create your views here.


def register(request):
    if 'submit' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            obj = Staff.objects.get(username=username)
            print(obj)
            if obj:
                # e = 'This username is taken. Please try again with different username.'
                # return render(request, 'login/register.html', {'e': e})
                messages.error(
                    request, f'This username is taken. Please try again with different username.')
        except:
            obj = Staff()
            obj.username = username
            obj.password = password
            obj.save()
            messages.success(
                request, f'Registeration Successfull. You may login now!!')
            return render(request, 'login/registet.html')
    return render(request, 'login/register.html')


def login(request):
    if 'submit' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            obj = Staff.objects.get(username=username)
            print(obj)
            if obj:
                if obj.password == password:
                    messages.success(request, f'Login Sucessfull !!')
                    return render(request, 'login/homepage.html')
                else:
                    messages.error(
                        request, f'This password is incorrect. Please enter the correct passsword.')
                    return render(request, 'login/login.html')
            else:
                messages.error(
                    request, f'Account with this username does not exist!! Please enter a valid username.')
                return render(request, 'login/login.html')
        except:
            return render(request, 'login/login.html')
    return render(request, 'login/login.html')


def home(request):
    return render(request, 'login/homepage.html')
