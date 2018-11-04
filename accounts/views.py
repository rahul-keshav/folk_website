from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm,EditProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login


def home(request):
    return render(request,'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('home:home'))
        else:
            messages.warning(request,"please correct the error below")
    else:
        form = RegistrationForm()
    return render(request,'accounts/reg_form.html',{'form': form,})


def view_profile(request,pk=None):
    if pk:
        user=User.objects.get(pk=pk)
    else:
        user=request.user
    args={'user':user}
    return render(request,'accounts/profile.html',args)


def edit_profile(request):
    if request.method=='POST':
        form=EditProfile(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:edit_profile'))
    else:
        form=EditProfile(instance=request.user)
        return render(request,'accounts/edit_profile.html',{'form':form,})



def change_password(request):
    if request.method== 'POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))

    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'accounts/edit_profile.html',args)

