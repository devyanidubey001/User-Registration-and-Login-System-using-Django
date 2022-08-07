from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    # Home Page
    path("", views.home, name="home"),
    # Registration URL
    path("registration", views.registration, name="registration"),
    # Login URL
    path("login", views.loginUser, name="login"),
    # Logout URL
    path("logout", views.logoutUser, name="logout"),
]
