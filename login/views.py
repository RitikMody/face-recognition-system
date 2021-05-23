############# uncomment line 28 and line 123 ######################

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
from PIL import Image
import numpy as np
from keras.models import load_model
import tensorflow as tf
from deepface import DeepFace
# net = DeepFace.OpenFace.loadModel()
from Crypto.Random import get_random_bytes
import os
from Crypto.Cipher import AES
import cv2
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password


classifier = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR, 'haarcascade_frontalface_default.xml'))

# Create your views here.
model = load_model("face_ver2.h5")


def pre_process(path):
    im = Image.open(path)
    out = im.resize((96, 96))
    out = np.expand_dims(out, axis=0)
    return np.array(out)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            del form.fields['password2']
            email = form.cleaned_data['email']
            try:
                staff_obj = Staff.objects.get(email=email)
                if(staff_obj):
                    messages.error(
                        request, f'This email is already registered.')
            except:
                password = form.cleaned_data['passwrd']
                hashed = make_password(password)
                obj = form.save()
                obj.passwrd = hashed
                obj.save()
                print(obj.img)
                frame = cv2.imread("media/"+str(obj.img))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bboxes = classifier.detectMultiScale(gray)
                if(len(bboxes) == 1):
                    for box in bboxes:
                        x, y, width, height = box
                        x2, y2 = x + width, y + height
                        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 1)
                        # FaceFileName = ".\captured_images\img.jpg"
                        # status = cv2.imwrite(FaceFileName, frame)
                        crop_img = frame[y:y2, x:x2]
                        FaceFileName = "media/"+str(obj.img)
                        os.remove(FaceFileName)
                        status = cv2.imwrite(FaceFileName, crop_img)

                else:
                    messages.error(
                        request, f'Unable to detect a unique face. Please upload one with just your face.')
                    obj.delete()
                    return redirect('register')

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
                    if check_password(password, obj.passwrd):
                        print("matched")
                        request.session['email'] = email
                        print(request.session['email'])
                        return redirect('home')
                    else:
                        messages.warning(
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
        x = pre_process('captured_images/img2.jpg')
        y = 'media/'
        email = request.POST.get('facelogin_email')
        scores = {}
        try:
            obj = Staff.objects.get(email=email)
            if obj:
                score = model.predict([x, pre_process(y + '/' + str(obj.img))])
                print(score)
                if score > 0.75:
                    try:
                        obj = Staff.objects.get(email=email)
                        print(obj)
                        if obj:
                            if obj.is_email_active:
                                request.session['email'] = email
                                return redirect('home')
                            else:
                                messages.error(
                                    request, f'Please verify your email account first.')
                                return redirect('login')
                    except:
                        pass
                else:
                    messages.error(
                        request, 'Unable to recognise the face.')
                    return redirect('login')
            else:
                messages.error(
                    request, f'No such email exist.Please register first')
        except:
            messages.error(
                request, f'No such email exist.Please register first')
            return redirect('login')

        #     obj = Staff.objects.get(img='images/' + image)
        #     score = 0
        #     score = model.predict([x, pre_process(y + '/' + image)])
        #     if score > 0.5:
        #         scores[obj.email] = score
        # print(scores)
        # if len(scores) > 0:
        #     print(len(scores))
        #     email = max(scores, key=scores.get)
        #     try:
        #         obj = Staff.objects.get(email=email)
        #         print(obj)
        #         if obj:
        #             if obj.is_email_active:
        #                 request.session['email'] = email
        #                 return redirect('home')
        #             else:
        #                 messages.error(
        #                     request, f'Please verify your email account first.')
        #                 return redirect('login')
        #     except:
        #         pass
        # else:
        #     messages.error(
        #         request, 'Unable to recognise the face.')
        #     return redirect('login')
        #     # return render(request, 'login/login.html', {'set_value': 0})

        return render(request, 'login/login.html', {'set_value': 1})

    return render(request, 'login/login.html')


def encrypt_pass(email, pwd):
    key = get_random_bytes(16)
    file_out = open(str(email) + ".b", "wb")
    file_out.write(key)
    print("Generated key bytes:", key)
    cipher_aes = AES.new(key, AES.MODE_EAX)
    print("AES Generated")
    ciphertext, tag = cipher_aes.encrypt_and_digest(pwd.encode('utf-8'))
    passwd = cipher_aes.nonce + tag + ciphertext
    print(len(cipher_aes.nonce), len(tag), len(ciphertext))
    print(len(passwd))
    return passwd


def home(request):
    try:
        print(request.session['email'])
        email = request.session['email']
        staff_obj = Staff.objects.get(email=email)
        name = staff_obj.fname + " " + staff_obj.lname
        pass_obj = Password.objects.all()
        pass_obj = pass_obj.filter(user=staff_obj)
        if 'form_submit' in request.POST:
            email = request.session['email']
            staff_obj = Staff.objects.get(email=email)
            app_name = request.POST.get('name')
            app_email = request.POST.get('email')
            password = request.POST.get('password')
            print("Encrypting")
            password = encrypt_pass(email, password)
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
            return render(request, 'login/homepage.html', {'obj': pass_obj, 'tab': 1, 'name': name})

        if 'update' in request.POST:
            userid = request.POST.get('userid')
            print(userid)
            app_name = request.POST.get('appname_update')
            app_email = request.POST.get('email_update')
            app_pass = request.POST.get('password')
            app_pass = encrypt_pass(email, app_pass)
            try:
                obj = pass_obj.get(id=userid)
                print(obj)
                if obj:
                    obj.app_name = app_name
                    obj.app_email = app_email
                    obj.app_password = app_pass
                    obj.save()
                    return render(request, 'login/homepage.html',  {'obj': pass_obj, 'tab': 1, 'name': name})

            except:
                pass

        if 'delete' in request.POST:
            userid = request.POST.get('user_d')
            print(userid)
            try:
                obj = pass_obj.get(id=userid)
                if obj:
                    obj.delete()
                    return render(request, 'login/homepage.html',  {'obj': pass_obj, 'tab': 1, 'name': name})
            except:
                pass

        if 'view' in request.POST:
            userid = request.POST.get('user_id_view')
            print(userid)
            obj = pass_obj.get(id=userid)
            if obj:
                print(obj.app_password)
                email = request.session['email']
                password = obj.app_password
                file_out = open(str(email) + ".b", "rb")
                key = file_out.read()
                print("key", key)
                print("password", len(password[:16]), "_______________", len(
                    password[16:32]), "______________", len(password[32:]))
                cipher_aes = AES.new(key, AES.MODE_EAX, password[:16])
                data = cipher_aes.decrypt_and_verify(
                    password[32:], password[16:32])
                password = data.decode('utf-8')
                mail_subject = 'Your account password.'
                current_site = get_current_site(request)
                message = "Your password for " + obj.app_name + " with username/email: " + \
                    obj.app_email + " is " + password
                print(messages)
                to_email = email
                print(to_email)
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'login/homepage.html',  {'obj': pass_obj, 'tab': 1, 'name': name})

        if 'signout' in request.POST:
            email = request.POST.get('user_session')
            print(email)
            if request.session['email'] == email:
                try:
                    del request.session['email']
                    return redirect('login')
                except:
                    return HttpResponse("logout failed")
        return render(request, 'login/homepage.html',  {'obj': pass_obj, 'name': name})
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
