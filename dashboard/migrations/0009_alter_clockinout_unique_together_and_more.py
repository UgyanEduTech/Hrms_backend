# Generated by Django 5.0.4 on 2024-11-14 07:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0008_merge_20241111_1248"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="clockinout",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="clockinout",
            name="login_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name="clockinout",
            name="reminder_5_min_sent",
        ),
        migrations.RemoveField(
            model_name="clockinout",
            name="working_hours",
        ),
    ]
