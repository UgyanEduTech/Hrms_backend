# Generated by Django 5.1 on 2024-11-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_clockinout_logout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clockinout',
            name='logout_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
