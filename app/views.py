from django.shortcuts import render

# Create your views here.

from app.forms import *

def registration(request):
    UFO=Userform()
    PFO=Profileform()
    d={'UFO':UFO,'PFO':PFO}
    

    return render(request,'registration.html',d)