from django.db import models
from django.contrib.auth.models import User


class LoginLogoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        logString = self.user.username
        if self.registration_time != None:
            logString += (
                "Registration time"
                + self.registration_time.astimezone().strftime("%m/%d/%Y, %H:%M:%S")
            )
        if self.login_time != None:
            logString += "Login time" + self.login_time.astimezone().strftime(
                "%m/%d/%Y, %H:%M:%S"
            )
        if self.logout_time != None:
            logString += "Logout time" + self.logout_time.astimezone().strftime(
                "%m/%d/%Y, %H:%M:%S"
            )

        return logString
