from django.shortcuts import render
from .forms import CreateUserForm
# Create your views here.


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "register.html", context)


def home(request):
    return render(request, "portal.html")
