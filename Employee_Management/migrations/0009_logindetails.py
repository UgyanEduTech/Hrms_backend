# Generated by Django 5.0.4 on 2024-11-23 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "Employee_Management",
            "0008_alter_employee_age_alter_employee_date_joined_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="LoginDetails",
            fields=[
                ("login_id", models.AutoField(primary_key=True, serialize=False)),
                ("employee_id", models.IntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("otp_code", models.CharField(blank=True, max_length=6, null=True)),
                ("otp_created_at", models.DateTimeField(blank=True, null=True)),
                ("otp_verified", models.BooleanField(default=False)),
                ("change_password_attempts", models.IntegerField(default=0)),
                (
                    "change_password_attempts_date",
                    models.DateTimeField(blank=True, null=True),
                ),
            ],
        ),
    ]
