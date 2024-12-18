from django.db import models

class Designation(models.Model):
    E_id=models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    reports_to = models.CharField(max_length=100, null=True, blank=True)
