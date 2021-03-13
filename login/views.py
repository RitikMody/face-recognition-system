from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Staff, Password
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
# for email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# Create your views here.


def register(request):
    if 'submit' in request.POST:
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        img = request.POST.get('img')
        try:
            obj = Staff.objects.get(username=username)
            obj = Staff.objects.get(email=email)
            print(obj)
            if obj:
                # e = 'This username is taken. Please try again with different username.'
                # return render(request, 'login/register.html', {'e': e})
                messages.error(
                    request, f'This username is taken. Please try again with different username.')
        except:
            obj = Staff()
            obj.fname = fname
            obj.lname = lname
            obj.email = email
            obj.username = username
            obj.passwrd = password
            obj.img = img
            obj.save()
            mail_subject = 'Verify your email account.'
            current_site = get_current_site(request)
            message = render_to_string('login/activate.html', {
                'user': obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
                'token': account_activation_token.make_token(obj),
            })
            to_email = obj.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(
                request, f'Registeration Successfull. Please verify your account!!')
            return render(request, 'login/register.html')
    return render(request, 'login/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Staff.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_active = True
        user.save()
        print("user registered")
        site = get_current_site(request)
        print(site)
        request.session['user_email'] = user.email
        return HttpResponse('Thank you for your email confirmation. You can now login!!')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    print('facelogin' in request.POST)
    if 'submit' in request.POST:
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        try:
            obj = Staff.objects.get(email=email)
            print(obj)
            if obj:
                if obj.passwrd == password:
                    request.session['email'] = email
                    print(request.session['email'])
                    return redirect('home')
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
    try:
        email = request.session['email']
        staff_obj = Staff.objects.get(email=email)
        pass_obj = Password.objects.all()
        pass_obj = pass_obj.filter(user=staff_obj)
        print(pass_obj)
        if 'form_submit' in request.POST:
            email = request.session['email']
            staff_obj = Staff.objects.get(email=email)
            app_name = request.POST.get('name')
            app_email = request.POST.get('email')
            password = request.POST.get('password')
            print(email)
            print(app_name)
            print(app_email)
            print(password)
            obj = Password()
            obj.user = staff_obj
            obj.app_email = app_email
            obj.app_name = app_name
            obj.app_password = password
            obj.save()
            return render(request, 'login/homepage.html', {'obj': pass_obj})

        if 'update' in request.POST:
            userid = request.POST.get('userid')
            app_name = request.POST.get('appname_update')
            app_email = request.POST.get('email_update')
            app_pass = request.POST.get('password')
            print(userid)
            print(app_name)
            try:
                obj = pass_obj.objects.get(app_name=app_name)
                if obj:
                    obj.app_email = app_email
                    obj.app_password = app_pass
                    obj.save()

            except:
                pass

        if 'delete' in request.POST:
            userid = request.POST.get('user_d')
            app_name = request.POST.get('appname_d')
            print(app_name)
            try:
                obj = pass_obj.objects.get(app_name=app_name)
                print(obj)
                if obj:
                    obj.delete()
            except:
                pass

        return render(request, 'login/homepage.html',  {'obj': pass_obj})
    except:
        return redirect('login')


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
