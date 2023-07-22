from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def registration(request):
    usfo=UserForm()
    pfo=ProfileModelForm()
    d={'usfo':usfo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        usfd=UserForm(request.POST)
        pfd=ProfileModelForm(request.POST,request.FILES)

        if usfd.is_valid() and pfd.is_valid():
            NSUFO=usfd.save(commit=False)
            submittedPW=usfd.cleaned_data['password']
            NSUFO.set_password(submittedPW)
            NSUFO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()

            send_mail('Registration','Emchestunnav',
                        'narasimhab8555@gmail.com',
                        [NSUFO.email],
                        fail_silently=False)

            return HttpResponse('successful')

    return render(request,'registration.html',d)



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))    