import uuid
from datetime import date, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.regex_helper import walk_to_end
from schoolAdmin.models import Invoice, InvoiceItem, Payment

from .forms import StudentLoginForm, StudentRegistrationForm
from .models import Student

# Create your views here.


def register(request):
    form = StudentRegistrationForm()
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "account was created for", user)
            return redirect("login")
    context = {"form": form}
    return render(request, "register.html", context)


def loginUser(request):

    form = StudentLoginForm()
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            url = reverse("studentPortal:home", kwargs={"adm": str(username)})
            if user is not None:
                login(request, user)
                return redirect(url)
            else:
                messages.info(request, "Username or Password incorrect")
    context = {}
    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("studentPortal:login")


login_required(login_url="studentPortal:login")


def home(request, adm):
    student = get_object_or_404(Student, admission_number=adm)
    fee_structure = student.get_fee_structure()

    def generate_invoice_for_student(student):
        fee_structure = student.get_fee_structure()

        if not fee_structure:
            raise ValueError("No fee structure found for student")

        total = (
            fee_structure.tuition_fee
            + (fee_structure.lunch_fee or Decimal("0.00"))
            + (fee_structure.transport_fee or Decimal("0.00"))
            + (fee_structure.other_fees or Decimal("0.00"))
        )

        invoice = Invoice.objects.create(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            student=student,
            academic_year=fee_structure.academic_year,
            term=student.term,
            total_amount=total,
            due_date=date.today() + timedelta(days=30),
        )

        return invoice

    context = {"student": student, "fee_structure": fee_structure}
    return render(request, "portal.html", context)
