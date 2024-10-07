from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.user.username} on {self.date} at {self.time}"
