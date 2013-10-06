from django.db import models
from utils.values import reverse_states

class Unit(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=True)
    council = models.ForeignKey('council.Council', null=True, blank=True)
    state = models.CharField(max_length="2", choices=reverse_states, blank=True)
    city = models.CharField(max_length="255", blank=True)
    calendar = models.CharField(max_length=255, blank=True, null=True)
    
    def scouts(self):
        return self.members.filter(position__youth=True)
    
    
    def __unicode__(self):
        return '%s'%self.number