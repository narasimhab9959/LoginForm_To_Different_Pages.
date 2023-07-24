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


@login_required
def display_details(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)

    d={'UO':UO,'PO':PO}
    return render(request,'display_details.html',d)

@login_required
def Change_Password(request):
    if request.method == 'POST':
        PW=request.POST.get('PW')
        UN=request.session.get('username')
        UO=User.objects.get(username=UN)
        UO.set_password(PW)
        UO.save()

        return HttpResponse('password is updated')
    return render(request,'Change_Password.html')



def reset_password(request):
    if request.method =='POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        rwp=request.POST.get('rwp')
        LUO=User.objects.filter(username=un)
        if LUO:
            if pw==rwp:
                UO=LUO[0]
                UO.set_password(pw)
                UO.save()
                return HttpResponse('re-set password is success')
            else:
                return HttpResponse('not match')
        else:
            return HttpResponse('invalid username')
    return render(request,'reset_password.html')


    return render(request,'reset_password.html')