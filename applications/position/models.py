from django.db import models

class Position(models.Model):
            
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    youth = models.BooleanField(default=True)

    
    def __unicode__(self):
        return '%s'% (self.name)
    
    
