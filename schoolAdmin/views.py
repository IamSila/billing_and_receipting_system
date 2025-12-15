from django.shortcuts import render

# Create your views here.


def base(request):
    return render(request, "base.html")


def dashboard(request):
    return render(request, "dashboard.html")


def students(request):
    return render(request, "students.html")


def invoices(request):
    return render(request, "invoices.html")


def payments(request):
    return render(request, "payments.html")


def receipts(request):
    return render(request, "receipts.html")


def reports(request):
    return render(request, "reports.html")


def settings(request):
    return render(request, "Settings.html")
