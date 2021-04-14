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
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                staff_obj = Staff.objects.get(email=email)
                if(staff_obj):
                    messages.error(
                        request, f'This email is already registered.')
            except:
                obj = form.save()
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

                return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})


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
        password = request.POST.get('password')
        try:
            obj = Staff.objects.get(email=email)
            print(obj)
            if obj:
                if obj.is_email_active:
                    if obj.passwrd == password:
                        print("matched")
                        request.session['email'] = email
                        print(request.session['email'])
                        return redirect('home')
                    else:
                        messages.error(
                            request, f'This password is incorrect. Please enter the correct passsword.')
                        return render(request, 'login/login.html')
                else:
                    messages.error(
                        request, f'Please verify your email account first.')

        except:
            messages.error(
                request, f'Account with this username does not exist!! Please enter a valid username.')
            return render(request, 'login/login.html')
    if 'facelogin' in request.POST:
        return render(request, 'login/login.html', {'set_value': 1})
    return render(request, 'login/login.html')


def home(request):
    try:
        print(request.session['email'])
        email = request.session['email']
        staff_obj = Staff.objects.get(email=email)
        pass_obj = Password.objects.all()
        pass_obj = pass_obj.filter(user=staff_obj)
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
            return render(request, 'login/homepage.html', {'obj': pass_obj, 'tab': 1})

        if 'update' in request.POST:
            userid = request.POST.get('userid')
            print(userid)
            app_name = request.POST.get('appname_update')
            app_email = request.POST.get('email_update')
            app_pass = request.POST.get('password')
            try:
                obj = pass_obj.get(id=userid)
                print(obj)
                if obj:
                    obj.app_name = app_name
                    obj.app_email = app_email
                    obj.app_password = app_pass
                    obj.save()
                    return render(request, 'login/homepage.html',  {'obj': pass_obj, 'tab': 1})

            except:
                pass

        if 'delete' in request.POST:
            userid = request.POST.get('user_d')
            print(userid)
            try:
                obj = pass_obj.get(id=userid)
                if obj:
                    obj.delete()
                    return render(request, 'login/homepage.html',  {'obj': pass_obj, 'tab': 1})
            except:
                pass

        if 'view' in request.POST:
            userid = request.POST.get('user_id_view')
            print(userid)
            try:
                obj = pass_obj.get(id=userid)
                if obj:
                    print(obj.app_password)
                    email = request.session['email']
                    mail_subject = 'Your account password.'
                    current_site = get_current_site(request)
                    message = "Your password for " + obj.app_name + " with username/email: " + \
                        obj.app_email + " is " + obj.app_password + "!!"
                    print(messages)
                    to_email = email
                    print(to_email)
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return render(request, 'login/homepage.html',  {'obj': pass_obj, 'tab': 1})
            except:
                pass

        if 'signout' in request.POST:
            email = request.POST.get('user_session')
            print(email)
            if request.session['email'] == email:
                try:
                    del request.session['email']
                    return redirect('login')
                except:
                    return HttpResponse("logout failed")
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
