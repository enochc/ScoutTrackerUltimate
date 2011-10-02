from django.db import models


class Rank(models.Model):
    class Meta:
        ordering = ['order']
        
    name = models.CharField(max_length=255)
    patch = models.ImageField(upload_to='rank')
    order = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    
    
