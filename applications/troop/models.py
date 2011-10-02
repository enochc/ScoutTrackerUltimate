from django.db import models


class Troop(models.Model):
    number = models.IntegerField()
    
    
    def __unicode__(self):
        return '%s'%self.number