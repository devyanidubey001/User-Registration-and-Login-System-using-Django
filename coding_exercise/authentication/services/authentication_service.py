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

    def getUserByUsername(self, username):
        return User.objects.filter(username=username).first()

    def getUserInSession(self, request):
        usernameFromSession = request.session.get("user")
        print("user from session", usernameFromSession)
        if usernameFromSession == None:
            return None

        return self.getUserByUsername(usernameFromSession)

    def loginUser(self, request):
        user = None

        username = request.POST.get("username")
        pass1 = request.POST.get("password")
        user = authenticate(username=username, password=pass1)

        if user == None:
            return None

        login(request, user)
        request.session["user"] = user.username
        return user

    def logoutUser(self, request):
        username = request.session.get("user")
        if username == None:
            return None

        user = self.getUserByUsername(username=username)
        logout(request)
        return user
