from django.shortcuts import render

# Create your views here.

from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail

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
            MUFDO.set_password(pw)
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

