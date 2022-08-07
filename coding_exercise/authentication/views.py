from re import I
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from authentication.services.authentication_service import AuthenticationService
from authentication.Handler import Handler
from authentication.services.authentication_logging import AuthenticationLogging

# initializing services here

authenticationService = AuthenticationService()
authenticationLogging = AuthenticationLogging()
handler = Handler(authenticationService, authenticationLogging)


# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def registration(request):
    return handler.registration(request)


def loginUser(request):
    return handler.userLoginAuthentication(request)


def logoutUser(request):

    return handler.userLogoutAuthentication(request)
