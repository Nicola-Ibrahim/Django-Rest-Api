# Generated by Django 4.1.6 on 2023-07-16 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_alter_adminprofile_admin_alter_otpnumber_is_verified_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_password_changed",
            field=models.BooleanField(default=False, verbose_name="is_password_changed"),
        ),
    ]
