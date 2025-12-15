from django.urls import path

from . import views

app_name = "schoolAdmin"

urlpatterns = [
    path("base/", views.base, name="base"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("students/", views.students, name="students"),
    path("invoices/", views.invoices, name="invoices"),
    path("payments", views.payments, name="payments"),
    path("receipts", views.receipts, name="receipts"),
    path("reports/", views.reports, name="reports"),
    path("settings/", views.settings, name="settings"),
]
