from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

def loginpage(request):
    
    if request.user.is_authenticated:
        return redirect('/menu/home/')
    
    context = {
        'error' : ''
    }
    if request.method == "POST":
        user = authenticate(username = request.POST['username'],
                            password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/menu/home/')
        else:
            context = {
                'error' : 'Invalid Credentials *'
            }
        return render(request,'login.html',context)
    return render(request,'login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('/')

def signup(request):
    context = {'error': ''}
    if request.method == "POST":   
        user_check = User.objects.filter(username=request.POST['username'])
        if user_check.exists():
            context['error'] = "Username already exists"
        else:
            new_user = User(
                username=request.POST['username'],
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname'],
                email=request.POST['email'],
                age=request.POST['age'],
                phone=request.POST['phone'],
            )
            new_user.set_password(request.POST['password'])
            new_user.save()
            return redirect('/')  # Redirect to home page or login page
    return render(request, 'signup.html', context)

@login_required(login_url='/')
def user_details(request):
    user = request.user
    
    if request.user.is_superuser:
        details = User.objects.all()
    # Fetch details of the logged-in user
    else:
        details = User.objects.filter(id=user.id)
    
    return render(request, 'user_details.html', {'details': details})


@login_required(login_url='/')
def user_update(request, id):
    det = get_object_or_404(User, id=id)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=det)
        if user_form.is_valid():  # Add parentheses to call the function
            user_form.save()
            return redirect('/details/')
    else:
        user_form = UserForm(instance=det)
    context = {
        'user_form': user_form
    }
    return render(request, 'user_update_form.html', context)

@login_required(login_url='/')
def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('/logout/')

    return render(request, 'confirm_delete.html', {'user': user})
    

class CustomPasswordChangeView(LoginRequiredMixin,SuccessMessageMixin, PasswordChangeView):
    login_url = '/'
    template_name = 'password_change.html'
    success_message = "Your password has been successfully updated!"
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(LoginRequiredMixin,PasswordChangeDoneView):
    login_url = '/'
    template_name = 'password_change_done.html'


