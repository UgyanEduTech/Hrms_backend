# Generated by Django 4.2.16 on 2024-11-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee_Management', '0003_alter_employee_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginDetails',
            fields=[
                ('login_id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_id', models.IntegerField()),
                ('change_password_attempts', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('change_password_attempts_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]