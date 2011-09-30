from django.db import models


class Rank(models.Model):
    name = models.CharField(max_length=255)
    patch = models.ImageField(upload_to='rank')
    
    def __unicode__(self):
        return self.name
    
    
