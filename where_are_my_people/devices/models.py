from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    assigned_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    device_type = models.CharField(max_length=50, default='other')

class Location(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="locations")
    latitude = models.FloatField()
    longitude = models.FloatField()
    ping_time = models.DateTimeField()
