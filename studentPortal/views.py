from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.


def register(request):
    form = UserCreationForm()
    context = {"form": form}
    return render(request, "register.html", context)


def home(request):
    return render(request, "portal.html")
