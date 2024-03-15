from django.contrib.auth.models import User
from django.db import models

class userData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    UserPicture = models.ImageField(default='default.png')

class Twot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userdata = models.ForeignKey(userData, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    date = models.DateTimeField()

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=4096)
    expires_on = models.DateTimeField()