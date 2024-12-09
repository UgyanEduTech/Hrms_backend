from django.db import models
from django.utils import timezone 
from django.utils.timezone import now


class ClockInOut(models.Model):
    E_id = models.CharField(max_length=12)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)
    shift_end_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    login_attempts = models.PositiveIntegerField(default=0)
    reset_attempts = models.PositiveIntegerField(default=0)

class MonthlyTarget(models.Model):
      target_id=models.AutoField(primary_key=True)
      month = models.CharField(max_length=20)
      year = models.IntegerField()
      target_value = models.FloatField()
      actual_value = models.FloatField()
      difference = models.FloatField(null=True, blank=True)
      status = models.CharField(max_length=20)
      emp_id = models.CharField(max_length=50)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)




class Message(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically sets the timestamp when created

    def __str__(self):
        # You can adjust the string representation to fit your needs
        return f"Message: {self.text[:50]} - {self.timestamp}"  # Adjusted to show more of the message text


