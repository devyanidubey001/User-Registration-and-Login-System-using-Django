from authentication.services.authentication_service import AuthenticationService
from authentication.services.authentication_logging import AuthenticationLogging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class Handler:
    def __init__(
        self,
        authenticationService: AuthenticationService,
        authenticationLogging: AuthenticationLogging,
    ) -> None:
        self.authenticationService = authenticationService
        self.authenticationLogging = authenticationLogging

    def registration(self, request):
        user = self.authenticationService.getUserInSession(request)
        if user != None:
            return self.processLoginResponse(request, user)

        if request.method == "POST":
            # fetching values from request
            username = request.POST.get("username")
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            email = request.POST.get("email")
            pass1 = request.POST.get("pass1")
            pass2 = request.POST.get("pass2")

            # trying to register user
            registrationResult = self.authenticationService.registerUser(
                username, email, pass1, pass2, fname, lname
            )

            # returning error response in case of registration failure
            if isinstance(registrationResult, Exception):
                messages.error(request, str(registrationResult))
                return redirect("registration")

            myuser = registrationResult

            # logging registration time of user
            self.authenticationLogging.logRegistrationTime(myuser)

            messages.success(
                request,
                "Your Account has been created succesfully!!",
            )

            return redirect("login")

        return render(request, "authentication/registration.html")

    # Authenticating login of a user

    def userLoginAuthentication(self, request):
        # Check if user did not logout
        user = self.authenticationService.getUserInSession(request)
        if user != None:
            return self.processLoginResponse(request, user)

        if request.method == "POST":

            user = self.authenticationService.loginUser(request)

            # For User to login
            if user is None:
                messages.error(request, "Bad Credentials!!")
                return redirect("home")

            # To store the login time of user
            self.authenticationLogging.logLoginTime(user)

            return self.processLoginResponse(request, user)

        return render(request, "authentication/login.html")

    # Fetching login and logout history and rendering to logged in user
    def processLoginResponse(self, request, user):
        auth_history = self.authenticationLogging.getAuthenticationHistory(user)
        user_registration_time = self.authenticationLogging.getRegistrationTime(user)

        messages.success(request, "Logged In Sucessfully!!")
        fname = user.first_name
        return render(
            request,
            "authentication/succesfullLogin.html",
            {
                "fname": fname,
                "login_and_logout_history": auth_history,
                "registration_time": user_registration_time,
            },
        )

    # Log out user authentication
    def userLogoutAuthentication(self, request):
        user = self.authenticationService.logoutUser(request)
        # If user has not logged in
        if user == None:
            messages.error(request, "Please Log In First")
            return redirect("home")

        self.authenticationLogging.logLogoutTime(user)

        messages.success(request, "Logged Out Successfully!!")
        return redirect("home")
