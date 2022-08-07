from django.db import models
from django.contrib.auth.models import User


class LoginLogoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.logout_time == None:
            return (
                self.user.username
                + " "
                + self.login_time.strftime("%m/%d/%Y, %H:%M:%S")
            )
        return (
            self.user.username
            + " "
            + self.login_time.strftime("%m/%d/%Y, %H:%M:%S")
            + self.logout_time.strftime("%m/%d/%Y, %H:%M:%S")
        )
