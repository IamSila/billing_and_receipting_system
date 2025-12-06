from django.urls import path

from . import views

app_name = "studentPortal"
urlpatterns = [
    # remember to change this path and the view
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
]
