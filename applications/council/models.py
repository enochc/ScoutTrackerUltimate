from django.db import models

class Council(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    
    

