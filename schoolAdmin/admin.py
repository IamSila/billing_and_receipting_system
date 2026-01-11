from django.contrib import admin

from .models import Invoice, InvoiceItem, Payment

# Register your models here.


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "STATUS_CHOICES",
        "invoice_number",
        "academic_year",
        "total_amount",
        "amount_paid",
        "issued_at",
        "balance",
    ]
    list_filter = ["invoice_number", "issued_at", "academic_year", "amount_paid"]
    search_fields = ["invoice_number", "issued_at", "academic_year", "amount_paid"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "method", "paid_at")
    list_filter = ("method",)


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("invoice", "description", "amount")
    search_fields = ("description",)
