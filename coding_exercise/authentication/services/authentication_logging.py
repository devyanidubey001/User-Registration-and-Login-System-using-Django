from authentication.models import LoginLogoutLog
from django.utils import timezone


class AuthenticationLogging:
    def logRegistrationTime(user):
        LoginLogoutLog.objects.create(user=user, registration_time=timezone.now())

    def logLoginTime(self, user):
        LoginLogoutLog.objects.create(user=user, login_time=timezone.now())

    def logLogoutTime(self, user):
        LoginLogoutLog.objects.create(user=user, logout_time=timezone.now())

    # Fetching registration time
    def getRegistrationTime(self, user):
        user_history_for_login = LoginLogoutLog.objects.filter(user=user).order_by(
            "-login_time"
        )
        user_registration_time = None
        for users in user_history_for_login:
            if users.registration_time != None:
                user_registration_time = users.registration_time
        return user_registration_time

    # Fetching login and logout history of the user
    def getAuthenticationHistory(self, user):
        user_history_for_login = LoginLogoutLog.objects.filter(user=user).order_by(
            "-login_time"
        )
        user_history_for_logout = LoginLogoutLog.objects.filter(user=user).order_by(
            "-logout_time"
        )
        login_and_logout_history = []
        user_registration_time = None
        for users in user_history_for_login:
            if users.registration_time != None:
                user_registration_time = users.registration_time
            if users.login_time != None:
                login_and_logout_history.append(("Login Time", users.login_time))
        for users in user_history_for_logout:
            if users.logout_time != None:
                login_and_logout_history.append(("Logout Time", users.logout_time))
        login_and_logout_history.sort(key=lambda a: a[1])
        final_login_and_logout_history = []
        for time in login_and_logout_history:
            final_login_and_logout_history.append(
                (
                    time[0],
                    time[1].astimezone().strftime("%m/%d/%Y, %-I:%H:%M:%S %p"),
                )
            )
        return final_login_and_logout_history
