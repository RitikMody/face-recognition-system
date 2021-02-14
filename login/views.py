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
            if not obj:
                try:
                    Staff.objects.create(username=username, password=password)
                    return render(request, 'login/login.html')
                except:
                    return render(request, 'login/register.html')
            else:
                e = 'This username is taken. Please try again with different username.'
                return render(request, 'login/register.html', {'e': e})
        except:
            return render(request, 'login/login.html')
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
                    return render(request, 'login/homepage.html')
                else:
                    return render(request, 'login/login.html')
            else:
                return render(request, 'login/register.html')
        except:
            return render(request, 'login/login.html')
    return render(request, 'login/login.html')


def home(request):
    return render(request, 'login/homepage.html')
