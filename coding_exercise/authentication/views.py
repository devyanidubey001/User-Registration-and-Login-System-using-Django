from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from authentication.models import LoginLogoutLog
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def registration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try some other username."
            )
            return redirect("home")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect("home")

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect("home")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect("home")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect("home")

        myuser = User.objects.create_user(
            username=username, email=email, password=pass1
        )
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()
        LoginLogoutLog.objects.create(user=myuser, registration_time=timezone.now())
        messages.success(
            request,
            "Your Account has been created succesfully!!",
        )

        return redirect("login")

    return render(request, "authentication/registration.html")


def loginUser(request):
    if request.session.get("user") != None:
        return render(request, "authentication/succesfullLogin.html")

    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("password")
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            # For login and logout sessions
            request.session["user"] = user.username
            LoginLogoutLog.objects.create(user=user, login_time=timezone.now())
            user_history_for_login = LoginLogoutLog.objects.filter(user=user).order_by(
                "-login_time"
            )
            user_history_for_logout = LoginLogoutLog.objects.filter(user=user).order_by(
                "-logout_time"
            )
            login_and_logout_history = []
            for users in user_history_for_login:
                if users.login_time != None:
                    login_and_logout_history.append(("Login Time", users.login_time))
            for users in user_history_for_logout:
                if users.logout_time != None:
                    login_and_logout_history.append(("Logout Time", users.logout_time))
            login_and_logout_history.sort(key=lambda a: a[1])
            final_login_and_logout_history = []
            for time in login_and_logout_history:
                final_login_and_logout_history.append(
                    (time[0], time[1].strftime("%m/%d/%Y, %H:%M:%S"))
                )

            messages.success(request, "Logged In Sucessfully!!")
            fname = user.first_name
            registration_time = (
                LoginLogoutLog.objects.filter(user=user)
                .order_by("registration_time")
                .first()
            )
            print(registration_time, "registration_time")
            return render(
                request,
                "authentication/succesfullLogin.html",
                {
                    "fname": fname,
                    "login_and_logout_history": final_login_and_logout_history,
                    "registration_time": registration_time,
                },
            )
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect("home")

    return render(request, "authentication/login.html")


def logoutUser(request):

    username = request.session["user"]
    user = User.objects.filter(username=username).first()
    LoginLogoutLog.objects.create(user=user, logout_time=timezone.now())
    del request.session["user"]
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect("home")
