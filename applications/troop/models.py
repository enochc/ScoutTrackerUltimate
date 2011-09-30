from django.db import models

from django.contrib.auth.models import User

class Troop(models.Model):
    number = models.IntegerField()
    
    
