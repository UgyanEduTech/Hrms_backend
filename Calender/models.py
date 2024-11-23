from django.db import models

# Create your models here.
# models.py
from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateField()

    
