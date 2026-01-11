from django.urls import path

from . import views

app_name = "studentPortal"
urlpatterns = [
    # remember to change this path and the view
  path("home/<str:adm>/", views.home, name="home"),
  path("register/", views.register, name="register"),
  path("login/", views.loginUser, name='login'),
  path("logout/", views.logoutUser, name='logout')

]
