from django.shortcuts import render
from django.contrib import messages
from .models import Staff
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
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
            return render(request, 'login/register.html')
    return render(request, 'login/register.html')


def login(request):
    print('facelogin' in request.POST)
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
        except:
            messages.error(
                request, f'Account with this username does not exist!! Please enter a valid username.')
            return render(request, 'login/login.html')
    if 'facelogin' in request.POST:
        return render(request, 'login/homepage.html')
    return render(request, 'login/login.html')


def home(request):
    return render(request, 'login/homepage.html')

def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    except:
        pass   

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')
