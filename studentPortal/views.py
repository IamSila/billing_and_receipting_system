from django.shortcuts import render, redirect
from .forms import CreateUserForm, StudentRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def register(request):
    #form = CreateUserForm()
    form = StudentRegistrationForm()
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "account was created for", user)
            return redirect('login')
    context = {"form": form}
    return render(request, "register.html", context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('studentPortal:home')
        else:
            messages.info(request, "Username or Password incorrect")
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('studentPortal:login')
def home(request):
    return render(request, "portal.html")
