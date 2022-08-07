from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class AuthenticationService:
    def registerUser(self, username, email, pass1, pass2, firstName, lastName):
        if User.objects.filter(username=username):
            return Exception("Username already exist! Please try some other username.")

        if User.objects.filter(email=email).exists():
            return Exception("Email Already Registered!!")

        if len(username) > 20:
            return Exception("Username must be under 20 charcters!!")

        if pass1 != pass2:
            return Exception("Passwords didn't matched!!")

        if not username.isalnum():
            return Exception("Username must be Alpha-Numeric!!")

        myuser = User.objects.create_user(
            username=username, email=email, password=pass1
        )
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.is_active = True
        myuser.save()

        return myuser

    def loginUser(self, request, user):
        login(request, user)

    def logoutUser(self, request):
        logout(request)
