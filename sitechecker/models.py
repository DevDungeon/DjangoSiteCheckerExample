from django.contrib.auth.models import User
from django.db import models


class Site(models.Model):
    description = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    last_response_code = models.CharField(max_length=8, blank=True, null=True)
    last_time_checked = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class Check(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    response_code = models.CharField(max_length=8)
