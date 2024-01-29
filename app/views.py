from django.shortcuts import render

# Create your views here.

from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def registration(request):
    UFO=UserForm()
    PFO=ProfileForm()
    d={'UFO':UFO,'PFO':PFO}
    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)

        if UFD.is_valid() and PFD.is_valid():
            MUFDO=UFD.save(commit=False)
            pw=UFD.cleaned_data['password']
            MUFDO.set_password(pw)                      #encryption
            MUFDO.save()

            MPFDO=PFD.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            MFPDO=PFD.save(commit=False)
            MFPDO.username=MUFDO
            MFPDO.save()

            send_mail(
                'Registration',
                'Registration is successful',
                'priyadarshita44@gmail.com',
                [MUFDO.email],
                fail_silently=False
            )
            return HttpResponse('Registration is successful')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Incorrect Username or Password.Please try again.')
    return render(request,'user_login.html')

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

# @login_required
# def change_password(request):
#     if request.method=='POST':
#         username=request.session.get('username')
#         UO=User.objects.get(username=username)
#         print(UO)
#         password=request.POST['password']
#         print(password,UO.password)
#         if UO.password==password:
#             pw=request.POST['pw']
#             print(pw)
#             # username=request.session.get('username')
#             # UO=User.objects.get(username=username)
#             # UO.set_password(pw)
#             # UO.save()
#             return HttpResponse('Password Changed Sucessfully')
#         else:
#             return HttpResponse('Write Correct Password')
#     return render(request,'change_password.html')

@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        npw=request.POST['pw']
        UO.set_password(npw)
        UO.save()
        return HttpResponse('Password Changed Sucessfully')
    return render(request,'change_password.html')

def forgot_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']

        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Reset password is done ')
        else:
            return HttpResponse('Username is not Valid')
    return render(request,'forgot_password.html')