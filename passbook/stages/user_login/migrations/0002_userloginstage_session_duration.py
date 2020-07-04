# Generated by Django 3.0.7 on 2020-07-04 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_stages_user_login", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userloginstage",
            name="session_duration",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Determines how long a session lasts, in seconds. Default of 0 means that the sessions lasts until the browser is closed.",
            ),
        ),
    ]
