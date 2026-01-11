from datetime import date
from decimal import Decimal

from django.db import models
from studentPortal.models import (FeeStructure, Parent, SchoolClass, Student,
                                  StudentProfile)

# Create your models here.


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PARTIAL", "Partially Paid"),
        ("PAID", "Paid"),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="invoices"
    )

    academic_year = models.CharField(max_length=20)
    term = models.CharField(max_length=10)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")

    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    class Meta:
        db_table = "invoices"

    def __str__(self):
        return self.invoice_number

    @property
    def balance(self):
        return self.total_amount - self.amount_paid


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "invoice_items"

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("CASH", "Cash"),
        ("MPESA", "MPESA"),
        ("BANK", "Bank"),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=100, blank=True, null=True)

    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments"
