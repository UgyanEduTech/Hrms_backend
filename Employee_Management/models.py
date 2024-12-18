from django.db import models
from django.utils import timezone

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    E_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.PositiveBigIntegerField()
    age = models.PositiveBigIntegerField()
    gender = models.CharField(max_length=2)
    Designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=timezone.now)  # Default value added
    date_joined = models.DateField(default=timezone.now)  # Default value added
    is_emp = models.BooleanField(default=False)
    is_HR = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password=models.CharField(max_length=255,null=True)
    profile_picture = models.ImageField(
        upload_to='employee_pics/',  # This will store images in media/employee_pics
        default='employee_pics/default.png',  # Default image if not provided
        null=True, 
        blank=True
    )


class LoginDetails(models.Model):
    login_id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)  
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    change_password_attempts = models.IntegerField(default=0)
    change_password_attempts_date = models.DateTimeField(null=True, blank=True)
    otp_expiration_time=models.DateTimeField(blank=True,null=True)

