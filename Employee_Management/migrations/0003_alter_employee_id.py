# Generated by Django 5.1 on 2024-11-06 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee_Management', '0002_alter_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.IntegerField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
