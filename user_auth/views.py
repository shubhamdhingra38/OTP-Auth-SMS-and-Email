from django.shortcuts import render, redirect
from cryptography.fernet import Fernet
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.urls import reverse
from .forms import UserRegistrationForm
from django.contrib.auth import login as django_login, logout as django_logout
from .otp_auth import PasswordlessAuthBackend, send_otp, verify_otp
from .models import MyUser


def authenticate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        status = verify_otp(phone_num=request.session['phone_num'], phone_code=data['phone_code'], 
                            email_id=request.session['email'], email_code=data['email_code'])

        if status:
            if data['type'] == 'register':
                form = UserRegistrationForm(data=request.session['form_data'])
                try:
                    form.save()
                    return JsonResponse({"message": "created new user"}, status=201)
                except:
                    errors = form.errors.get_json_data()
                    return JsonResponse(errors, status=400)
            elif data['type'] == 'login':
                user = PasswordlessAuthBackend.get_user(request, request.session['email']) 
                if user is not None:
                    django_login(request, user)
            return JsonResponse({"message": "Successfully verified the otp"}, status=200)
        else:
            return JsonResponse({"message": "Could not verify otp"}, status=400)


def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        form = UserRegistrationForm(data=data)

        if not form.is_valid():
            errors = form.errors.get_json_data()
            return JsonResponse(errors, status=400)

        try:
            send_otp(data['email'], data['phone_num'])
            request.session['form_data'] = data
            return JsonResponse({'message': "Successfully sent OTP"}, status=200)
        except:
            return JsonResponse({"message": "Problem with phone number/email address"}, status=400)

    return JsonResponse({"message": "Signup API"})

def signup_view(request):
    return render(request, 'user_auth/register.html')

def verification(request, type):
    return render(request, 'user_auth/verification.html', context={'type': type})


def login(request):
    context = {}
    error = None
    if request.method == 'POST':
        username = request.POST['email']
        user = PasswordlessAuthBackend.start_auth(request, username=username)
        if user is not None:
            request.session['email'] = user.email
            request.session['phone_num'] = user.phone_num 
            return redirect('verify', type='login')
        else:
            error = "Invalid details"
    if error is not None:
        context['error'] = error
    return render(request, 'user_auth/login.html', context=context)


def logout(request):
    django_logout(request)
    return redirect(reverse('home'))
    

def home(request):
    if 'email' in request.session:
        user = PasswordlessAuthBackend.get_user(request, request.session['email'])
        if user is not None and user.is_authenticated:
            return render(request, 'user_auth/home.html', context={'user': user})
    return render(request, 'user_auth/home.html', context={'error': "Please login first to see details"})