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
                return redirect("login")

            myuser = registrationResult

            # logging registration time of user
            self.authenticationLogging.logRegistrationTime(myuser)

            messages.success(
                request,
                "Your Account has been created succesfully!!",
            )

            return redirect("login")

        return render(request, "authentication/registration.html")

    def userLoginAuthentication(self, request):

        if request.session.get("user") != None:
            return render(request, "authentication/succesfullLogin.html")

        if request.method == "POST":
            username = request.POST.get("username")
            pass1 = request.POST.get("password")
            user = authenticate(username=username, password=pass1)
            # For User to login
            if user is not None:
                self.authenticationService.loginUser(request, user)
                # For login and logout sessions
                request.session["user"] = user.username
                # To store the login time of user
                self.authenticationLogging.logLoginTime(user)

                final_login_and_logout_history = (
                    self.authenticationLogging.getAuthenticationHistory(user)
                )
                user_registration_time = self.authenticationLogging.getRegistrationTime(
                    user
                )

                messages.success(request, "Logged In Sucessfully!!")
                fname = user.first_name
                return render(
                    request,
                    "authentication/succesfullLogin.html",
                    {
                        "fname": fname,
                        "login_and_logout_history": final_login_and_logout_history,
                        "registration_time": user_registration_time,
                    },
                )
            else:
                messages.error(request, "Bad Credentials!!")
                return redirect("home")

        return render(request, "authentication/login.html")

    def userLogoutAuthentication(self, request):
        username = request.session.get("user")
        if username == None:
            messages.error(request, "Please Log In First")
            return redirect("home")
        user = User.objects.filter(username=username).first()
        self.authenticationLogging.logLogoutTime(user)
        self.authenticationService.logoutUser(request)
        messages.success(request, "Logged Out Successfully!!")
        return redirect("home")
