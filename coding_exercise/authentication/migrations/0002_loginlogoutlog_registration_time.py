# Generated by Django 4.1 on 2022-08-07 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="loginlogoutlog",
            name="registration_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]