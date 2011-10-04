from django.db import models


class Troop(models.Model):
    number = models.IntegerField()
    calendar = models.CharField(max_length=255, blank=True, null=True)
    
    def scouts(self):
        return self.members.filter(position__youth=True)
    
    
    def __unicode__(self):
        return '%s'%self.number